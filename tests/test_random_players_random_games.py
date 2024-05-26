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
import random

setup_logging(logging_mode='CRITICAL')
logger = logging.getLogger('poker_game')
logger_analytics = logging.getLogger('poker_game_analytics')

class TestTexasHoldemGame(unittest.TestCase):
    def test_random_players_random_games(self):
        # test how long this test takes
        start = datetime.datetime.now()
        winnerlist = []
        role_list = ['raises_with_aces_reduces_with_12345', 'conservative', 'careful_calculator', 'aggressive', 'always_fold', 'super_aggressive', 'completely_random']
        length_of_role_list = len(role_list)-1
        for game in range(0, 10): 
            # get the game number
            logger.info(f"Game NR {game}")
            
            # create names here to make sure that we can identify the player style
            A_role = role_list[random.randint(0,length_of_role_list)]
            B_role = role_list[random.randint(0,length_of_role_list)]
            C_role = role_list[random.randint(0,length_of_role_list)]
            D_role = role_list[random.randint(0,length_of_role_list)]
            E_role = role_list[random.randint(0,length_of_role_list)]
            F_role = role_list[random.randint(0,length_of_role_list)]
            
            table = Table()
            A = create_player(A_role + '_A', A_role, Chips(100))
            B = create_player(B_role + "_B", B_role, Chips(100))
            C = create_player(C_role + "_C", C_role, Chips(100))
            D = create_player(D_role + "_D", D_role, Chips(100))
            E = create_player(E_role + "_E", E_role, Chips(100))
            F = create_player(F_role + "_F", F_role, Chips(100))
            
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
        logger_analytics.info(f"Winnerlist: {Counter(winnerlist)}")
        end = datetime.datetime.now()
        logger.info(f"Time taken: {end-start}")


if __name__ == '__main__': 
    unittest.main()