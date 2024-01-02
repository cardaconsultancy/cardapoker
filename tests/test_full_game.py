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
        game_seed = 100
        for game_seed in range(game_seed, game_seed+20):
            table = Table()

            player1 = create_player("Grietje", 'raises_with_aces_reduces_with_12345', Chips(100))
            player2 = create_player("Jan", 'aggressive', Chips(100))
            player3 = create_player("Martin", 'conservative', Chips(100))
            
            table.add_player(player1)
            table.add_player(player2)
            table.add_player(player3)
            
            expected_sum = sum([player.chips.amount for player in table.players])

            result = play_game(seed=game_seed, table=table)
            logger.debug(f"round seed: {game_seed}")
            self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)


if __name__ == '__main__':
    unittest.main()