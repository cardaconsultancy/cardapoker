import unittest
from poker_game.utils.players import Player, ActualPlayerTemplate, create_player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.pot_management import check_for_side_pots

import unittest

import unittest


class TestTexasHoldemGame(unittest.TestCase):

    # don't test if one folds as this will be checked earlier, now this will lead to an error

    def setUp(self):
        self.scenarios = [
            {
                "test": "test1",
                "player1_chips": 100,
                "player2_chips": 50,
                "player3_chips": 10,
                "player1_bet": 50,
                "player2_bet": 50,
                "player3_bet": 10,
                "player1_folded": False,
                "player2_folded": False,
                "player3_folded": False,
                "player1_all_in": False,
                "player2_all_in": True,
                "player3_all_in": True,
                "expected_pots": [30, 80],
            },
            {
                "test": "test2",
                "player1_chips": 50,
                "player2_chips": 50,
                "player3_chips": 50,
                "player1_bet": 50,
                "player2_bet": 50,
                "player3_bet": 50,
                "player1_folded": False,
                "player2_folded": False,
                "player3_folded": False,
                "player1_all_in": True,
                "player2_all_in": True,
                "player3_all_in": True,
                "expected_pots": [150],
            },
            {
                "test": "test3",
                "player1_chips": 500,
                "player2_chips": 500,
                "player3_chips": 500,
                "player1_bet": 50,
                "player2_bet": 50,
                "player3_bet": 50,
                "player1_folded": True,
                "player2_folded": False,
                "player3_folded": False,
                "player1_all_in": False,
                "player2_all_in": False,
                "player3_all_in": False,
                "expected_pots": [150],
            },
        ]

    def test_play_round(self):
        for scenario in self.scenarios:
            print("------------ ", scenario["test"], " ------------")
            with self.subTest(scenario=scenario):
                deck = Deck()
                table = Table()
                pot = Pot()

                player1 = create_player("KWIK", scenario["player1_chips"])
                player2 = create_player("KWEK", scenario["player2_chips"])
                player3 = create_player("KWAK", scenario["player3_chips"])

                player1.folded = scenario["player1_folded"]
                player2.folded = scenario["player2_folded"]
                player3.folded = scenario["player3_folded"]

                player1.all_in = scenario["player1_all_in"]
                player2.all_in = scenario["player2_all_in"]
                player3.all_in = scenario["player3_all_in"]

                player1.total_bet_betting_round = scenario["player1_bet"]
                player2.total_bet_betting_round = scenario["player2_bet"]
                player3.total_bet_betting_round = scenario["player3_bet"]

                pot.players = [player1, player2, player3]
                # pot.amount = 0

                # have to create a pot as this happens outside of this function
                table.pots.append(pot)

                table.add_player(player1)
                table.add_player(player2)
                table.add_player(player3)

                game = TexasHoldemGame(table, deck)
                check_for_side_pots(table)

                # check if all bets are reduced to zero in the end
                self.assertEqual(
                    sum([player.total_bet_betting_round for player in pot.players]), 0
                )

                # check if the pots have the same amount
                self.assertEqual(
                    [pot.amount for pot in table.pots], scenario["expected_pots"]
                )


if __name__ == "__main__":
    unittest.main()
