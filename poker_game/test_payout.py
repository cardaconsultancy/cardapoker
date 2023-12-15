import unittest
from utils.players import Player
from utils.table import Table
from utils.objects_on_table import Deck, Chips, Card
from utils.game import TexasHoldemGame

class TestTexasHoldemGame(unittest.TestCase):

    def test_game_initialization(self):
        deck = Deck()
        table = Table()
        game = TexasHoldemGame(table, deck)
        self.assertEqual(game.table, table)
        self.assertEqual(game.deck, deck)

    def test_play_round(self):
        deck = Deck()
        table = Table()
        game = TexasHoldemGame(table, deck)

        player1 = Player("Klaas", Chips(100))
        player2 = Player("Jan", Chips(100))
        player3 = Player("Piet", Chips(100))

        test = 'pair'
        community_cards = [Card(rank='3', suit='♣'), Card(rank='2', suit='♠'), Card(rank='J', suit='♠'), Card(rank='8', suit='♣'), Card(rank='7', suit='♠')]
        # player_1 should win, due to highest kicker
        player1_hand = [Card(rank='A', suit='♥'), Card(rank='J', suit='♥')]
        player2_hand = [Card("T", "♥"), Card("4", "♦")]
        player3_hand = [Card("A", "♥"), Card("K", "♦")]

        table.set_community_cards(community_cards)
        player1.set_hand(player1_hand)
        player2.set_hand(player2_hand)
        player3.set_hand(player3_hand)

        table.add_player(player1)
        table.add_player(player2)
        table.add_player(player3)
        if test == 'pair':
            self.assertEqual(game.determine_winners()[0], player3)


if __name__ == '__main__':
    unittest.main()