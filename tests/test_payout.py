import unittest
from poker_game.utils.players import Player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Pot, Card
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.logging_config import setup_logging
from poker_game.utils.get_and_pay_winners import pay_winners

setup_logging()


class TestTexasHoldemGame(unittest.TestCase):

    def test_pay_winners(self):
        deck = Deck()
        table = Table()
        game = TexasHoldemGame(table, deck)

        player1 = Player("Klaas", Chips(0))
        player2 = Player("Jan", Chips(0))
        player3 = Player("Piet", Chips(0))

        test_hands = "p1 p2 p3 all equal and all in"

        if test_hands == "p1 p2 p3 all equal and all in":
            player1 = Player("Klaas", Chips(0))
            player2 = Player("Jan", Chips(0))
            player3 = Player("Piet", Chips(0))
            
            community_cards = [
                Card(rank="3", suit="♣"),
                Card(rank="2", suit="♠"),
                Card(rank="T", suit="♠"),
                Card(rank="8", suit="♣"),
                Card(rank="7", suit="♠"),
            ]
            # all equal, all all in
            player1_hand = [Card(rank="A", suit="♥"), Card(rank="J", suit="♥")]
            player2_hand = [Card("A", "♥"), Card("J", "♦")]
            player3_hand = [Card("A", "♥"), Card("J", "♦")]

        elif test_hands == "p1 winner, p2 second, p3 loser":
            community_cards = [
                Card(rank="3", suit="♣"),
                Card(rank="2", suit="♠"),
                Card(rank="J", suit="♠"),
                Card(rank="8", suit="♣"),
                Card(rank="7", suit="♠"),
            ]
            # player_1 should win, due to highest kicker
            player1_hand = [Card(rank="A", suit="♥"), Card(rank="J", suit="♥")]
            player2_hand = [Card("A", "♥"), Card("K", "♦")]
            player3_hand = [Card("T", "♥"), Card("4", "♦")]

        elif test_hands == "p1 and p2 winner, p3 loser":
            community_cards = [
                Card(rank="3", suit="♣"),
                Card(rank="2", suit="♠"),
                Card(rank="J", suit="♠"),
                Card(rank="8", suit="♣"),
                Card(rank="7", suit="♠"),
            ]
            # player_1 should win, due to highest kicker
            player1_hand = [Card("A", "♥"), Card("J", "♥")]
            player2_hand = [Card("A", "♥"), Card("J", "♥")]
            player3_hand = [Card("A", "♥"), Card("K", "♦")]

        table.set_community_cards(community_cards)
        player1.set_hand(player1_hand)
        player2.set_hand(player2_hand)
        player3.set_hand(player3_hand)

        table.add_player(player1)
        table.add_player(player2)
        table.add_player(player3)

        testpot = Pot()
        testpot.amount = 300
        testpot.players = [player1, player2, player3]

        table.pots = [testpot]
        pay_winners(table, 'round_ID')

        if test_hands == "p1 and p2 winner, p3 loser":
            self.assertEqual(150, player1.chips.amount)
            self.assertEqual(150, player2.chips.amount)
            self.assertEqual(0, player3.chips.amount)
        
        elif test_hands == "p1 winner, p2 second, p3 loser":
            self.assertEqual(300, player1.chips.amount)
        
        elif test_hands == "p1 p2 p3 all in all equal":
            self.assertEqual(100, player1.chips.amount)
            self.assertEqual(100, player2.chips.amount)
            self.assertEqual(100, player3.chips.amount)


if __name__ == "__main__":
    unittest.main()
