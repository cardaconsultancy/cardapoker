from utils.objects_on_table import Chips
import logging


class Player:
    def __init__(self, name, chips):
        self.logger = logging.getLogger(__name__)
        self.name = name
        self.hand = []
        self.chips = chips if chips else Chips()
        self.best_hand = []
        self.total_bet_betting_round = 0
        self.total_bet_game = 0
        self.hand_score = [0, 0, 0, 0, 0, 0]

    def receive_card(self, card):
        self.logger.debug(f"{self.name} gets a {card.rank} of {card.suit}.")
        self.hand.append(card)

    def show_hand(self):
        return ', '.join(map(str, self.hand))

    def set_hand(self, hand_list):
        self.hand = hand_list

    def set_best_hand(self, hand_rank):
        self.best_hand = hand_rank

    def response(self, max_total_bet_size):
        self.logger.debug(f"{self.name} must do his/her thing: the bet is {max_total_bet_size} and he/she already has {self.total_bet_betting_round} in the pot")
        # this is the function that should be shared
        
        # simple call function
        amount_to_call = max_total_bet_size - self.total_bet_betting_round
        amount_to_bet = self.bet(amount_to_call)
        return(amount_to_bet)
    
    # standard bet is 10, override below
    def bet(self, betsize):
        # do this in game so that errors in modification don't mess this up
        # self.chips.lose(10)
        return betsize

### decorators which people can fill in

def poker_player_decorator(player_class):
    class DecoratedPlayer(player_class):
        def __init__(self, name):
            # Call the constructor of the base class (Player or ActualPlayer)
            super().__init__(name)
            # Add or override attributes/methods specific to the decorated player
            self.decorated_attribute = "Decorated Attribute"

        def decorated_method(self):
            print(f"{self.name} performs a decorated action.")

    return DecoratedPlayer

@poker_player_decorator
class ActualPlayerTemplate(Player):
    def __init__(self, name):
        # Call the constructor of the base class (Player)
        super().__init__(name)
        # Add or override attributes specific to the Player
        self.advanced_attribute = "Advanced Attribute"

    # Standard bet is 10, you could (and should) override it here
    def bet(self):
        betsize = 20
        self.bet(betsize)
        return betsize
        # OR make it more complex:
        # bet_to_make_pot_20()
    # A more complex function can be added:
    
    # def bet_to_make_pot_20(self, previous_bet, pot, players):
    #     self.logger.debug(f"{self.name} has to decide what to do.")
    #     if pot < 20 and self.hand != [Card('2', '♠'), Card('7', '♥')]:
    #         self.logger.debug(f"{self.name} says: let's make that pot 20!")
    #         self.bet((20-pot)/players)