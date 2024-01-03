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
        for game_seed in range(game_seed, game_seed+80):
            table = Table()

            player1 = create_player("Grietje", 'raises_with_aces_reduces_with_12345', Chips(100))
            player2 = create_player("Jan", 'raises_with_aces_reduces_with_12345', Chips(100))
            player3 = create_player("Martin", 'conservative', Chips(100))
            
            table.add_player(player1)
            table.add_player(player2)
            table.add_player(player3)
            
            expected_sum = sum([player.chips.amount for player in table.players])

            result, rounds = play_game(seed=game_seed, table=table)
            nr_of_rounds += rounds
            logger.info(f"Total nr of rounds: {nr_of_rounds}")

            self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)


if __name__ == '__main__':
    unittest.main()