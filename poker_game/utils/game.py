# TODO: when BB has not enough chips, the other players should be calling the BB and not his max bet
from .betting_round import betting_round
from .objects_on_table import Pot, Deck
from .clean_up import clean_up
import logging
from operator import attrgetter
from collections import deque
from .next_player import get_next_player
from .pot_management import create_pots, check_if_rest_folded_and_pay
from .get_and_pay_winners import pay_winners

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
        self.logger.debug(f"the dealer is {self.table.dealer}.")

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
        betting_round(self.table, preflop_round=True)
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
            betting_round(self.table)
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
            betting_round(self.table)
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
            betting_round(self.table)
            self.logger.debug(f"Total is {sum(player.total_in_pots_this_game for player in self.table.players)}.")
        
        if check_if_rest_folded_and_pay(self.table):
            return True
        
        # Determine the winner(s)
        self.logger.debug(f"Pay_the_winner(s)")
        pay_winners(self.table)

        # Clean up
        clean_up(self.table)

        return True