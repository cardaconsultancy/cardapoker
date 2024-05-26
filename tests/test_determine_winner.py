# cut up logic in parts
# TODO: Integrate player feedback logic
# create an GPT that can help players set up their player
# TODO: AI commentator

import unittest
from poker_game.utils.play_round import play_round
from poker_game.utils.players import create_player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.get_and_pay_winners import determine_winners
from poker_game.utils.logging_config import setup_logging

setup_logging(logging_mode="DEBUG")

TEST_ONE = True


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

            gets_it_in_hands.hand = [Card("A", "♠"), Card("T", "♥")]
            does_not_get_it1.hand = [Card("A", "♣"), Card("K", "♠")]
            does_not_get_it2.hand = [Card("A", "♦"), Card("9", "♦")]

            test_cards = [
                Card("A", "♥"),
                Card("K", "♥"),
                Card("Q", "♥"),
                Card("J", "♥"),
                Card("T", "♠"),
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

    # # a two pair
    # community_cards = [Card("T", "♠"), Card("9", "♠"), Card("8", "♦"), Card("3", "♦"), Card("2", "♠")]
    # # player_1 should win, due to highest kicker
    # player1_hand = [Card("T", "♥"), Card("9", "♦")]
    # player2_hand = [Card("T", "♥"), Card("2", "♦")]
    # player3_hand = [Card("A", "♥"), Card("K", "♦")]

    # # trips
    # community_cards = [Card("T", "♠"), Card("9", "♠"), Card("8", "♦"), Card("2", "♦"), Card("2", "♠")]
    # # player_1 should win, due to highest kicker
    # player1_hand = [Card("6", "♥"), Card("2", "♦")]
    # player2_hand = [Card("7", "♥"), Card("2", "♦")]
    # player3_hand = [Card("A", "♥"), Card("K", "♦")]

    # # straight
    # community_cards = [
    #     Card("3", "♠"),
    #     Card("4", "♠"),
    #     Card("5", "♦"),
    #     Card("K", "♦"),
    #     Card("K", "♠"),
    # ]
    # player1_hand = [Card("A", "♥"), Card("2", "♦")]
    # player2_hand = [Card("2", "♥"), Card("6", "♦")]
    # player3_hand = [Card("6", "♥"), Card("7", "♦")]

    # # # flush
    # community_cards = [Card("3", "♠"), Card("4", "♠"), Card("5", "♠"), Card("K", "♠"), Card("K", "♠")]
    # player1_hand = [Card("A", "♠"), Card("2", "♦")]
    # player2_hand = [Card("2", "♠"), Card("6", "♦")]
    # player3_hand = [Card("6", "♠"), Card("7", "♦")]

    # # # full house
    # community_cards = [Card("3", "♠"), Card("3", "♠"), Card("3", "♠"), Card("K", "♠"), Card("6", "♠")]
    # player1_hand = [Card("A", "♠"), Card("A", "♦")]
    # player2_hand = [Card("2", "♠"), Card("2", "♦")]
    # player3_hand = [Card("6", "♠"), Card("6", "♦")]

    # # # quads
    # community_cards = [Card("3", "♠"), Card("3", "♦"), Card("3", "♠"), Card("2", "♦"), Card("2", "♠")]
    # player1_hand = [Card("A", "♠"), Card("3", "♦")]
    # player2_hand = [Card("2", "♠"), Card("2", "♦")]
    # player3_hand = [Card("6", "♠"), Card("3", "♦")]

    # # # quads
    # community_cards = [Card("3", "♠"), Card("3", "♠"), Card("3", "♠"), Card("2", "♠"), Card("2", "♠")]
    # player1_hand = [Card("A", "♠"), Card("3", "♦")]
    # player2_hand = [Card("2", "♠"), Card("2", "♦")]
    # player3_hand = [Card("6", "♠"), Card("3", "♦")]

    # # straight flush
    # community_cards = [Card("3", "♠"), Card("4", "♠"), Card("5", "♠"), Card("6", "♦"), Card("7", "♦")]
    # player1_hand = [Card("A", "♠"), Card("2", "♦")]
    # player2_hand = [Card("A", "♠"), Card("2", "♠")]
    # player3_hand = [Card("6", "♠"), Card("2", "♠")]

    # straight check
    # community_cards = [Card("9", "♠"), Card("Q", "♠"), Card("K", "♠"), Card("6", "♦"), Card("8", "♦")]
    # player1_hand = [Card("J", "♠"), Card("5", "♦")]
    # player2_hand = [Card("T", "♠"), Card("J", "♦")]
    # player3_hand = [Card("A", "♠"), Card("2", "♠")]

    # table.set_community_cards(community_cards)
    # player1.set_hand(player1_hand)
    # player2.set_hand(player2_hand)
    # player3.set_hand(player3_hand)

    # table.add_player(player1)
    # table.add_player(player2)
    # table.add_player(player3)
    # if test == 'pair':
    #     self.assertEqual(game.determine_winners(pot_players)[0], player3)
    # if test == 'quads':
    #     self.assertEqual(game.determine_winners(pot_players)[0], player1)
    # if test == "straight":
    #     self.assertEqual(
    #         determine_winners(table=table, pot_players=pot_players)[0], player3
    #     )

    # class TestTexasHoldemGame(unittest.TestCase):

    #     # def test_game_initialization(self):
    #     #     deck = Deck()
    #     #     table = Table()
    #     #     game = TexasHoldemGame(table, deck)
    #     #     self.assertEqual(game.table, table)
    #     #     self.assertEqual(game.deck, deck)

    #     def test_play_round(self):
    #         deck = Deck()
    #         table = Table()
    #         game = TexasHoldemGame(table, deck)

    #         # Add players to the table
    #         # table.add_chair(8)
    #         player1 = Player("Alice", Chips(4))
    #         player2 = Player("Bob", Chips(4))
    #         # player1.chips = 100
    #         # player2.chips = 100
    #         table.add_player(player1)
    #         table.add_player(player2)

    #         # Manually set community cards and player hands for testing
    #         # community_cards = [Card("A", "♠"), Card("K", "♠"), Card("Q", "♠"), Card("J", "♠"), Card("9", "♠")]
    #         # player1_hand = [Card("A", "♥"), Card("A", "♦")]
    #         # player2_hand = [Card("K", "♥"), Card("K", "♦")]

    #         # Set the game state for testing
    #         # table.set_community_cards(community_cards)
    #         # player1.set_hand(player1_hand)
    #         # player2.set_hand(player2_hand)

    #         # Play a round
    # play_round(table)


#         # Check if the pot and winner are updated correctly
#         self.assertEqual(table.pot, 0)  # Assuming no betting for simplicity in this example
#         self.assertEqual(game.determine_winner(), player1)

#         # Check if player chip counts are updated correctly
#         self.assertEqual(player1.chips.amount, 200)  # Assuming the initial chip count was 100 for each player
#         self.assertEqual(player2.chips.amount, 0)    # Player 2 lost the round

#     # Add more tests for TexasHoldemGame as needed


if __name__ == "__main__":
    unittest.main()
