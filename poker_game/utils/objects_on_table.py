import collections
import logging
import random

Card = collections.namedtuple('Card', ['rank', 'suit'])

class Chips:
    def __init__(self, amount=0):
        self.logger = logging.getLogger(__name__)
        self.amount = amount

    def win(self, amount):
        self.logger.debug(f"{amount} chip(s) is/are awarded to the winner")
        self.amount += amount

    # create a seperate function for the rare event that a player actually gets chips back because the opposing player went all in and has less chips than the original bet.
    def give_back(self, amount):
        self.logger.debug(f"{amount} chip(s) is/are given back")
        self.amount += amount

    def lose(self, amount):
        if amount < self.amount:
            self.logger.debug(f"{amount} chip(s) is/are lost")
            self.amount -= amount
        else:
            self.logger.debug(f"THIS PLAYER IS ALL INNNNNNNNNN!!!!!!!!!!!")
            return False

class Pot:
    def __init__(self, amount=0):
        self.number = 0
        self.amount = amount
        self.players= []

    def in_pot(self, amount):
        self.amount += amount

    def out_pot(self, amount):
        self.amount -= amount

class Deck:
    """A standard deck of playing cards."""

    ranks = '23456789TJQKA'
    suits = '♠♥♦♣'

    def __init__(self):
        """Initialize a deck of cards and shuffle it."""
        self.logger = logging.getLogger(__name__)
        self.cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        random.shuffle(self.cards)
        self.dealt_cards = collections.deque()
        logging.basicConfig(level=logging.DEBUG)
        self.logger.debug(f"A new deck with {len(self.cards)} cards.")


    def deal(self, number_of_cards = 1):
        """Deal a card from the deck."""
        # dealt_cards = []
        # for card in range(number_of_cards):
        #     dealt_card = self.cards.pop()
        #     self.dealt_cards.append(dealt_card)
        # dealt_cards = dealt_cards.append(dealt_card)
        # return dealt_cards
        dealt_card = self.cards.pop()
        # self.logger.debug(f"A {dealt_card.rank} of {dealt_card.suit} was dealt.")
        self.dealt_cards.append(dealt_card)
        return dealt_card

    def get_number_of_cards(self):
        """Get the number of cards remaining in the deck."""
        return len(self.cards)