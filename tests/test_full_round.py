import unittest
from poker_game.utils.players import create_player
from poker_game.utils.start_round import start_round
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame

class TestTexasHoldemGame(unittest.TestCase):
    def test_play_round(self):
        deck = Deck(seed=1)
        table = Table()
        # game = TexasHoldemGame(table, deck)

        player1 = create_player("Grietje", 'raises_with_aces_reduces_with_12345', Chips(100))
        player2 = create_player("Jan", 'conservative', Chips(100))
        player3 = create_player("Martin", 'conservative', Chips(100))
        
        table.add_player(player1)
        table.add_player(player2)
        table.add_player(player3)

        start_round(seed=1, table=table)


if __name__ == '__main__':
    unittest.main()