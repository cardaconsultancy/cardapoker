import unittest
from poker_game.play_game import play_game
from poker_game.utils.players import Player, ActualPlayerTemplate, create_player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card
from poker_game.utils.game import TexasHoldemGame
import logging

logger = logging.getLogger(__name__)
class TestTexasHoldemGame(unittest.TestCase):
    def test_play_round(self):
        nr_of_rounds = 0
        game_seed = 100
        winnerdict = {}
        for game_seed in range(game_seed, game_seed+20):
            table = Table()

            player1 = create_player("A", 'raises_with_aces_reduces_with_12345', Chips(100))
            player2 = create_player("B", 'conservative', Chips(100))
            player3 = create_player("C", 'conservative', Chips(100))
            player4 = create_player("D", 'careful_calculator', Chips(100))
            player5 = create_player("E", 'aggressive', Chips(100))
            player6 = create_player("F", 'always_fold', Chips(100))
            
            table.add_player(player1)
            table.add_player(player2)
            table.add_player(player3)
            table.add_player(player4)
            table.add_player(player5)
            table.add_player(player6)
            
            expected_sum = sum([player.chips.amount for player in table.players])

            result_table, rounds = play_game(seed=game_seed, table=table)
            nr_of_rounds += rounds
            logger.info(f"Total  nr of rounds: {nr_of_rounds}")

            self.assertEqual(sum([player.chips.amount for player in result_table.players]), expected_sum)


if __name__ == '__main__': 
    unittest.main()