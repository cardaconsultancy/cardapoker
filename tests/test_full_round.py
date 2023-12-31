import unittest
from poker_game.utils.players import create_player
from poker_game.utils.start_round import start_round
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
import logging

logger = logging.getLogger(__name__)

class TestTexasHoldemGame(unittest.TestCase):
    def test_play_round(self):
        round_seed = 1
        for round_seed in range(round_seed, 30):
            table = Table()

            player1 = create_player("Grietje", 'raises_with_aces_reduces_with_12345', Chips(100))
            player2 = create_player("Jan", 'conservative', Chips(100))
            player3 = create_player("Martin", 'conservative', Chips(100))
            
            table.add_player(player1)
            table.add_player(player2)
            table.add_player(player3)

            expected_sum = sum([player.chips.amount for player in table.players])

            result = start_round(seed=round_seed, table=table)
            logger.debug(f"round seed: {round_seed}")
            self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

if __name__ == '__main__':
    unittest.main()