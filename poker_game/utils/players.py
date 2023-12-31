from .objects_on_table import Chips
import logging


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
        self.logger.debug(f"{self.name} gets a {card.rank} of {card.suit}.")
        self.hand.append(card)

    def show_hand(self):
        return ', '.join(map(str, self.hand))

    def set_hand(self, hand_list):
        self.hand = hand_list

    def set_best_hand(self, hand_rank):
        self.best_hand = hand_rank

    def response(self, max_total_bet_size, hand, tablecards):
        self.logger.debug(f"{self.name} must do his/her thing: the bet is {max_total_bet_size} and he/she already has {self.total_bet_betting_round} in the pot and {self.chips.amount} left.")
        # this is the function that should be shared
        
        # simple call function
        amount_to_call = max_total_bet_size - self.total_bet_betting_round
        amount_to_bet = self.bet(amount_to_call, hand, tablecards)
        return(amount_to_bet)
    
    # standard bet is 10, override below
    def bet(self, betsize, hand, tablecards):
        self.logger.debug(f"The standard parent class is called, no modification has been done.")
        print("The standard parent class is called, no modification has been done")
        # do this in game so that errors in modification don't mess this up
        # self.chips.lose(10)
        return betsize

## decorators which people can fill in <-- other option would be to directly change the child class.
def aggressive_player_decorator(player_class):
    class AggressivePlayer(player_class):
        def bet(self, betsize, hand, table):
            self.logger.debug(f"Aggressive players go all in at first chance")
            return 100
        # Additional methods or overrides can go here
    return AggressivePlayer

def conservative_player_decorator(player_class):
    class ConservativePlayer(player_class):
        def bet(self, betsize, hand, table):
            self.logger.debug(f"Conservative players only call")
            return betsize
        # Additional methods or overrides can go here
    return ConservativePlayer

def raises_with_aces_reduces_with_12345_decorator(player_class):
    class Raises_with_aces_reduces_with_12345Player(player_class):
        def bet(self, betsize, hand, table):
            self.logger.debug(f"I am an Ace Raiser!")
            for card in hand:
                if card.suit == 'A':
                    betsize = betsize * 2 
                    print("Ace is raise!")
                elif card.suit in '12345':
                    print("that is a low card!")
                    betsize = betsize / 2
                else:
                    print('that is an average card!')
            return betsize
        # Additional methods or overrides can go here
    return Raises_with_aces_reduces_with_12345Player

# Instantiate a player with a specific playing style
def create_player(name, style):
    if style == 'aggressive':
        DecoratedPlayer = aggressive_player_decorator(ActualPlayerTemplate)
    elif style == 'conservative':
        DecoratedPlayer = conservative_player_decorator(ActualPlayerTemplate)
    elif style == 'raises_with_aces_reduces_with_12345':
        DecoratedPlayer = raises_with_aces_reduces_with_12345_decorator(ActualPlayerTemplate)
    else:
        DecoratedPlayer = ActualPlayerTemplate  # No decoration

    return DecoratedPlayer(name)

    # class DecoratedPlayer(player_class):
    #     def __init__(self, name):
    #         # Call the constructor of the base class (Player or ActualPlayer)
    #         super().__init__(name)
    #         # Add or override attributes/methods specific to the decorated player
    #         self.decorated_attribute = "Decorated Attribute"

    #     def decorated_method(self):
    #         print(f"{self.name} performs a decorated action.")

    #     def bet(self, betsize=None):
    #         # Override the bet method to set the bet size to 100
    #         return 100

    return DecoratedPlayer

# The child class, which will function as a template.
class ActualPlayerTemplate(Player):
    def __init__(self, name, chips = None):
        # Call the constructor of the base class (Player)
        super().__init__(name, chips)
        # Add or override attributes specific to the Player
        self.advanced_attribute = "Advanced Attribute"

    # Standard bet is 10, you could (and should) override it here
    def bet(self, betsize):
        betsize = 20
        # self.bet(betsize)
        return betsize
        # OR make it more complex:
        # bet_to_make_pot_20()
    # A more complex function can be added:
    
    # def bet_to_make_pot_20(self, previous_bet, pot, players):
    #     self.logger.debug(f"{self.name} has to decide what to do.")
    #     if pot < 20 and self.hand != [Card('2', '♠'), Card('7', '♥')]:
    #         self.logger.debug(f"{self.name} says: let's make that pot 20!")
    #         self.bet((20-pot)/players)

def create_player(name, style, chips=Chips(100)):
    if style == 'aggressive':
        DecoratedPlayer = aggressive_player_decorator(ActualPlayerTemplate)
    elif style == 'conservative':
        DecoratedPlayer = conservative_player_decorator(ActualPlayerTemplate)
    elif style == 'raises_with_aces_reduces_with_12345':
        DecoratedPlayer = raises_with_aces_reduces_with_12345_decorator(ActualPlayerTemplate)
    else:
        DecoratedPlayer = ActualPlayerTemplate  # No decoration

    return DecoratedPlayer(name, chips)