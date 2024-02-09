from poker_game.utils.evaluate_hand import evaluate_hand, get_hand_rank
# from .objects_on_table import Chips
import logging
from openai_client.test_openai import client 

class Player:
    def __init__(self, name, chips):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.hand = []
        self.chips = chips if chips else Chips()
        self.best_hand = []
        self.total_bet_betting_round = 0
        self.total_in_pots_this_game = 0
        self.total_bet = 0
        self.hand_score = [0, 0, 0, 0, 0, 0]
        self.raised_called_or_checked_this_round = False
        self.folded = False
        self.all_in = False

    def receive_card(self, card):
        #self.logger.debug(f"{self.name} gets a {card.rank} of {card.suit}.")
        self.hand.append(card)

    def show_hand(self):
        return ', '.join(map(str, self.hand))

    def set_hand(self, hand_list):
        self.hand = hand_list

    def set_best_hand(self, hand_rank):
        self.best_hand = hand_rank

    def response(self, max_total_bet_size, hand, table):
        #self.logger.debug(f"{self.name} must do his/her thing: the bet is {max_total_bet_size} and he/she already has {self.total_bet_betting_round} in the pot and {self.chips.amount} left.")
        # this is the function that should be shared
        
        # simple call function
        amount_to_call = max_total_bet_size - self.total_bet_betting_round
        amount_to_bet = self.bet(amount_to_call, hand, table)
        return(amount_to_bet)
    
    # standard bet is 10, override below
    def bet(self, betsize):
        #self.logger.debug(f"The standard parent class is called, no modification has been done.")
        print("The standard parent class is called, no modification has been done")
        # do this in game so that errors in modification don't mess this up
        # self.chips.lose(10)
        return betsize 

#########################################################################################

## decorators which people can fill in <-- other option would be to directly change the child class.
def aggressive_player_decorator(player_class):
    class AggressivePlayer(player_class):
        def bet(self, betsize, hand, table):
            #self.logger.debug(f"Aggressive players go big at first chance")
            return 10
        # Additional methods or overrides can go here
    return AggressivePlayer

def super_aggressive_player_decorator(player_class):
    class SuperAggressivePlayer(player_class):
        def bet(self, betsize, hand, table):
            #self.logger.debug(f"Aggressive players go big at first chance")
            return 100
        # Additional methods or overrides can go here
    return SuperAggressivePlayer

def conservative_player_decorator(player_class):
    class ConservativePlayer(player_class):
        def bet(self, betsize, hand, table):
            #self.logger.debug(f"Conservative players only call")
            return betsize
        # Additional methods or overrides can go here
    return ConservativePlayer

def always_fold_player_decorator(player_class):
    class AlwaysFoldPlayer(player_class):
        def bet(self, betsize, hand, table):
            #self.logger.debug(f"folding is all I do")
            return 0
        # Additional methods or overrides can go here
    return AlwaysFoldPlayer

def raises_with_aces_reduces_with_12345_decorator(player_class):
    class Raises_with_aces_reduces_with_12345Player(player_class):
        def bet(self, betsize, hand, table):
            #self.logger.debug(f"I am an Ace Raiser!")
            for card in hand:
                if card.suit == 'A':
                    betsize = betsize * 2 
                    # print("Ace is raise!")
                elif card.suit in '12345':
                    # print("that is a low card!")
                    betsize = betsize / 2
                # else:
                #     print('that is an average card!')
            return betsize
        # Additional methods or overrides can go here
    return Raises_with_aces_reduces_with_12345Player

def careful_calculator_decorator(player_class):
    class careful_calculator_Player(player_class):
        def bet(self, betsize, hand, table):
            #self.logger.debug(f"I am an Ace Raiser!")
            # if flop:
            if len(table.community_cards) >= 3:
                rank = get_hand_rank(self, table)
                if rank[0] > 4:
                    # raise if raising, limp if not
                    betsize = betsize * 3
                if 2 <= rank[0] <= 4:
                    # raise
                    betsize = betsize * 2 + 20
            # if before flop: 
            else:    
                for card in hand:
                    if card.suit == 'A':
                        betsize = betsize * 2 
                        # print("Ace is raise!")
                    elif card.suit in '12345':
                        # print("that is a low card!")
                        betsize = betsize / 2
                    # else:
                    #     print('that is an average card!')
                return betsize
            return betsize
        # Additional methods or overrides can go here
    return careful_calculator_Player


def chatgpt35_decorator(player_class):
    class chatgpt35(player_class):
        def bet(self, betsize, hand, table):

            table.players 

            prompt = "6 players. Nr chips per person: 1000"\
            "You are the fouth player after the dealer."\
            "First round. You get a jack of hearts and a queen of hearts."\
            "Player 2 small blind: 1 chip. Player 3 big blind: 2 chips."\
            "Your turn. What do you do? Pick one option."

            chat_completion = client.chat.completions.create(
                messages = [
                    {
                        "role":"user",
                        "content": prompt
                    }
                ],
                model="gpt-3.5-turbo"
            )
            print(chat_completion)
        # Additional methods or overrides can go here
    return chatgpt35


#########################################################################################


# Instantiate a player with a specific playing style
def create_player(name, style):
    if style == 'aggressive':
        DecoratedPlayer = aggressive_player_decorator(ActualPlayerTemplate)
    elif style == 'super aggressive':
        DecoratedPlayer = conservative_player_decorator(ActualPlayerTemplate)
    elif style == 'conservative':
        DecoratedPlayer = conservative_player_decorator(ActualPlayerTemplate)
    elif style == 'raises_with_aces_reduces_with_12345':
        DecoratedPlayer = raises_with_aces_reduces_with_12345_decorator(ActualPlayerTemplate)
    else:
        DecoratedPlayer = ActualPlayerTemplate  # No decoration

    return DecoratedPlayer(name)

# The child class, which will function as a template.
class ActualPlayerTemplate(Player):
    def __init__(self, name, chips = None):
        # Call the constructor of the base class (Player)
        super().__init__(name, chips)
        # Add or override attributes specific to the Player
        self.advanced_attribute = "Advanced Attribute"

    # Standard bet is 10, you could (and should) override it here
    def bet(self, betsize, hand, tablecards):
        betsize = 20
        # self.bet(betsize)
        return betsize
        # OR make it more complex:
        # bet_to_make_pot_20()
    # A more complex function can be added: 
    
    # def bet_to_make_pot_20(self, previous_bet, pot, players):
    #     #self.logger.debug(f"{self.name} has to decide what to do.")
    #     if pot < 20 and self.hand != [Card('2', '♠'), Card('7', '♥')]:
    #         #self.logger.debug(f"{self.name} says: let's make that pot 20!")
    #         self.bet((20-pot)/players) 

def create_player(name, style, chips=Chips(100)):
    if style == 'aggressive':
        DecoratedPlayer = aggressive_player_decorator(ActualPlayerTemplate)
    elif style == 'super aggressive':
        DecoratedPlayer = super_aggressive_player_decorator(ActualPlayerTemplate)
    elif style == 'conservative':
        DecoratedPlayer = conservative_player_decorator(ActualPlayerTemplate)
    elif style == 'careful calculator':
        DecoratedPlayer = careful_calculator_decorator(ActualPlayerTemplate)
    elif style == 'always fold':
        DecoratedPlayer = always_fold_player_decorator(ActualPlayerTemplate)
    elif style == 'raises with aces reduces with 12345':
        DecoratedPlayer = raises_with_aces_reduces_with_12345_decorator(ActualPlayerTemplate)
    else:
        DecoratedPlayer = ActualPlayerTemplate  # No decoration 

    return DecoratedPlayer(name, chips)