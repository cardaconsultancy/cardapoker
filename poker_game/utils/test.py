import logging

# A file handler for info level and higher
file_handler = logging.FileHandler('my_log.log')
file_handler.setLevel(logging.INFO)
logging.basicConfig(level=logging.INFO)


# A formatter and add it to the handlers
formatter = logging.Formatter('%(message)s')

# console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add the handlers to the logger
# logger.addHandler(console_handler)
logger = logging.getLogger('test')
logger.addHandler(file_handler)

import time

def start_round(table, test_cards=None, seed=None):
    # log new game

    logger.info(f"this doesn't get logged")
    logger.info(f"this doesn't get logged")
    print('1')
    logger.debug("2^10")
    # reset the deck
    logger.info(f"this doesn't get logged")
    # deck = Deck(seed=seed)
    print('2')
    logger.info(f"this doesn't get logged")

start_round('bla')

class Deck:
    """A standard deck of playing cards."""

    ranks = '23456789TJQKA'
    suits = '♠♥♦♣'

    def __init__(self, seed=None):
        """Initialize a deck of cards and shuffle it.

        Args:
            seed (int, optional): Seed for random number generator. Defaults to None.
        """
        self.logger = logging.getLogger('test')
        # self.cards = ['bla']

        # random.seed(seed)  # Set the random seed
        # random.shuffle(self.cards)
        # # self.dealt_cards = collections.deque()
        logging.basicConfig(level=logging.INFO)
        #self.logger.debug(f"A new deck with {len(self.cards)} cards.")

def start_round2(table, test_cards=None, seed=None):
    # log new game

    logger.info(f"this doesn't get logged")
    logger.info(f"this doesn't get logged")
    print('3')
    logger.debug("2^10")
    # reset the deck
    logger.info(f"this doesn't get logged")
    deck = Deck(seed=seed)
    print('4')
    logger.info(f"this gets logged")

start_round2('bla')