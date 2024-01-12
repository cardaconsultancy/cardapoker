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
        winnerlist = []
        for game in range(1, 100):
            table = Table()
            player1 = create_player("A", 'raises with aces reduces with 12345', Chips(100))
            player2 = create_player("B", 'conservative', Chips(100))
            player3 = create_player("C", 'conservative', Chips(100))
            player4 = create_player("D", 'careful calculator', Chips(100))
            player5 = create_player("E", 'aggressive', Chips(100))
            player6 = create_player("F", 'always fold', Chips(100))
            
            table.add_player(player1)
            table.add_player(player2)
            table.add_player(player3)
            table.add_player(player4)
            table.add_player(player5)
            table.add_player(player6)
            
            expected_sum = sum([player.chips.amount for player in table.players])

            winner, rounds = play_game(table=table)
            winnerlist.append(winner)
            logger.info(f"Winner of game {game} is {winner} after {rounds} rounds!")
        winnerlist.values_count()
        # self.assertEqual(sum([player.chips.amount for player in result_table.players]), expected_sum)


if __name__ == '__main__': 
    unittest.main()