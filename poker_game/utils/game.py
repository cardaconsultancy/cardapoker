from utils.objects_on_table import Card, Chips
import logging
from operator import attrgetter
from collections import deque

class TexasHoldemGame:
    winners = []
    HAND_RANKS = {
        'High Card': 0,
        'One Pair': 100,
        'Two Pair': 200,
        'Three of a Kind': 300,
        'Straight': 400,
        'Flush': 500,
        'Full House': 600,
        'Four of a Kind': 700,
        'Straight Flush': 800,
        'Royal Flush': 900
    }

    def __init__(self, table, deck):
        self.table = table
        self.deck = deck
        self.logger = logging.getLogger(__name__)

    def start_game(self, table):
        for raising_time in range(0, 20):
            for round in range(0, 20):
                self.start_round(self)
            self.table.increase_blinds

    def start_round(self):
        # Reset community cards at the beginning of each round
        self.table.community_cards = []

        # move the dealer button
        self.logger.debug(f"the dealer is {self.table.dealer_seat}.")

        # create a temporary deque to easily rotate 
        self.table.players_game = deque(self.table.players)
        self.table.players_game.rotate(-self.table.small_blind_seat)
        self.table.players_game = list(self.table.players)

        # Deal two private cards to each player
        # (Chosen to stay the closest to the real game, by not dealing two at once)
        for player in self.table.players_game:
            player.receive_card(self.deck.deal())
        for player in self.table.players_game:
            player.receive_card(self.deck.deal())

        # Betting Round 1
        self.logger.debug(f"Players can make their first bet.")
        self.betting_round(first=True)
        self.logger.debug(f"Bets are made") 
        self.logger.debug(f"Total is {sum(player.total_bet_betting_round for player in self.table.players)}.")

        # Deal the flop (three community cards)
        self.table.community_cards.append(self.deck.deal())
        self.table.community_cards.append(self.deck.deal())
        self.table.community_cards.append(self.deck.deal())
        for card in self.table.community_cards:
            self.logger.debug(f"On the table lies {card.rank} of {card.suit}.")

        # Betting Round 2
        self.logger.debug(f"Players can bet on the flop.")
        self.betting_round()
        self.logger.debug(f"Total is {sum(player.total_bet_betting_round for player in self.table.players)}.")

        # Deal the turn (one additional community card)
        self.table.community_cards.append(self.deck.deal())
        self.logger.debug(f"On the table comes {self.table.community_cards[3].rank} of {self.table.community_cards[3].suit}.") 

        # Betting Round 3
        self.logger.debug(f"Players can bet on the flop.")
        self.betting_round()
        self.logger.debug(f"Total is {sum(player.total_bet_betting_round for player in self.table.players)}.")

        # Deal the river (one final community card)
        self.table.community_cards.append(self.deck.deal())
        self.logger.debug(f"On the table comes {self.table.community_cards[4].rank} of {self.table.community_cards[4].suit}.") 


        # Betting Round 4
        self.logger.debug(f"Players can bet on the river, final bet!")
        self.betting_round()
        self.logger.debug(f"Total is {sum(player.total_bet_betting_round for player in self.table.players)}.")

        # Determine the winner
        winner = self.determine_winner()
        self.logger.debug(f"The winner is {winner.name}!!!")


    def betting_round(self, first = False):
        required_action = 0

        if first == True:
            self.table.players_game[0].bet(self.table.blind_size)
            # ugly but this prevents the users from making mistakes our cheating by removing the lost chips.
            # perhaps make bet the parent
            self.table.players_game[0].chips.lose(self.table.blind_size)
            self.table.players_game[0].total_bet_betting_round += self.table.blind_size
            self.logger.debug(f"Player {self.table.players_game[0].name} has the small blind of {self.table.players_game[0].total_bet_betting_round} and has {self.table.players_game[0].chips.amount} chips left")

            self.table.players_game[1].bet(self.table.blind_size*2)
            self.table.players_game[1].chips.lose(self.table.blind_size*2)
            self.table.players_game[1].total_bet_betting_round += self.table.blind_size*2
            self.logger.debug(f"Player {self.table.players_game[1].name} has the big blind of {self.table.players_game[1].total_bet_betting_round} and has {self.table.players_game[1].chips.amount} chips left")

            required_action = -2
        self.logger.debug(f" ------------- Start betting round ------------- ")
        # max 100 
        while required_action < 100:
            print('ho', required_action)
            for player in self.table.players_game:
                self.logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the pot")
                self.logger.debug(f'required_action {required_action}')
                if required_action == -2:
                    self.logger.debug(f'skipping {player.name} as he/she has the small blind')
                    required_action += 1
                    continue
                if required_action == -1:
                    self.logger.debug(f'skipping {player.name} as he/she has the big blind')
                    required_action += 1
                    continue
                self.logger.debug(f"{player.name} is up.")
                bet_sizes = [player.total_bet_betting_round for player in self.table.players_game]
                self.logger.debug(f'bet sizes {bet_sizes}')
                # get info for response
                max_bet = max(bet_sizes)
                self.logger.debug(f"Max bet size = {max_bet}")
                
                # ugly but this prevents the users from making mistakes (or cheating) by this functionality in their standard function.
                player_bet = player.response(max_bet)
                self.logger.debug(f"total bet was {player.total_bet_betting_round}")
                player.total_bet_betting_round = player.total_bet_betting_round + player_bet
                self.logger.debug(f"total bet is {player.total_bet_betting_round}")

                # check if the betsize is bigger than the chips, if so correct by making it the max bet
                # TODO Still have to figure out side pots 
                player.chips.lose(player_bet)

                if player.total_bet_betting_round >= player.chips.amount:
                    self.logger.debug(f"{player.name} goes all in!")
                    player.total_bet_betting_round = player.chips
                
                elif player.total_bet_betting_round < max_bet:
                    self.logger.debug(f"Player {player.name} folds as {player.total_bet_betting_round} is smaller than {max_bet} and loses his/her chips")
                    self.table.players_game.remove(player)
                    self.logger.debug(f"left are {self.table.players_game}")
                    if len(self.table.players_game) < 2:
                        break
                elif player.total_bet_betting_round == max_bet and player_bet == 0:
                    self.logger.debug(f"Player {player.name} checks with {player_bet} and has {player.chips.amount} chips left")
                elif player.total_bet_betting_round == max_bet:
                    self.logger.debug(f"Player {player.name} calls with {player_bet} and has {player.chips.amount} chips left")
                elif player.total_bet_betting_round > max_bet:
                    self.logger.debug(f"Player {player.name} throws in {player_bet}, raising to {player.total_bet_betting_round} and has {player.chips.amount} chips left")
 
                player.total_bet_game = player.total_bet_betting_round
                required_action += 1

            bet_sizes = [player.total_bet_betting_round for player in self.table.players_game]
            avg_bet = sum(bet_sizes) / len(self.table.players_game)
            max_bet = max(bet_sizes)
            self.logger.debug(f'total bet: {player.total_bet_betting_round}')
            self.logger.debug(f'NR of players in game = {len(self.table.players_game)}')
            for player in self.table.players_game:
                print('1', player.total_bet_betting_round)           
            if all(player.total_bet_betting_round == avg_bet for player in self.table.players_game):
                self.logger.debug(f"Betting round over")
                required_action = 9999
                for player in self.table.players_game:
                    player.total_bet_betting_round = 0
                    self.logger.debug(f"Reset total bets {player.name} to {player.total_bet_betting_round}")

    def determine_winner(self):
        # Determine the best hand for each player
        # dict_example = {}
        winner_list = []
        for player in self.table.players_game:
            player.set_best_hand(self.get_hand_rank(player))
            self.logger.debug(f"{player.name} highest hand is {player.best_hand}")
        ## player_hands = {player: self.get_best_hand(player) for player in self.table.players}
            self.logger.debug(f"- {player.name} has hand {player.best_hand}")
            # create a list of players
            winner_list.append(player)
            # print('----+++++++++-----', winner_list)
            # dict_example[player] = player.best_hand
        # print(dict_example)
        # Find the maximum best_hand value among players

        # the old fashioned way + check ---- I select the name. I could also just get the highest hand rank and select 
        # the name from the list of names
        for metric in range(0,5):
            self.logger.debug(f"1. Metric nr {metric}")
            # get the max metric in hand rank
            metric_list = []
            # print('-----------', metric_list)
            for player in winner_list:
                self.logger.debug(f"  2a. Player {player.name} with {player.best_hand}")
                if metric == 0:
                    metric_list.append(player.best_hand[metric])
                else:
                    metric_list.append(self.card_rank_value(player.best_hand[metric]))
                # print('-----------', metric_list)
            max_metric = max(metric_list)
            mask = []
            for metric in metric_list:
                self.logger.debug(f"  2b. Metric score {metric}")
                if metric == max_metric:
                    mask.append(True)
                else:
                    mask.append(False)
            # use the mask to select True candidates from winner_list
            relevant_winners = []
            for i in range(len(winner_list)):
                self.logger.debug(f"  2c. {i} of {len(winner_list)}")
                if mask[i]:
                    relevant_winners.append(winner_list[i])
                    self.logger.debug(f"{winner_list[i].name} is in winner list")
            winner_list = relevant_winners
        self.logger.debug(f"0. The winner list {winner_list[0].name}")


            # new way
            # max_best_hand = max(self.table.players_game, key=attrgetter('best_hand')).best_hand[metric]
            # print(f"----------{max_best_hand}")



            # deselect all the players that are not that rank
            # for player in self.table.players_game:
                
            # if more than one go to next metric

            # if no more return list of winners
            # print(max_best_hand)

        # Find the players with the maximum best_hand attribute
        winners = [player for player in self.table.players if player.best_hand == max_best_hand]
        ## Find the player with the best hand
        ## winner = max(player_hands, key=lambda player: player_hands[player])
        # winning_cards = max(dict_example.values())
        # winners = [key for key, value in dict_example.items() if value == winning_cards]
        # self.logger.debug(f"{winning_cards} are highest")

        winners = []
        for player in self.table.players_game:
            if player.best_hand == max_best_hand:
                self.logger.debug(f"Player {player.name} is a winner because {player.hand} == {max_best_hand} given on table {self.table.community_cards}")
                winners.append(player)

        # choose one winner for now
        winner = winners[0]

        # Award the pot to the winner
        pot = sum(player.total_bet_game for player in self.table.players)
        self.logger.debug(f"Winner {winner.name} wins {pot}")

        # side pot

        # can't bet more than you have.
        
        # reset game --> needs to be refactored
        for player in self.table.players:
            # remove players who have 0 chips
            if player.chips.amount <= 0:
                self.table.players.remove(player)
                self.logger.debug(f"Player {player.name} is out of chips and leaves the table")
            # reset bet
            player.total_bet_game = 0
            # return cards
            player.hand = []
        if len(self.table.players) == 1:
            print(f'THE WINNER IS {self.table.players[0].name}')
        
        # move dealer button --> needs to be refactored
        self.table.change_dealer_and_blinds()
        self.logger.debug(f"Player {winner.name} is out of chips and leaves the table")

        winner.chips.win(pot)

        return winner

    def is_royal_flush(self, sorted_hand):
        self.logger.debug("Checking for Royal Flush...")
        if self.is_straight_flush(sorted_hand) and sorted_hand[0].rank == 'A':# incorrect, i think this is wrong as a person could have A, 10 with 9, 8, 7, 6, 5 on the board
            self.logger.debug(f"Found Royal Flush!")
            return True
        else:
            self.logger.debug(f"No Royal Flush")


    def is_straight_flush(self, sorted_hand):
        self.logger.debug("Checking for Straight Flush...")
        if self.is_straight(sorted_hand) and self.is_flush(sorted_hand):
            self.logger.debug(f"Found Straight Flush.")
            return True
        else:
            self.logger.debug(f"No Straight Flush")

    def is_four_of_a_kind(self, sorted_hand):
        self.logger.debug("Checking for Four of a Kind...")
        for i in range(len(sorted_hand) - 3):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank == sorted_hand[i + 2].rank == sorted_hand[i + 3].rank:
                self.logger.debug("Four of a Kind found!")
                return True
        self.logger.debug("No Four of a Kind.")
        return False

    def is_full_house(self, sorted_hand):
        self.logger.debug("Checking for Full House...")
        is_full_house = self.is_three_of_a_kind(sorted_hand) and self.is_one_pair(sorted_hand)
        self.logger.debug(f"Is Full House: {is_full_house}")
        return is_full_house

    def is_flush(self, sorted_hand):
        self.logger.debug("Checking for Flush...")
        is_flush = all(card.suit == sorted_hand[0].suit for card in sorted_hand)
        self.logger.debug(f"Is Flush: {is_flush}")
        return is_flush

    def is_straight(self, sorted_hand):
        self.logger.debug("Checking for Straight...")
        for i in range(1, len(sorted_hand)):
            if self.card_rank_value(sorted_hand[i - 1].rank) != self.card_rank_value(sorted_hand[i].rank) + 1:
                self.logger.debug("No Straight.")
                return False
        self.logger.debug("Straight found!")
        return True

    def is_three_of_a_kind(self, sorted_hand):
        self.logger.debug("Checking for Three of a Kind...")
        for i in range(len(sorted_hand) - 2):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank == sorted_hand[i + 2].rank:
                self.logger.debug("Three of a Kind found!")
                return True
        self.logger.debug("No Three of a Kind.")
        return False

    def is_two_pair(self, sorted_hand):
        self.logger.debug("Checking for Two Pair...")
        pairs = 0
        for i in range(len(sorted_hand) - 1):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank and pairs == 0:
                self.logger.debug("First pair found!")

                # remove the two cards to easily access the kickers                
                first_pair_rank = sorted_hand[i].rank
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                self.logger.debug(f"rest is now {sorted_hand}")

                pairs += 1
            if sorted_hand[i].rank == sorted_hand[i + 1].rank and pairs == 1:
                second_pair_rank = sorted_hand[i].rank
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                self.logger.debug(f"rest is now {sorted_hand}")
                handscore = [2, first_pair_rank, second_pair_rank, sorted_hand[0].rank, None, None]
                return handscore
            # fill the rest with first, second and third kicker
        self.logger.debug(f"No two Pair!")
        return False
    
    def card_rank_value(self, rank):
        return '23456789TJQKA'.index(rank) + 2
    
    def is_one_pair(self, sorted_hand):
        self.logger.debug("Checking for One Pair...")
        for i in range(len(sorted_hand) - 1):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank:
                self.logger.debug("One Pair found!")

                # remove the two cards to easily access the kickers
                pair_rank = sorted_hand[i].rank
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                self.logger.debug(f"7-2={sorted_hand}")
                
                # fill the rest with first, second and third kicker
                handscore = [1, pair_rank, sorted_hand[0].rank, sorted_hand[1].rank, sorted_hand[2].rank, None]
                self.logger.debug(f"Handscore = {handscore}")
                return handscore
        self.logger.debug("No One Pair.")
        return False

    def display_table(self):
        for player in self.table.players:
            print(f"{player.name}'s hand: {player.show_hand()}")

        print(f"Community cards: {', '.join(map(str, self.table.community_cards))}")

    def evaluate_hand(self, all_cards):
        sorted_hand = sorted(all_cards, key=lambda card: self.card_rank_value(card.rank), reverse=True)
        self.logger.debug(f"...Checking for different hand Ranks.. for {sorted_hand}")
        # if self.is_royal_flush(sorted_hand):
        #     return self.HAND_RANKS['Royal Flush']
        # elif self.is_straight_flush(sorted_hand):
        #     return self.HAND_RANKS['Straight Flush']
        # elif self.is_four_of_a_kind(sorted_hand):
        #     return self.HAND_RANKS['Four of a Kind']
        # elif self.is_full_house(sorted_hand):
        #     return self.HAND_RANKS['Full House']
        # elif self.is_flush(sorted_hand):
        #     return self.HAND_RANKS['Flush']
        # elif self.is_straight(sorted_hand):
        #     return self.HAND_RANKS['Straight']
        # elif self.is_three_of_a_kind(sorted_hand):
        #     return self.HAND_RANKS['Three of a Kind']
        # elif self.is_two_pair(sorted_hand):
        #     return self.HAND_RANKS['Two Pair']
        hand_rank = self.is_two_pair(sorted_hand)
        if hand_rank == False:
            hand_rank = self.is_one_pair(sorted_hand)
        elif hand_rank == False:
            self.logger.debug("Return high card...")
            hand_rank = [0, sorted_hand[0].rank, sorted_hand[1].rank, sorted_hand[2].rank, sorted_hand[3].rank, sorted_hand[4].rank]
        return hand_rank


    def get_hand_rank(self, player):
        # print('self.table.community_cards: ', self.table.community_cards)
        # print('player.hand: ', player.hand)
        self.logger.debug(f"...Checking for different hand Ranks for {player.name }")

        for card in self.table.community_cards:
            self.logger.debug(f"On the table lies {card.rank} of {card.suit}.")
        for card in player.hand:
            self.logger.debug(f"   {player.name} has a {card.rank} of {card.suit}.")
        all_cards = player.hand + [Card(card[0], card[1]) for card in self.table.community_cards]
        hand_rank = self.evaluate_hand(all_cards)
        self.logger.debug(f"The best hand is {hand_rank}")
        return hand_rank