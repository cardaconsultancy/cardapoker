from utils.objects_on_table import Card, Pot
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
    
    def card_rank_value(self, rank):
        if rank == None:
           return 0
        return '123456789TJQKA'.index(rank) + 1
    
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
        if self.check_if_all_folded() == True:
            return 'game finished'
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
        
        if self.check_if_all_folded() == True:
            return 'game finished'
        
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
        
        if self.check_if_all_folded() == True:
            return 'game finished'
        
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
        
        if self.check_if_all_folded() == True:
            return 'game finished'
        
        # Determine the winner(s)
        self.logger.debug(f"Pay_the_winner(s)")
        self.pay_winners()

        # Clean up
        self.clean_up()

        return 'game finished'
        # winner = self.determine_winner()
        # self.logger.debug(f"The winner is {winner.name}!!!")


    def betting_round(self, first = False):
        required_action = 0

        if first == True:
            # self.table.players_game[0].bet(self.table.blind_size)
            self.table.players_game[0].total_bet_betting_round += self.table.blind_size
            self.logger.debug(f"Player {self.table.players_game[0].name} has the small blind of {self.table.players_game[0].total_bet_betting_round}")
            self.table.players_game[0].chips.lose(self.table.blind_size)
            self.table.players_game[0].total_bet_betting_round = (self.table.blind_size)
            self.table.players_game[0].total_in_pots_this_game = (self.table.blind_size)

            # self.table.players_game[1].bet(self.table.blind_size*2)
            self.table.players_game[1].total_bet_betting_round += self.table.blind_size*2
            self.logger.debug(f"Player {self.table.players_game[1].name} has the big blind of {self.table.players_game[1].total_bet_betting_round}")
            self.table.players_game[1].chips.lose(self.table.blind_size*2)
            self.table.players_game[1].total_bet_betting_round = (self.table.blind_size*2)
            self.table.players_game[1].total_in_pots_this_game = (self.table.blind_size*2)

            required_action = -2
        self.logger.debug(f" ------------- Start betting round ------------- ")
        # max 100 
        while required_action != 100:
            print('ho', required_action)
            # if required_action > 9:
            #     1 / 0
            for player in self.table.players_game:
                self.logger.debug(f"{player.name} is up and currently has {player.total_bet_betting_round} in the betting round pot")
                self.logger.debug(f'required_action {required_action}')
                # for playerprint in self.table.players_game:
                #     print('-------', playerprint.total_bet_betting_round)
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
                ####### user call #########
                player_bet = player.response(max_bet)
                # print(f'the player bet is {player_bet}')
                ################

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
                    player.all_in = True
                
                elif player.total_bet_betting_round + player_bet < max_bet:
                    player.chips.lose(player.chips.amount)
                    self.logger.debug(f"Player {player.name} folds as {player.total_bet_betting_round + player_bet} is smaller than {max_bet} and NO all in. He/she loses his/her chips")
                    # add to total_bet as this must be added to the pot
                    player.total_bet_betting_round += (player_bet)
                    player.total_in_pots_this_game += (player_bet)
                    player.folded = True

                elif player.total_bet_betting_round + player_bet == max_bet and player_bet == 0:
                    print(player.name, player.chips.amount, '????????????????????????')
                    # player.chips.lose(player.total_bet_betting_round)
                    # player.total_bet_betting_round += player_bet
                    # player.total_in_pot_this_game += player.total_bet_betting_round
                    self.logger.debug(f"Player {player.name} checks with {player_bet} and has {player.chips.amount} chips left")

                elif player.total_bet_betting_round + player_bet == max_bet:
                    player.chips.lose(player_bet)
                    print(player_bet)
                    print(player.total_bet_betting_round)
                    player.total_in_pots_this_game += player_bet
                    player.total_bet_betting_round += player_bet
                    self.logger.debug(f"Player {player.name} calls with {player_bet}, making the total {player.total_bet_betting_round} this round and {player.total_in_pots_this_game} this game. He/she has {player.chips.amount} chips left")

                elif player.total_bet_betting_round + player_bet > max_bet:
                    player.chips.lose(player_bet)
                    player.total_bet_betting_round += player_bet
                    player.total_in_pots_this_game += player_bet
                    self.logger.debug(f"Player {player.name} throws in {player_bet}, raising to {player.total_bet_betting_round} and has {player.chips.amount} chips left")
        
                player.total_bet += player.total_in_pots_this_game
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
                if len(self.table.pots) == 0:
                    main_pot = Pot()
                    main_pot.players = self.table.players_game
                    self.table.pots.append(main_pot)
                    self.logger.debug(f"No pot yet, so created {len(self.table.pots)} main pot")
                self.check_for_side_pots()
                required_action = 100
                for player in self.table.players_game:
                    player.total_in_pots_this_game += player.total_bet_betting_round
                    player.total_bet_betting_round = 0
                    self.logger.debug(f"Reset total bets {player.name} to {player.total_bet_betting_round}")

    def check_if_all_folded(self):
        at_least_two_not_folded = []
        for player in self.table.players_game:
            if player.is_folded == False:
                at_least_two_not_folded.append(player)
        if len(at_least_two_not_folded) < 2:
            # skipp_all
            at_least_two_not_folded[0].chips.win(bounty)
            self.clean_up()
            return 1

    def check_for_side_pots(self):
        self.logger.debug(f"checking for side pots")

        # get the minimum bet fromt he people that did not fold:
        not_folded = []
        for player in self.table.players_game:
            # get all the minimum bet
            if player.folded == False:
                not_folded.append(player)
        lowest_bet = min([player.total_bet_betting_round for player in not_folded])
        check_for_side_pots = True
        self.logger.debug(f"lowest bet == {lowest_bet}")
        sidepot_created = False
        counter = 1
        while check_for_side_pots == True and counter < 5:
            
            # check if there is only 1 person not all in, reduce his/her bet by the difference with the max bidder.
            if len([player for player in not_folded if not player.all_in]) == 1:

                # Find the player who is not all-in
                non_all_in_player = next(player for player in not_folded if not player.all_in)
                # print(non_all_in_player.name)

                # Find the max bet among all-in players
                all_in_bet = max(player.total_bet_betting_round for player in not_folded if player.all_in)
                # print(all_in_bet, non_all_in_player.total_bet_betting_round)

                # This is the only case in which we give players back money in mid game as we cannot guarantee who joins.
                non_all_in_player.chips.give_back(non_all_in_player.total_bet_betting_round - all_in_bet)

                # Adjust the bet of the non all-in player
                non_all_in_player.total_bet_betting_round = all_in_bet
                self.logger.debug(f"As {non_all_in_player.name} was the only one not all in, his/her bet got reduced by {non_all_in_player.total_bet_betting_round - all_in_bet}")

            # check if the players all betted the same amount, if so take shortcut (also necessary to prevent loop):
            if lowest_bet == max([player.total_bet_betting_round for player in not_folded]):
                self.logger.debug(f"Every player is in with the same amount")
                check_for_side_pots = False
                self.fill_current_pot(not_folded[0])
                return None
            
            counter += 1
            print('keep looping for more side pots')
            check_for_side_pots = False
            for player in not_folded[:]:
                if player.total_bet_betting_round == lowest_bet:
                    self.logger.debug(f"player {player.name} has the lowest bet of {lowest_bet}")
                    if player.chips.amount == 0:
                        self.logger.debug(f"player {player.name} went all in, side pot is needed")
                        # fill up original pot & create side pot
                        self.fill_current_pot(player)
                        side_pot = Pot()
                        side_pot.players = not_folded
                        self.table.pots.append(side_pot)
                        sidepot_created = True
                        check_for_side_pots = True
                        player.folded = True
                        not_folded.remove(player)
                        print(f'the rest of the list {not_folded}')
                elif player.total_bet_betting_round == 0 and player.folded == False:
                    self.logger.debug(f"{player.name} also went all in with the minimum bet")
                    not_folded.remove(player)
                    print(f'the rest of the list {not_folded}')
            if sidepot_created == False:
                self.logger.debug(f"No (more) sidepots created")
                # just get a person that did not fold, as there are no sidepots his/her bet will be the same as the others.
                self.fill_current_pot(not_folded[0])
                for pot in self.table.pots:
                    print(f'---------- pot {pot} is {pot.amount}')
                return None
                    # get the minimum bet fromt he people that did not fold:
            
            # get a new minimum
            lowest_bet = min([player.total_bet_betting_round for player in not_folded])
            check_for_side_pots = True
            self.logger.debug(f"new lowest bet == {lowest_bet}")

            self.logger.debug(f"A sidepot was created")
    
    def fill_current_pot(self, lowest_player):
        self.logger.debug(f"Fill the current pot")
        lowest_bet = lowest_player.total_bet_betting_round
        current_pot = self.table.pots[-1]
        # reset the participants
        current_pot.players = []
        # you HAVE TO use players here, as you can still get some of your big blind back if the person you beat has less chips than that.
        for player in self.table.players:
            # fill up current pot with folds
            if player.total_bet_betting_round < lowest_bet and player.folded == True:
                current_pot.amount += player.total_bet_betting_round
                player.total_bet_betting_round = 0
                self.logger.debug(f"{player.name} folded as {player.total_bet_betting_round} < {lowest_bet}")
                self.table.players_game.remove(player)
                self.logger.debug(f"player removed, left are {self.table.players_game}")
                if len(self.table.players_game) < 2:
                    break
                self.logger.debug(f"{player.name} bet is down to {player.total_bet_betting_round}")
            # and with calls
            else:
                current_pot.amount += player.total_bet_betting_round
                player.total_bet_betting_round -= lowest_bet
                self.logger.debug(f"{player.name} bet is down to {player.total_bet_betting_round}")
                # add them to the list if they call...
                # exceptional situation. p1 BB 200 , p2 all in 120, p3 raise 400, p1 folds, but cannot distinguish. Need a fold indicator!
                if player.folded == False:
                    current_pot.players.append(player)
        # side_pot.players.append(player)
        # self.table.pots.append(side_pot)
    
    def pay_winners(self):
        for pot in self.table.pots:
            last_pot = self.table.pots[-1]
            winner_list = self.determine_winners(last_pot.players)
            bounty = last_pot.amount / len(winner_list)
            for winner in winner_list:
                self.logger.debug(f"{winner.name} gets {bounty} chips")
                winner.chips.win(bounty)
            self.logger.debug(f"Removing {self.table.pots.pop()}, so {len(self.table.pots)} pots left")





    # def pay_winners(self):
    #     # print('-------------------------------------')
    #     pot = sum(player.total_bet_game for player in self.table.players)
    #     # for player in self.table.players:
    #         # print(player.name, player.total_bet_game)
    #     for player in self.table.players_game:
    #         print('-------------------------------------')
    #         pot = self.devide_pot(pot)
    #         if pot != 0:
    #             self.logger.debug(f"The side pot has been payed, in the pot remains {pot}")
    #             self.devide_pot(pot)
    #         else:
    #             self.logger.debug(f"All the money has been payed")
    #             print()
    #             print()
    #             break
    #     # Award the pot to the winner(s)
        
    #     # side pot

    #     # can't bet more than you have.

    # def devide_pot(self, pot):
    #     winner_list = self.determine_winners()
    #     self.logger.debug(f"1. we have the following winners {winner_list}.")
    #     avg_bet = pot/len(self.table.players_game)
    #     self.logger.debug(f"2. That betted on average {avg_bet}.")
    #     # get the person with the lowest amount and see if he went all in
    #     lowest_better = min(winner_list, key=lambda winner: winner.total_bet_game)
    #     self.logger.debug(f"3. lowest better was {lowest_better.name}.")

    #     # not sure if relevant yet, but produces error if not works so that is handy
    #     if lowest_better.chips.amount == 0:
    #         main_pot = lowest_better.total_bet_game*len(self.table.players_game)
    #         self.logger.debug(f"Looks like {lowest_better.name} went all-in and deserves {main_pot} chips!")
    #         # TODO case when equal and both have equal hands
        
    #     if lowest_better.total_bet_game < avg_bet:
    #         self.logger.debug(f"we have a side pot of {main_pot}.")
    #         for winner in winner_list:
    #             share = main_pot/len(winner_list)
    #             winner.chips.win(share)
    #         for player in self.table.players:
    #             self.logger.debug(f"{player.name} has {player.chips.amount} left")
    #         self.logger.debug(f"Looks like {lowest_better.name} went all-in and deserves {main_pot} chips!")
    #         return pot - main_pot
    #     else:
    #         self.logger.debug(f"the pot can be devided.")
    #         for winner in winner_list:
    #             share = pot/len(winner_list)
    #             winner.chips.win(share)
    #             for player in self.table.players:
    #                 self.logger.debug(f"{player.name} has {player.chips.amount} left")
    #         return 0

    def determine_winners(self, pot_players):
        # Determine the best hand for each player
        # dict_example = {}
        winner_list = []
        for player in pot_players:
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

    def clean_up(self):
        # print(f'cleaning time{self.table.players}')
        # reset game --> needs to be refactored
        for player in self.table.players:
            print(f'player {player.name} has {player.chips.amount} chips')
            player.total_bet_game = 0
        # Create a new list that only includes the players you want to keep
        self.table.players = [player for player in self.table.players if player.chips.amount > 0]
        if len(self.table.players) == 1:
            print(f'THE WINNER IS {self.table.players[0].name}')
            return None
        # move dealer button --> needs to be refactored
        else:
            self.table.change_dealer_and_blinds()


    def is_royal_or_straight_flush(self, sorted_hand):
        # print(f"3. {id(sorted_hand)} {sorted_hand}")
        self.logger.debug("Checking for Royal and/or Straight Flush...")
        for the_suit in ['♠','♥','♦','♣']:
            # omdat als ie nou een niet suited eentje naar beneden gaat? Dat sluit nu nog niks uit...
            suited_list = []
            for hand in sorted_hand:
                if hand.suit == the_suit:
                    suited_list.append(hand)
            # print(f'suited list {suited_list}')
            straight_suited_counter = 0
            if len(suited_list) != 0:
                if suited_list[0].rank == 'A':
                    # self.logger.debug(f'Found an ace')
                    # USE + instead of .append as this doesn't mutate the original list.
                    suited_list + [Card(rank='1', suit=the_suit)]
            # self.logger.debug(f'New list: {suited_list}')
            for i in range(len(suited_list)-1):
                if self.card_rank_value(suited_list[i].rank) == self.card_rank_value(suited_list[i+1].rank) + 1:
                    print(f'******* {self.card_rank_value(suited_list[i].rank)} = {self.card_rank_value(suited_list[i+1].rank) + 1}')
                    straight_suited_counter += 1
                    if straight_suited_counter == 4:
                        self.logger.debug(f"Straight Flush was Found with suit {the_suit}!!")
                        handscore = [8, suited_list[i - 3].rank, None, None, None, None]
                        if sorted_hand[i].rank == 'A':
                            self.logger.debug('... a Royal one!!!')
                        return handscore
                elif self.card_rank_value(suited_list[i].rank) - self.card_rank_value(suited_list[i+1].rank) > 2:
                    # print("too big of a gap")
                    straight_suited_counter = 0 
                    
            self.logger.debug("No straight flush was Found.")
            return False           

    def is_four_of_a_kind(self, sorted_hand):
        self.logger.debug("Checking for Four of a Kind...")
        for i in range(len(sorted_hand) - 3):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank == sorted_hand[i + 2].rank == sorted_hand[i + 3].rank:
                self.logger.debug("Four of a Kind found!")
                quads_rank = sorted_hand[i].rank
                # it is OK to change this list as we are sure that it is four of a kind at this point
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                self.logger.debug(f"rest is now {sorted_hand}")
                return [7, quads_rank, sorted_hand[0].rank, None, None, None]
        self.logger.debug("No Four of a Kind.")
        return False


    def is_full_house(self, sorted_hand):
        self.logger.debug("Checking for Full House...")
        first_handscore = self.is_three_of_a_kind(sorted_hand)
        if first_handscore != False:
            self.logger.debug("Checking for another Pair...")
            for i in range(len(sorted_hand) - 1):
                if sorted_hand[i].rank == sorted_hand[i + 1].rank and sorted_hand[i].rank != first_handscore[1]:
                    self.logger.debug("Found a full house!")
                    return [6, first_handscore[1], sorted_hand[i].rank, None, None, None]
        self.logger.debug(f"No Full House")
        return False


    def is_flush(self, sorted_hand):
        self.logger.debug("Checking for Flush...")
        handscore = [5]
        for suit in ['♠','♥','♦','♣']:
            for card in sorted_hand:
                if card.suit == suit:
                    handscore.append(card.rank)
                    if len(handscore) == 6:
                        self.logger.debug("Flush was Found!")
                        return handscore
            handscore = [5]
        return False


    def is_straight(self, sorted_hand):
        self.logger.debug("Checking for Straight...")
        
        # as there are nog 8 cards with the extra Ace possibility, needs different solving for straight flush
        straight_counter = 0
        if sorted_hand[0].rank == 'A':
            # self.logger.debug(f'Found an ace')
            ace_suit = sorted_hand[0].suit
            # self.logger.debug(f'old list: {sorted_hand}')
            sorted_hand.append(Card(rank='1', suit=ace_suit))
            # self.logger.debug(f'New list: {sorted_hand}')
        for i in range(len(sorted_hand)-1):
            # just an extra card for each ace
            # print("----", self.card_rank_value(sorted_hand[i].rank))
            if self.card_rank_value(sorted_hand[i].rank) == self.card_rank_value(sorted_hand[i+1].rank) + 1:
                # print("==", self.card_rank_value(sorted_hand[i+1].rank) + 1, straight_counter)
                straight_counter += 1
                if straight_counter == 4:
                    self.logger.debug("Straight was Found!")
                    handscore = [4, sorted_hand[i-3].rank, None, None, None, None]
                    return handscore

            else: #self.card_rank_value(sorted_hand[i].rank) - self.card_rank_value(sorted_hand[i+1].rank) > 2:
                # print(f'{self.card_rank_value(sorted_hand[i+1].rank)} too big')
                straight_counter = 0

        self.logger.debug("No straight found!")
        return False

    def is_three_of_a_kind(self, sorted_hand):
        # print(f"-------------{sorted_hand}")
        self.logger.debug("Checking for Three of a Kind...")
        for i in range(len(sorted_hand) - 2):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank == sorted_hand[i + 2].rank:
                self.logger.debug("Three of a Kind found!")
                trips_rank = sorted_hand[i].rank
                # we need to make sure this is mutable as this gets called by is_full_house
                sorted_hand = sorted_hand.copy()
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                self.logger.debug(f"rest is now {sorted_hand}")
                return [3, trips_rank, sorted_hand[0].rank, sorted_hand[1].rank, None, None]
        self.logger.debug("No Three of a Kind.")
        return False

    def is_two_pair(self, sorted_hand):
        # we need to make sure this is mutable as this gets called by is_full_house
        sorted_hand = sorted_hand.copy()
        self.logger.debug("Checking for Two Pair...")
        pairs = 0
        for i in range(len(sorted_hand) - 3):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank and pairs == 0:
                self.logger.debug("First pair found...")

                # remove the two cards to easily access the kickers                
                first_pair_rank = sorted_hand[i].rank
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                self.logger.debug(f"rest is now {sorted_hand}")

                pairs += 1
            if sorted_hand[i].rank == sorted_hand[i + 1].rank and pairs == 1:
                self.logger.debug("Two pair found!")
                second_pair_rank = sorted_hand[i].rank
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                # self.logger.debug(f"rest is now {sorted_hand}")
                handscore = [2, first_pair_rank, second_pair_rank, sorted_hand[0].rank, None, None]
                return handscore
            # fill the rest with first, second and third kicker
        self.logger.debug(f"No two Pair!")
        return False
    
    def is_one_pair(self, sorted_hand):
        self.logger.debug("Checking for One Pair...")
        for i in range(len(sorted_hand) - 1):
            if sorted_hand[i].rank == sorted_hand[i + 1].rank:
                self.logger.debug("One Pair found!")

                # remove the two cards to easily access the kickers
                pair_rank = sorted_hand[i].rank
                sorted_hand.remove(sorted_hand[i])
                sorted_hand.remove(sorted_hand[i])
                # self.logger.debug(f"7-2={sorted_hand}")
                
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
        # hier wordt een kopietje gemaakt omdat ie anders de orginele list pakt
        # print(f"1.        {id(sorted_hand)} {sorted_hand}")
        sorted_hand = sorted_hand.copy()
        # print(f"2.        {id(sorted_hand)} {sorted_hand}")
        hand_rank = self.is_royal_or_straight_flush(sorted_hand)
        # print(f"4.        {id(sorted_hand)} {sorted_hand}")
        if hand_rank == False:
            hand_rank = self.is_four_of_a_kind(sorted_hand)
        # print(f"5.        {id(sorted_hand)} {sorted_hand}")
        if hand_rank == False:
            hand_rank = self.is_full_house(sorted_hand)
        if hand_rank == False:
            hand_rank = self.is_flush(sorted_hand)
        if hand_rank == False:
            hand_rank = self.is_straight(sorted_hand)
        if hand_rank == False:
            hand_rank = self.is_three_of_a_kind(sorted_hand)
        if hand_rank == False:
            hand_rank = self.is_two_pair(sorted_hand)
        if hand_rank == False:
            hand_rank = self.is_one_pair(sorted_hand)
        if hand_rank == False:
            self.logger.debug("Return high card...")
            hand_rank = [0, sorted_hand[0].rank, sorted_hand[1].rank, sorted_hand[2].rank, sorted_hand[3].rank, sorted_hand[4].rank]
        # print(f"9.        {id(sorted_hand)} {sorted_hand}")
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