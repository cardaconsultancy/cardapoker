# cut up logic in parts
# TODO : Integrate player feedback logic
# create an GPT that can help players set up their player
# TODO : AI commentator

import unittest
from utils.players import Player
from utils.table import Table
from utils.objects_on_table import Deck, Chips, Card, Pot
from utils.game import TexasHoldemGame

# class TestDeck(unittest.TestCase):

#     def test_deck_initialization(self):
#         deck = Deck()
#         self.assertEqual(len(deck.cards), 52)
#         self.assertEqual(len(deck.dealt_cards), 0)

#     def test_deal_one_card(self):
#         deck = Deck()
#         initial_card_count = len(deck.cards)
#         card = deck.deal()
#         self.assertIsInstance(card, Card)
#         self.assertEqual(len(deck.dealt_cards), 1)
#         self.assertEqual(len(deck.cards), initial_card_count - 1)

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

class TestTexasHoldemGame(unittest.TestCase):

    # def test_game_initialization(self):
    #     deck = Deck()
    #     table = Table()
    #     game = TexasHoldemGame(table, deck)
    #     self.assertEqual(game.table, table)
    #     self.assertEqual(game.deck, deck)

    def test_play_round(self):
        deck = Deck()
        table = Table()
        game = TexasHoldemGame(table, deck)
        pot = Pot()

        player1 = Player("Klaas", Chips(100))
        player2 = Player("Jan", Chips(100))
        player3 = Player("Piet", Chips(100))
        
        pot_players = [player1, player2, player3]

        test = 'straight'

        # # a pair
        # community_cards = [Card(rank='3', suit='♣'), Card(rank='2', suit='♠'), Card(rank='J', suit='♠'), Card(rank='8', suit='♣'), Card(rank='7', suit='♠')]
        # # player_1 should win, due to highest kicker
        # player1_hand = [Card(rank='A', suit='♥'), Card(rank='J', suit='♥')]
        # player2_hand = [Card("T", "♥"), Card("4", "♦")]
        # player3_hand = [Card("A", "♥"), Card("K", "♦")]

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
        community_cards = [Card("3", "♠"), Card("4", "♠"), Card("5", "♦"), Card("K", "♦"), Card("K", "♠")]
        player1_hand = [Card("A", "♥"), Card("2", "♦")]
        player2_hand = [Card("2", "♥"), Card("6", "♦")]
        player3_hand = [Card("6", "♥"), Card("7", "♦")]

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

#         DEBUG:utils.game:On the table lies 8 of ♦.
# DEBUG:utils.game:On the table lies 9 of ♣.
# DEBUG:utils.game:On the table lies Q of ♣.
# DEBUG:utils.game:On the table lies K of ♠.
# DEBUG:utils.game:On the table lies 6 of ♣.
# DEBUG:utils.game:   Jan has a J of ♦.
# DEBUG:utils.game:   Jan has a 5 of ♥.
        # straight check
        # community_cards = [Card("9", "♠"), Card("Q", "♠"), Card("K", "♠"), Card("6", "♦"), Card("8", "♦")]
        # player1_hand = [Card("J", "♠"), Card("5", "♦")]
        # player2_hand = [Card("T", "♠"), Card("J", "♦")]
        # player3_hand = [Card("A", "♠"), Card("2", "♠")]

        table.set_community_cards(community_cards)
        player1.set_hand(player1_hand)
        player2.set_hand(player2_hand)
        player3.set_hand(player3_hand)

        table.add_player(player1)
        table.add_player(player2)
        table.add_player(player3)
        # if test == 'pair':
        #     self.assertEqual(game.determine_winners(pot_players)[0], player3)
        # if test == 'quads':
        #     self.assertEqual(game.determine_winners(pot_players)[0], player1)
        if test == 'straight':
            self.assertEqual(game.determine_winners(pot_players)[0], player1)


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
        game.start_round()

#         # Check if the pot and winner are updated correctly
#         self.assertEqual(table.pot, 0)  # Assuming no betting for simplicity in this example
#         self.assertEqual(game.determine_winner(), player1)

#         # Check if player chip counts are updated correctly
#         self.assertEqual(player1.chips.amount, 200)  # Assuming the initial chip count was 100 for each player
#         self.assertEqual(player2.chips.amount, 0)    # Player 2 lost the round

#     # Add more tests for TexasHoldemGame as needed


if __name__ == '__main__':
    unittest.main()
