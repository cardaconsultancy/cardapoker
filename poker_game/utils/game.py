from .betting_round import betting_round_completed
from .objects_on_table import Pot, Deck
from .clean_up import clean_up
import logging

class TexasHoldemGame:

    def __init__(self, table, deck):
        self.table = table
