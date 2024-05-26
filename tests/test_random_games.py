import datetime
import unittest
from poker_game.play_game import play_game
from poker_game.utils.players import Player, ActualPlayerTemplate, create_player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.logging_config import setup_logging
import logging
from collections import Counter

setup_logging()
logger = logging.getLogger('poker_game')

class TestTexasHoldemGame(unittest.TestCase):
    def test_play_round(self):
        # test how long this test takes
        start = datetime.datetime.now()
        winnerlist = []
        for game in range(1, 1):
            # get the game number
            logger.info(f"Game NR {game}")

            table = Table()
            A = create_player("A", 'raises_with_aces_reduces_with_12345', Chips(100))
            B = create_player("B", 'conservative', Chips(100))
            C = create_player("C", 'conservative', Chips(100))
            D = create_player("D", 'careful_calculator', Chips(100))
            E = create_player("E", 'aggressive', Chips(100))
            F = create_player("F", 'always_fold', Chips(100))
            
            table.add_player(A)
            table.add_player(B)
            table.add_player(C)
            table.add_player(D)
            table.add_player(E)
            table.add_player(F)
            
            expected_sum = sum([player.chips.amount for player in table.players])

            winner, rounds = play_game(table=table)
            winnerlist.append(winner)
            logger.info(f"Winner of game {game} is {winner} after {rounds} rounds!")
        logger.info(f"Winnerlist: {Counter(winnerlist)}")
        end = datetime.datetime.now()
        logger.info(f"Time taken: {end-start}")
        


if __name__ == '__main__': 
    unittest.main()