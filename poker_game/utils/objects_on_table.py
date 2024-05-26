import collections
import logging
import random

Card = collections.namedtuple("Card", ["rank", "suit"])


class Chips:
    def __init__(self, amount=0):
        self.logger = logging.getLogger(__name__)
        self.amount = amount

    def win(self, amount):
        # self.logger.debug(f"{amount} chip(s) is/are awarded to the winner")
        self.amount += amount

    # create a seperate function for the rare event that a player actually gets chips back because the opposing player went all in and has less chips than the original bet.
    def give_back(self, amount):
        # self.logger.debug(f"{amount} chip(s) is/are given back")
        self.amount += amount

    def lose(self, amount):
        if amount < self.amount:
            # self.logger.debug(f"{amount} chip(s) is/are lost")
            self.amount -= amount
        else:
            # self.logger.debug("THIS PLAYER IS ALL INNNNNNNNNN!!!!!!!!!!!")
            self.amount -= self.amount
            # self.logger.debug(f"{self.amount} chips left")
            return False


class Pot:
    def __init__(self, amount=0):
        self.number = 0
        self.amount = amount
        self.players = []

    def in_pot(self, amount):
        self.amount += amount

    def out_pot(self, amount):
        self.amount -= amount


class Deck:
    """A standard deck of playing cards."""

    ranks = "23456789TJQKA"
    suits = "♠♥♦♣"

    def __init__(self, seed=None):
        """Initialize a deck of cards and shuffle it.

        Args:
            seed (int, optional): Seed for random number generator. Defaults to None.
        """
        self.logger = logging.getLogger(__name__)
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]

        random.seed(seed)  # Set the random seed
        random.shuffle(self.cards)
        logging.basicConfig(level=logging.DEBUG)

    def deal(self):
        """Deal a card from the deck."""
        dealt_card = self.cards.pop()
        return dealt_card

    def get_number_of_cards(self):
        """Get the number of cards remaining in the deck."""
        return len(self.cards)
