# cut up logic in parts
# TODO: Integrate player feedback logic
# create an GPT that can help players set up their player
# TODO: AI commentator

import unittest
import logging
from poker_game.utils.play_round import play_round
from poker_game.utils.players import create_player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.get_and_pay_winners import determine_winners
from poker_game.utils.logging_config import setup_logging


setup_logging(logging_mode="DEBUG")
logger = logging.getLogger("poker_game")

TEST_ONE = False


class TestDeck(unittest.TestCase):

    if TEST_ONE:

        def test_template(self):
            pass

    else:

        def test_deck_initialization(self):
            deck = Deck()
            self.assertEqual(len(deck.cards), 52)

        def test_deal_one_card(self):
            deck = Deck()
            initial_card_count = len(deck.cards)
            card = deck.deal()
            self.assertIsInstance(card, Card)
            self.assertEqual(len(deck.cards), initial_card_count - 1)

        def test_royal_flush(self):
            """Test a royal flush"""
            table = Table()
            table.blind_size = 8
            gets_it_in_hands = create_player(
                "conservative_A", "conservative", Chips(100)
            )
            does_not_get_it1 = create_player(
                "conservative_B", "conservative", Chips(100)
            )
            does_not_get_it2 = create_player(
                "conservative_C", "conservative", Chips(100)
            )

            table.add_player(gets_it_in_hands)
            table.add_player(does_not_get_it1)
            table.add_player(does_not_get_it2)

            gets_it_in_hands.hand = [Card("A", "♥"), Card("T", "♠")]
            does_not_get_it1.hand = [Card("A", "♣"), Card("K", "♠")]
            does_not_get_it2.hand = [Card("A", "♦"), Card("9", "♦")]
            test_cards = [
                Card("A", "♥"),
                Card("K", "♥"),
                Card("T", "♥"),
                Card("J", "♥"),
                Card("Q", "♥"),
            ]
            expected_sum = sum([player.chips.amount for player in table.players])

            result = play_round(table=table, test_cards=test_cards)
            print(expected_sum)
            print(sum([player.chips.amount for player in result.players]))
            self.assertEqual(
                sum([player.chips.amount for player in result.players]), expected_sum
            )

    #     def test_get_number_of_cards(self):
    #         deck = Deck()
    #         self.assertEqual(deck.get_number_of_cards(), 52)
    #         deck.deal()
    #         self.assertEqual(deck.get_number_of_cards(), 51)

    # class TestChips(unittest.TestCase):

    #     def test_chips_initialization(self):
    #         chips = Chips()
    #         self.assertEqual(chips.amount, 0)

    #     def test_chips_win(self):
    #         chips = Chips(100)
    #         chips.win(50)
    #         self.assertEqual(chips.amount, 150)

    #     def test_chips_lose(self):
    #         chips = Chips(100)
    #         chips.lose(30)
    #         self.assertEqual(chips.amount, 70)

    # class TestPlayer(unittest.TestCase):

    #     def test_player_initialization(self):
    #         player = Player("John", Chips(100))
    #         self.assertEqual(player.name, "John")
    #         self.assertEqual(len(player.hand), 0)
    #         self.assertIsInstance(player.chips, Chips)

    #     def test_receive_card(self):
    #         player = Player("John", Chips(100))
    #         card = Card("A", "♠")
    #         player.receive_card(card)
    #         self.assertIn(card, player.hand)

    # class TestTable(unittest.TestCase):

    #     def test_table_initialization(self):
    #         table = Table()
    #         self.assertEqual(len(table.community_cards), 0)
    #         self.assertEqual(len(table.players), 0)

    #     def test_add_remove_player(self):
    #         table = Table()
    #         player = Player("Alice", Chips(100))
    #         # table.add_chair(1)
    #         table.add_player(player)
    #         self.assertIn(player, table.players)
    #         table.remove_player(player)
    #         self.assertNotIn(player, table.players)

    # def test_game_initialization(self):
    #     deck = Deck()
    #     table = Table()
    #     game = TexasHoldemGame(table, deck)
    #     self.assertEqual(game.table, table)
    #     self.assertEqual(game.deck, deck)

    # def test_play_round(self):
    #     deck = Deck()
    #     table = Table()
    #     game = TexasHoldemGame(table, deck)
    #     pot = Pot()
    #     player1 = create_player("A", "raises_with_aces_reduces_with_12345", Chips(100))
    #     player2 = create_player("B", "conservative", Chips(100))
    #     player3 = create_player("C", "conservative", Chips(100))

    #     pot_players = [player1, player2, player3]

    #     # a pair
    #     community_cards = [
    #         Card(rank="3", suit="♣"),
    #         Card(rank="2", suit="♠"),
    #         Card(rank="J", suit="♠"),
    #         Card(rank="8", suit="♣"),
    #         Card(rank="7", suit="♠"),
    #     ]
    #     # player_1 should win, due to highest kicker
    #     player1_hand = [Card(rank="A", suit="♥"), Card(rank="J", suit="♥")]
    #     player2_hand = [Card("T", "♥"), Card("4", "♦")]
    #     player3_hand = [Card("A", "♥"), Card("K", "♦")]

    #     self.assertEqual(play_round(table), 0)


if __name__ == "__main__":
    unittest.main()
