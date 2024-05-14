import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('test')


def start_round(table, test_cards=None, seed=None):
    # log new game
    logger.debug(f"this doesn't get logged")
    logger.info(f"this doesn't get logged")
    print('1')
    logger.info(f"this doesn't get logged")
    print('2')
    logger.info(f"this doesn't get logged")

start_round('bla')

class Deck:
    """A standard deck of playing cards."""

    ranks = '23456789TJQKA'
    suits = '♠♥♦♣'

    def __init__(self, seed=None):
        logging.basicConfig(level=logging.DEBUG)

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