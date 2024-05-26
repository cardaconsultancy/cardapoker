"""
These tests allow for randomness, but they are limited so that they can be tested... sort of. 
"""

import unittest
from poker_game.utils.players import create_player
from poker_game.utils.play_round import play_round
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.logging_config import setup_logging
import logging

setup_logging(logging_mode=True)

logger = logging.getLogger("poker_game")

test_one = True


class TestTexasHoldemGame(unittest.TestCase):
    if test_one:

        def test_devision_by_zero(self):
            table = Table()
            table.blind_size = 1
            always_fold_A = create_player("always_fold_A", "always_fold", Chips(100))
            aggressive_B = create_player("aggressive_B", "aggressive", Chips(99))
            careful_calculator_C = create_player(
                "careful_calculator_C", "careful_calculator", Chips(4)
            )
            completely_random_D = create_player(
                "completely_random_D", "completely_random", Chips(197)
            )
            aggressive_E = create_player("aggressive_E", "aggressive", Chips(100))
            always_fold_F = create_player("always_fold_F", "always_fold", Chips(100))
            always_fold_A.hand = [Card("7", "♥"), Card("2", "♥")]
            aggressive_B.hand = [Card("2", "♠"), Card("8", "♠")]
            careful_calculator_C.hand = [Card("J", "♣"), Card("5", "♥")]
            completely_random_D.hand = [Card("7", "♣"), Card("4", "♣")]
            aggressive_E.hand = [Card("K", "♥"), Card("K", "♠")]
            always_fold_F.hand = [Card("2", "♦"), Card("3", "♦")]
            table.add_player(careful_calculator_C)
            table.add_player(completely_random_D)
            table.add_player(aggressive_E)
            table.add_player(always_fold_F)
            table.add_player(always_fold_A)
            table.add_player(aggressive_B)
            test_cards = [
                Card("Q", "♣"),
                Card("7", "♦"),
                Card("6", "♥"),
                Card("K", "♦"),
                Card("4", "♥"),
            ]
            play_round(table=table, test_cards=test_cards)

    # test all the other test cases
    else:

        def folding_must_lead_to_exclusion(self):
            table = Table()
            table.blind_size = 1
            always_fold_A = create_player("always_fold_A", "always_fold", Chips(100))
            aggressive_B = create_player("aggressive_B", "aggressive", Chips(99))
            careful_calculator_C = create_player(
                "careful_calculator_C", "careful_calculator", Chips(4)
            )
            completely_random_D = create_player(
                "completely_random_D", "completely_random", Chips(197)
            )
            aggressive_E = create_player("aggressive_E", "aggressive", Chips(100))
            always_fold_F = create_player("always_fold_F", "always_fold", Chips(100))
            always_fold_A.hand = [Card("7", "♥"), Card("2", "♥")]
            aggressive_B.hand = [Card("2", "♠"), Card("8", "♠")]
            careful_calculator_C.hand = [Card("J", "♣"), Card("5", "♥")]
            completely_random_D.hand = [Card("7", "♣"), Card("4", "♣")]
            aggressive_E.hand = [Card("K", "♥"), Card("K", "♠")]
            always_fold_F.hand = [Card("2", "♦"), Card("3", "♦")]
            table.add_player(careful_calculator_C)
            table.add_player(completely_random_D)
            table.add_player(aggressive_E)
            table.add_player(always_fold_F)
            table.add_player(always_fold_A)
            table.add_player(aggressive_B)
            test_cards = [
                Card("Q", "♣"),
                Card("7", "♦"),
                Card("6", "♥"),
                Card("K", "♦"),
                Card("4", "♥"),
            ]
            play_round(table=table, test_cards=test_cards)


if __name__ == "__main__":
    unittest.main()
