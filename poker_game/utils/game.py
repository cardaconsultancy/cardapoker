# TODO: when BB has not enough chips, the other players should be calling the BB and not his max bet
from utils.evaluate_hand import evaluate_hand, get_hand_rank, card_rank_value
from utils.objects_on_table import Pot, Deck
import logging
from operator import attrgetter
from collections import deque
from utils.next_player import get_next_player
from utils.pot_management import create_pots, check_for_side_pots, fill_current_pot, check_if_rest_folded_and_pay

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
    
    def start_game(self, rounds_before_raise_blinds=20):
        self.table.dealer = self.table.players_game[0]
        game_on = True
        number_of_rounds = 1
        while game_on == True:
            for raising_time in range(0, rounds_before_raise_blinds):
                print()
                print() 
                print()
                for player in self.table.players_game:
                    self.logger.debug(f'Player {player.name} has {player.chips.amount} chips') 
                game_on = self.start_round()
                self.logger.debug(f'Blinds raised {raising_time} times')
            self.table.increase_blinds()
            number_of_rounds += 1
            if number_of_rounds > 10:
                break
        return False

    def start_round(self):
        # reset the deck
        self.deck = Deck()

        # Reset community cards at the beginning of each round
        self.table.community_cards = []

        # move the dealer button
        self.logger.debug(f"the dealer is {self.table.dealer.name}.")

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
        self.betting_round(preflop_round=True)
        if check_if_rest_folded_and_pay(self.table) == True:
            return True
        
        self.logger.debug(f"Bets are made") 
        self.logger.debug(f"Total betted {sum(player.total_in_pots_this_game for player in self.table.players)}.")

        # Deal the flop (three community cards)
        self.table.community_cards.append(self.deck.deal())
        self.table.community_cards.append(self.deck.deal())
        self.table.community_cards.append(self.deck.deal())
        for card in self.table.community_cards:
            self.logger.debug(f"On the table comes {card.rank} of {card.suit}.")

        # Betting Round 2: flop
        if all(player.all_in or player.folded for player in self.table.players_game):
            print('Everybody is all in, no more bets!')
        
        else:
            self.logger.debug(f"Players can bet on the flop.")
            self.betting_round()
            self.logger.debug(f"Total is {sum(player.total_in_pots_this_game for player in self.table.players)}.")
        
        if check_if_rest_folded_and_pay(self.table):
            return True
        
        # Deal the turn (one additional community card)
        self.table.community_cards.append(self.deck.deal())
        self.logger.debug(f"On the table comes {self.table.community_cards[3].rank} of {self.table.community_cards[3].suit}.") 

        # Betting Round 3
        if all(player.all_in or player.folded for player in self.table.players_game):
            print('Everybody is all in, no more bets!')
        
        else:
            self.logger.debug(f"Players can bet on the flop.")
            self.betting_round()
            self.logger.debug(f"Total is {sum(player.total_in_pots_this_game for player in self.table.players)}.")
        
        if check_if_rest_folded_and_pay(self.table):
            return True
        
        # Deal the river (one final community card)
        self.table.community_cards.append(self.deck.deal())
        self.logger.debug(f"On the table comes {self.table.community_cards[4].rank} of {self.table.community_cards[4].suit}.") 

        # Betting Round 4
        if all(player.all_in or player.folded for player in self.table.players_game):
            print('Everybody is all in, no more bets!')
        
        else:
            self.logger.debug(f"Players can bet on the river, final bet!")
            self.betting_round()
            self.logger.debug(f"Total is {sum(player.total_in_pots_this_game for player in self.table.players)}.")
        
        if check_if_rest_folded_and_pay(self.table):
            return True
        
        # Determine the winner(s)
        self.logger.debug(f"Pay_the_winner(s)")
        self.pay_winners()

        # Clean up
        clean_up(self.table)

        return True
        # winner = self.determine_winner()
        # self.logger.debug(f"The winner is {winner.name}!!!")

    def betting_round(self, preflop_round = False):
        print()
        self.logger.debug(f"The dealer is {self.table.dealer.name}.")
        # print()
        # required_action = 0

        # if first == True:
        #     # self.table.players_game[0].bet(self.table.blind_size)
        #     self.table.players_game[self.table.dealer+1].total_bet_betting_round += self.table.blind_size
        #     self.logger.debug(f"Player {self.table.players_game[self.table.dealer+1].name} has the small blind of {self.table.players_game[self.table.dealer+1].total_bet_betting_round}")
        #     self.logger.debug(f"Player {self.table.players_game[self.table.dealer+1].name} has the small blind of {self.table.players_game[self.table.dealer+1].total_bet_betting_round}")
        #     self.table.players_game[self.table.dealer+1].chips.lose(self.table.blind_size)
        #     self.table.players_game[self.table.dealer+1].total_bet_betting_round = (self.table.blind_size)
        #     self.table.players_game[self.table.dealer+1].total_in_pots_this_game = (self.table.blind_size)

        #     # self.table.players_game[1].bet(self.table.blind_size*2)
        #     self.table.players_game[self.table.dealer+2].total_bet_betting_round += self.table.blind_size*2
        #     self.logger.debug(f"Player {self.table.players_game[self.table.dealer+2].name} has the big blind of {self.table.players_game[self.table.dealer+2].total_bet_betting_round}")
        #     self.table.players_game[self.table.dealer+2].chips.lose(self.table.blind_size*2)
        #     self.table.players_game[self.table.dealer+2].total_bet_betting_round = (self.table.blind_size*2)
        #     self.table.players_game[self.table.dealer+2].total_in_pots_this_game = (self.table.blind_size*2)
        #     required_action = -2
        # else:
        #     full_round_player = self.table.players_game[self.table.dealer]
        #     self.logger.debug(f"The game ends when {full_round_player.name} is about to get his turn again")


        self.logger.debug(f" ------------- Start betting round ------------- ")
        # max 100 
        all_are_done = False

        # do we have to initialise it here or is there a smarter way to make this while loop work?
        last_raiser = self.table.dealer
        player = get_next_player(last_raiser, self.table)

        # create a second indicator that helps with letting the BB have another turn
        # create another variable for if it is the first_bet
        BB_can_have_another_go = False
        first_bet = True
        if preflop_round == True:
            BB_can_have_another_go = True
            first_bet = False

        for pl in self.table.players_game:
            print('check: ', pl.name)

        counter = 0
        while player != last_raiser and counter <10:
            for pl in self.table.players_game:
                print('check: ', pl.name)
            if first_bet == True and preflop_round == False:
                last_raiser = player
                self.logger.debug(f"this is the first round and so {last_raiser.name} is the last raiser")
                first_bet = False
            self.logger.debug(f" the current last raiser is {last_raiser.name} with {last_raiser.total_bet_betting_round} chips")

            counter += 1
            
            self.logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the betting round pot")
            # self.logger.debug(f'required_action {required_action}')

            # check if player has the big or small blind
            # for player in self.table.players_game:
            #     self.logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the betting round pot")
            #     self.logger.debug(f'required_action {required_action}')
            #     for playerprint in self.table.players_game:
            #         print('-------', playerprint.total_bet_betting_round)

            # if required_action == -2:
            #     self.logger.debug(f'skipping {player.name} as he/she has the small blind')
            #     required_action += 1
            #     continue
            # if required_action == -1:
            #     self.logger.debug(f'skipping {player.name} as he/she has the big blind')
            #     required_action += 1
            #     full_round_player = self.table.players_game[0]
            #     last_raiser = player 
            #     continue

            # This takes care of the exception: this is the player on which the bet has to end in the first round, regardless of what he/she does
            # if no one else raises, this is where it ends.
            # last_raiser = player

            if preflop_round == True:
                player.total_bet_betting_round += self.table.blind_size
                self.logger.debug(f"Player {player.name} has the small blind of {player.total_bet_betting_round}")
                if player.chips.lose(self.table.blind_size) == False:
                    self.logger.debug(f"Player {player.name} is all in")
                    player.all_in = True
                    player.total_bet_betting_round = player.chips.amount
                    player.total_in_pots_this_game = player.chips.amount
                    player.chips.lose(player.chips.amount)
                else:
                    player.total_bet_betting_round = (self.table.blind_size)
                    player.total_in_pots_this_game = (self.table.blind_size)

                player = get_next_player(player, self.table)
                player.total_bet_betting_round += self.table.blind_size*2
                self.logger.debug(f"Player {player.name} has the big blind of {player.total_bet_betting_round}")

                if player.chips.lose(self.table.blind_size*2) == False:
                    self.logger.debug(f"Player {player.name} is all in")
                    player.all_in = True
                    player.total_bet_betting_round = player.chips.amount
                    player.total_in_pots_this_game = player.chips.amount
                    player.chips.lose(player.chips.amount)
                else:
                    player.total_bet_betting_round = (self.table.blind_size*2)
                    player.total_in_pots_this_game = (self.table.blind_size*2)

                # to get the max bet? Can also be changed.
                last_raiser = player
                self.logger.debug(f"The last raiser is now {player.name} with {player.total_bet_betting_round}")

                preflop_round = False
                print('1. checking??', player.name)
                player = get_next_player(player, self.table)
                print('2. checking??', player.name)

            for pl in self.table.players_game:
                print('check: ', pl.name)
            self.logger.debug(f"{player.name} is up.")
            # bet_sizes = [player.total_bet_betting_round for player in self.table.players_game]
            # self.logger.debug(f'bet sizes {bet_sizes}')
            # check if all in or folded
            if not player.all_in or player.folded:
                # add the 'first' rule to account for the time when a person has a big blind and is the last raiser.
                if player != last_raiser or (player == last_raiser and BB_can_have_another_go == True):
                    self.logger.debug(f"{player.name} is not the last raiser (or had the BB)")
                    # get info for response
                    # max_bet = max(bet_sizes)
                    max_bet = last_raiser.total_bet_betting_round

                    # check if betsize of lastraiser is lower than theirs 
                    # (this can happen if the SB or is higher than the chipsstack and player is the BB), if so make current player lastraiser
                    if max_bet < player.total_bet_betting_round:
                        self.logger.debug(f"Because {last_raiser.name}'s {max_bet} chips is less than {player.name}'s {player.total_bet_betting_round}, make this the last bet")
                        last_raiser = player

                    self.logger.debug(f"-------- {player.name} has to match {max_bet} from last raiser {last_raiser.name}")
                    
                    for gambler in self.table.players_game:
                        print(gambler.name, gambler.total_bet_betting_round)

                    # ugly but this prevents the users from making mistakes (or cheating) by this functionality in their standard function.
                    ################## user call #####################
                    player_bet = player.response(max_bet, player.hand, self.table.community_cards)
                    # print(f'the player bet is {player_bet}')
                    ##################################################

                    for gambler in self.table.players_game:
                        print(gambler.name, gambler.total_bet_betting_round)

                    self.logger.debug(f"total bet was {player.total_bet_betting_round}")
                    # new_bet = player.total_bet_betting_round + player_bet
                    self.logger.debug(f"total bet is {player.total_bet_betting_round + player_bet}")

                    # check if the betsize is bigger than the chips, if so correct by making it the max bet 
                    if player.total_bet_betting_round + player_bet >= player.total_bet_betting_round + player.chips.amount:
                        self.logger.debug(f"{player.name} goes all in because {player.total_bet_betting_round + player_bet} >= {player.total_bet_betting_round + player.chips.amount}, so automatically the player is all in!!")
                        player_bet = player.chips.amount
                        # what is left and what is bet is the all in
                        player.chips.lose(player.chips.amount)
                        player.total_bet_betting_round += (player_bet)
                        player.total_in_pots_this_game += (player_bet)
                        self.logger.debug(f"{player.name} new bet is {player.total_bet_betting_round}.")
                        player.all_in = True

                        # check if the all in player is raising (seems better than to check for all options if player is all in)
                        if player.total_bet_betting_round > max_bet:
                            last_raiser = player
                            self.logger.debug(f"----{player.name} is the last raiser")

                    # Folding
                    elif player.total_bet_betting_round + player_bet < max_bet:
                        player.chips.lose(player.chips.amount)
                        self.logger.debug(f"Player {player.name} folds as {player.total_bet_betting_round + player_bet} is smaller than {max_bet} and NO all in. He/she loses his/her chips")
                        # add to total_bet as this must be added to the pot (don't remove yet from player_list)
                        player.total_bet_betting_round += (player_bet)
                        player.total_in_pots_this_game += (player_bet)
                        player.folded = True

                    # Checking
                    elif player.total_bet_betting_round + player_bet == max_bet and player_bet == 0:
                        # print(player.name, player.chips.amount, '????????????????????????')
                        # player.chips.lose(player.total_bet_betting_round)
                        # player.total_bet_betting_round += player_bet
                        # player.total_in_pot_this_game += player.total_bet_betting_round
                        player.raised_called_or_checked_this_round = True
                        self.logger.debug(f"Player {player.name} checks with {player_bet} and has {player.chips.amount} chips left")


                    # Calling
                    elif player.total_bet_betting_round + player_bet == max_bet:
                        player.chips.lose(player_bet)
                        print(player_bet)
                        print(player.total_bet_betting_round)
                        player.total_in_pots_this_game += player_bet
                        player.total_bet_betting_round += player_bet
                        player.raised_called_or_checked_this_round = True
                        self.logger.debug(f"Player {player.name} calls with {player_bet}, making the total {player.total_bet_betting_round} this round. He/she has {player.chips.amount} chips left")

                    # Raising
                    elif player.total_bet_betting_round + player_bet > max_bet:
                        player.chips.lose(player_bet)
                        player.total_bet_betting_round += player_bet
                        player.total_in_pots_this_game += player_bet
                        player.raised_called_or_checked_this_round = True
                        self.logger.debug(f"Player {player.name} throws in {player_bet}, raising to {player.total_bet_betting_round} and has {player.chips.amount} chips left")
                        last_raiser = player
                        self.logger.debug(f"----{player.name} is the last raiser")
                    
                    # remove the special status of Big Blind is removed if we continue
                    if player == last_raiser and BB_can_have_another_go == True:
                        BB_can_have_another_go = False

                    player.total_bet += player.total_in_pots_this_game
                    # required_action += 1

                    # set first to False to make sure that we select the last raiser next time.
                    # first = False
                # else:
                #     self.logger.debug(f"Player {player.name} was the last raiser")
                #     all_are_done = True
                # update the all_are_done
            else:
                self.logger.debug(f"Player {player.name} has folded or is all in")

            self.logger.debug(f'total bet: {player.total_bet_betting_round}')
            self.logger.debug(f'NR of players in game = {len(self.table.players_game)}')
            self.logger.debug(f"-- The player was {player.name}")
            # The player who has the small blind makes the first bet in poker, which is why we can get the next one directly
            player = get_next_player(player, self.table)

            if player == last_raiser:
                print("IT SHOULD END HERE")

                # sugg
                # playernr = 0
                # while not all_are_done:
                #     player = playerlist[playernr]
                #     if not folded or all in:
                #         # works in two man heads up
                #         if not last_raiser:
                #             do action
                #             if raise:
                #                 update last_raiser = player
                #         else:
                #             all_are_done = True
                #     playernr += 1
                #     
                # 
                
                # this is incorrect, someone could check and then someone raises
                # rather than making a complex average, just check whether someone has raised (a seperate attribute) and the rest hasn't folded
                # if so continue

            # all_are_done = all(player.folded == True or player.raised_called_or_checked_this_round == True or player.all_in == True for player in self.table.players_game)

            # bet_sizes = [player.total_bet_betting_round for player in self.table.players_game]
            # avg_bet = sum(bet_sizes) / len(self.table.players_game)
            # max_bet = max(bet_sizes)

        for player in self.table.players_game:
            print('1', player.total_bet_betting_round, player.chips.amount)           

        for player in self.table.players_game:
            print(player.name)
            print(player.folded, player.raised_called_or_checked_this_round, player.all_in)

        # all players are either all in or folded or have called/checked/raised
        self.logger.debug(f"Betting round over")

        # create pots
        create_pots(self.table)
    
    def pay_winners(self):
        for pot in self.table.pots:
            last_pot = self.table.pots[-1]
            winner_list = self.determine_winners(last_pot.players)
            bounty = last_pot.amount / len(winner_list)
            for winner in winner_list:
                self.logger.debug(f"{winner.name} gets {bounty} chips")
                winner.chips.win(bounty)
            self.logger.debug(f"Removing {self.table.pots.pop()}, so {len(self.table.pots)} pots left")

    def determine_winners(self, pot_players):
        # Determine the best hand for each player
        # dict_example = {}
        winner_list = []
        for player in pot_players:
            player.set_best_hand(get_hand_rank(player, self.table))
            self.logger.debug(f"{player.name} highest hand is {player.best_hand}")
            self.logger.debug(f"- {player.name} has hand {player.best_hand}")
            # create a list of players
            winner_list.append(player)

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
                    metric_list.append(card_rank_value(player.best_hand[metric]))
                # print('-----------', metric_list)
            max_metric = max(metric_list)
            mask = []
            for metric in metric_list:
                # self.logger.debug(f"  2b. Metric score {metric}")
                if metric == max_metric:
                    mask.append(True)
                else:
                    mask.append(False)
            # use the mask to select True candidates from winner_list
            relevant_winners = []
            for i in range(len(winner_list)):
                # self.logger.debug(f"  2c. {i} of {len(winner_list)}")
                if mask[i]:
                    relevant_winners.append(winner_list[i])
                    self.logger.debug(f"{winner_list[i].name} is in winner list")
            winner_list = relevant_winners
            if len(winner_list) == 1:
                self.logger.debug(f"0. The winner is {winner_list[0].name}")
                break
        if len(winner_list) != 1:
            self.logger.debug(f"0. There is a tie between winners:")
            for winner in winner_list:
                self.logger.debug(f"- {winner.name}")
        return winner_list