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

    def __init__(self, table, deck):
        self.table = table