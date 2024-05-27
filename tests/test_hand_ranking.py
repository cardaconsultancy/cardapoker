""" Tests for the hand ranking functions """

import unittest
import logging
from poker_game.utils.players import create_player
from poker_game.utils.table import Table
from poker_game.utils.evaluate_hand import get_hand_rank
from poker_game.utils.objects_on_table import Chips, Card
from poker_game.utils.logging_config import setup_logging


setup_logging(logging_mode="DEBUG")
logger = logging.getLogger("poker_game")

TEST_ONE = False


class TestDeck(unittest.TestCase):

    if TEST_ONE:

        def test_template(self):
            pass

    else:

### Royal Flush

        def test_royal_flush(self):
            """Test a royal flush"""
            table = Table()
            gets_royal_flush = create_player(
                "conservative_A", "conservative", Chips(100)
            )
            gets_royal_flush.hand = [Card("A", "♠"), Card("T", "♠")]

            test_cards = [
                Card("A", "♥"),
                Card("K", "♥"),
                Card("T", "♥"),
                Card("J", "♥"),
                Card("Q", "♥"),
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player = gets_royal_flush, table=table)
            self.assertEqual(result, [9, None, None, None, None, None])


        def test_royal_flush_clubs(self):
            """Test a royal flush in clubs"""
            table = Table()
            player = create_player("club_king", "passive", Chips(250))
            player.hand = [Card("A", "♣"), Card("K", "♣")]

            test_cards = [
                Card("Q", "♣"),
                Card("J", "♣"),
                Card("T", "♣"),
                Card("9", "♦"),
                Card("8", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [9, None, None, None, None, None])

        def test_not_royal_flush_missing_ace(self):
            """Test not a royal flush due to missing ace"""
            table = Table()
            player = create_player("no_ace", "aggressive", Chips(200))
            player.hand = [Card("K", "♠"), Card("Q", "♠")]

            test_cards = [
                Card("J", "♠"),
                Card("T", "♠"),
                Card("9", "♠"),
                Card("8", "♠"),
                Card("7", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 9)  # Not a Royal Flush rank

        def test_not_royal_flush_mixed_suits(self):
            """Test not a royal flush due to mixed suits"""
            table = Table()
            player = create_player("mixed_suits", "loose", Chips(150))
            player.hand = [Card("A", "♠"), Card("K", "♥")]

            test_cards = [
                Card("Q", "♠"),
                Card("J", "♥"),
                Card("T", "♠"),
                Card("9", "♥"),
                Card("8", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 9)  # Not a Royal Flush rank


################## straight Flush ####################

        def test_straight_flush_positive(self):
            """Test correctly identifying a straight flush"""
            table = Table()
            player = create_player("flush_guru", "conservative", Chips(300))
            player.hand = [Card("9", "♦"), Card("8", "♦")]

            test_cards = [
                Card("7", "♦"),
                Card("6", "♦"),
                Card("5", "♦"),
                Card("4", "♣"),
                Card("3", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [8, "9", None, None, None, None])

        def test_straight_flush_ace_low(self):
            """Test a straight flush using Ace as the low card"""
            table = Table()
            player = create_player("ace_low", "aggressive", Chips(200))
            player.hand = [Card("A", "♣"), Card("2", "♣")]

            test_cards = [
                Card("3", "♣"),
                Card("4", "♣"),
                Card("5", "♣"),
                Card("6", "♦"),
                Card("7", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [8, "5", None, None, None, None])

        def test_not_straight_flush_mixed_ace(self):
            """Test incorrect straight flush due to Ace from different suit"""
            table = Table()
            player = create_player("mixed_suits", "loose", Chips(150))
            player.hand = [Card("A", "♥"), Card("2", "♠")]

            test_cards = [
                Card("3", "♠"),
                Card("4", "♠"),
                Card("5", "♠"),
                Card("6", "♥"),
                Card("7", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 8)  # Not a Straight Flush rank

        def test_not_straight_flush_broken_sequence(self):
            """Test not a straight flush due to broken sequence"""
            table = Table()
            player = create_player("sequence_breaker", "conservative", Chips(100))
            player.hand = [Card("6", "♦"), Card("7", "♦")]

            test_cards = [
                Card("8", "♦"),
                Card("T", "♦"),
                Card("J", "♦"),
                Card("Q", "♦"),
                Card("K", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 8)  # Not a Straight Flush rank

################## Quads/FOAK ####################

        def test_four_of_a_kind_positive(self):
            """Test correctly identifying a four of a kind"""
            table = Table()
            player = create_player("four_king", "tight", Chips(350))
            player.hand = [Card("K", "♠"), Card("K", "♦")]

            test_cards = [
                Card("K", "♣"),
                Card("K", "♥"),
                Card("3", "♠"),
                Card("4", "♦"),
                Card("5", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [7, "K", '5', None, None, None])

        def test_four_of_a_kind_with_ten(self):
            """Test a four of a kind with Tens"""
            table = Table()
            player = create_player("ten_power", "aggressive", Chips(275))
            player.hand = [Card("T", "♠"), Card("T", "♦")]

            test_cards = [
                Card("T", "♣"),
                Card("T", "♥"),
                Card("2", "♠"),
                Card("4", "♦"),
                Card("5", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [7, "T", '5', None, None, None])

        def test_not_four_of_a_kind_three_cards(self):
            """Test incorrectly identifying a four of a kind with only three matching cards"""
            table = Table()
            player = create_player("missing_fourth", "passive", Chips(225))
            player.hand = [Card("9", "♠"), Card("9", "♦")]

            test_cards = [
                Card("9", "♣"),
                Card("J", "♥"),
                Card("J", "♠"),
                Card("Q", "♦"),
                Card("K", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 7)  # Not a Four of a Kind rank

        def test_not_four_of_a_kind_mixed_ranks(self):
            """Test not a four of a kind due to mixed ranks"""
            table = Table()
            player = create_player("mixed_ranks", "loose", Chips(175))
            player.hand = [Card("8", "♠"), Card("8", "♦")]

            test_cards = [
                Card("8", "♣"),
                Card("7", "♥"),
                Card("7", "♠"),
                Card("6", "♦"),
                Card("6", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 7)  # Not a Four of a Kind rank

##### Full House #####

        def test_full_house_from_two_triplets(self):
            """Test correctly identifying a full house from two sets of triplets"""
            table = Table()
            player = create_player("rich_in_triples", "aggressive", Chips(200))
            player.hand = [Card("9", "♠"), Card("9", "♦")]

            test_cards = [
                Card("9", "♣"),  # Completes a set of three 9s
                Card("8", "♥"),
                Card("8", "♠"),
                Card("8", "♦"),  # Forms another set of three 8s
                Card("7", "♣")
            ]
            table.set_community_cards(test_cards)
            # The hand rank should consider one triplet (here, the higher one, 9s) and a pair from the other triplet (8s).
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [6, "9", "8", None, None, None])

        def test_full_house_from_two_triplets_reverse(self):
            """Test correctly identifying a full house from two sets of triplets"""
            table = Table()
            player = create_player("rich_in_triples", "aggressive", Chips(200))
            player.hand = [Card("8", "♠"), Card("8", "♦")]

            test_cards = [
                Card("8", "♣"),  # Completes a set of three 9s
                Card("9", "♥"),
                Card("9", "♠"),
                Card("9", "♦"),  # Forms another set of three 8s
                Card("7", "♣")
            ]
            table.set_community_cards(test_cards)
            # The hand rank should consider one triplet (here, the higher one, 9s) and a pair from the other triplet (8s).
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [6, "9", "8", None, None, None])

        def test_full_house_standard(self):
            """Test correctly identifying a standard full house"""
            table = Table()
            player = create_player("standard_house", "tight", Chips(300))
            player.hand = [Card("J", "♠"), Card("J", "♦")]

            test_cards = [
                Card("J", "♣"),  # Triplet of Jacks
                Card("4", "♠"),
                Card("4", "♦"),  # Pair of Fours
                Card("2", "♣"),
                Card("3", "♥")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [6, "J", "4", None, None, None])

        def test_not_full_house_only_a_triplet(self):
            """Test not a full house due to only having a triplet and no pair"""
            table = Table()
            player = create_player("missing_pair", "passive", Chips(175))
            player.hand = [Card("J", "♠"), Card("J", "♦")]

            test_cards = [
                Card("J", "♣"),  # Triplet of Jacks
                Card("Q", "♠"),  # Random card
                Card("K", "♦"),  # Random card
                Card("A", "♣"),  # Random card
                Card("2", "♥")   # Random card
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 6)  # Not a Full House rank because it lacks the necessary pair


        def test_full_house_lower_triplet_higher_pair(self):
            """Test correctly identifying a full house with a lower-ranked triplet and a higher-ranked pair"""
            table = Table()
            player = create_player("inverted_full_house", "tight", Chips(300))
            player.hand = [Card("6", "♠"), Card("6", "♦")]

            test_cards = [
                Card("6", "♣"),  # Triplet of Sixes
                Card("A", "♠"),
                Card("A", "♦"),  # Pair of Aces
                Card("2", "♣"),
                Card("3", "♥")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            # Expecting a full house, with '6' as the triplet and 'A' as the pair.
            self.assertEqual(result, [6, "6", "A", None, None, None])

########## Flush ##########

        def test_flush_positive(self):
            """Test correctly identifying a flush"""
            table = Table()
            player = create_player("flush_lover", "aggressive", Chips(300))
            player.hand = [Card("K", "♠"), Card("J", "♠")]

            test_cards = [
                Card("9", "♠"),
                Card("6", "♠"),
                Card("3", "♠"),
                Card("2", "♦"),
                Card("4", "♥")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [5, "K", "J", "9", "6", "3"])

        def test_not_flush_but_royal(self):
            """Test identifying a flush with all face cards and a ten"""
            table = Table()
            player = create_player("high_card_flush", "tight", Chips(250))
            player.hand = [Card("Q", "♦"), Card("J", "♦")]

            test_cards = [
                Card("T", "♦"),
                Card("A", "♦"),
                Card("K", "♦"),
                Card("2", "♠"),
                Card("3", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            print(result)
            self.assertEqual(result, [9, None, None, None, None, None])

        def test_not_flush_mixed_suits(self):
            """Test not a flush due to mixed suits"""
            table = Table()
            player = create_player("mixed_suits", "loose", Chips(200))
            player.hand = [Card("9", "♠"), Card("8", "♦")]

            test_cards = [
                Card("7", "♠"),
                Card("6", "♦"),
                Card("5", "♠"),
                Card("4", "♠"),
                Card("3", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 5)  # Not a flush

        def test_not_flush_only_four_cards_same_suit(self):
            """Test not a flush due to only four cards of the same suit"""
            table = Table()
            player = create_player("almost_flush", "passive", Chips(175))
            player.hand = [Card("A", "♣"), Card("K", "♣")]

            test_cards = [
                Card("Q", "♣"),
                Card("J", "♣"),
                Card("T", "♦"),
                Card("3", "♠"),
                Card("4", "♥")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 5)  # Not a flush

        def test_straight_positive(self):
            """Test correctly identifying a straight"""
            table = Table()
            player = create_player("straight_shooter", "aggressive", Chips(300))
            player.hand = [Card("6", "♠"), Card("7", "♦")]

            test_cards = [
                Card("8", "♣"),
                Card("9", "♠"),
                Card("T", "♠"),
                Card("2", "♦"),  # Non-consecutive card
                Card("3", "♥")   # Non-consecutive card
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [4, "T", None, None, None, None])

        def test_straight_ace_high(self):
            """Test identifying a straight with Ace as high card"""
            table = Table()
            player = create_player("ace_high_straight", "tight", Chips(250))
            player.hand = [Card("K", "♦"), Card("Q", "♦")]

            test_cards = [
                Card("J", "♠"),
                Card("T", "♣"),
                Card("A", "♠"),
                Card("2", "♣"),  # Non-consecutive card
                Card("3", "♦")   # Non-consecutive card
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [4, "A", None, None, None, None])

        def test_straight_ace_low(self):
            """Test identifying a straight with Ace as low card"""
            table = Table()
            player = create_player("ace_low_straight", "loose", Chips(200))
            player.hand = [Card("2", "♠"), Card("3", "♦")]

            test_cards = [
                Card("4", "♣"),
                Card("5", "♥"),
                Card("A", "♦"),
                Card("K", "♣"),  # Non-consecutive card
                Card("Q", "♠")  # Non-consecutive card
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [4, "5", None, None, None, None])

        def test_not_straight_broken_sequence(self):
            """Test not a straight due to broken sequence"""
            table = Table()
            player = create_player("broken_sequence", "passive", Chips(175))
            player.hand = [Card("6", "♠"), Card("7", "♦")]

            test_cards = [
                Card("8", "♣"),
                Card("T", "♠"),  # Gap between 8 and T
                Card("J", "♦"),
                Card("2", "♠"),
                Card("3", "♥")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 4)  # Not a straight

        def test_not_straight_insufficient_consecutive_cards(self):
            """Test not a straight due to insufficient consecutive cards"""
            table = Table()
            player = create_player("almost_straight", "conservative", Chips(150))
            player.hand = [Card("T", "♣"), Card("J", "♠")]

            test_cards = [
                Card("Q", "♦"),
                Card("K", "♥"),  # Four consecutive high cards
                Card("3", "♠"),  # Random low card
                Card("4", "♦"),  # Random low card
                Card("5", "♥")   # Random low card
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 4)  # Not a straight
    
        def test_highest_straight_from_seven_consecutive_cards(self):
            """Test identifying the highest straight from a sequence of seven consecutive cards"""
            table = Table()
            player = create_player("high_straight_expert", "aggressive", Chips(300))
            player.hand = [Card("8", "♠"), Card("9", "♦")]

            test_cards = [
                Card("5", "♣"),  # Starts the consecutive sequence
                Card("6", "♠"),  # Continues the sequence
                Card("7", "♦"),  # Continues the sequence
                Card("T", "♣"), # Ends the seven-card straight
                Card("J", "♥")   # Beyond the needed sequence for a straight to "10"
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            # The expected highest straight is "J" down to "7"
            self.assertEqual(result, [4, "J", None, None, None, None])

##### Trips/TOAK #####

        def test_three_of_a_kind_positive(self):
            """Test correctly identifying a three of a kind"""
            table = Table()
            player = create_player("trips_master", "aggressive", Chips(300))
            player.hand = [Card("7", "♠"), Card("7", "♦")]

            test_cards = [
                Card("7", "♣"),
                Card("K", "♦"),
                Card("4", "♥"),
                Card("2", "♠"),
                Card("3", "♥")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [3, "7", "K", "4", None, None])

        def test_three_of_a_kind_with_higher_kicker(self):
            """Test correctly identifying a three of a kind with a high kicker"""
            table = Table()
            player = create_player("trips_high_kicker", "tight", Chips(250))
            player.hand = [Card("Q", "♠"), Card("Q", "♦")]

            test_cards = [
                Card("Q", "♣"),
                Card("A", "♦"),
                Card("J", "♠"),
                Card("9", "♣"),
                Card("8", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [3, "Q", "A", "J", None, None])

        def test_not_three_of_a_kind_two_pairs(self):
            """Test not a three of a kind due to only having two pairs"""
            table = Table()
            player = create_player("two_pair", "loose", Chips(200))
            player.hand = [Card("8", "♠"), Card("8", "♦")]

            test_cards = [
                Card("K", "♠"),
                Card("K", "♦"),
                Card("J", "♣"),
                Card("3", "♠"),
                Card("2", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 3)  # Not a three of a kind

        def test_not_three_of_a_kind_full_house(self):
            """Test correctly not identifying a three of a kind when a full house is present"""
            table = Table()
            player = create_player("full_house_tester", "passive", Chips(175))
            player.hand = [Card("5", "♣"), Card("5", "♠")]

            test_cards = [
                Card("5", "♦"),  # Completes three of a kind
                Card("8", "♠"),
                Card("8", "♦"),  # Forms a pair, creating a full house
                Card("J", "♥"),
                Card("2", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 3)  # Should be a full house, not just three of a kind


        def test_full_house_instead_of_trips(self):
            """Test correctly identifying the full house"""
            table = Table()
            player = create_player("high_trips_selector", "aggressive", Chips(300))
            player.hand = [Card("K", "♠"), Card("K", "♦")]

            test_cards = [
                Card("K", "♣"),  # Completes a set of three Kings
                Card("9", "♦"),
                Card("9", "♠"),
                Card("9", "♥"),  # Completes a set of three Nines
                Card("2", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            # The highest three of a kind (Kings) should be selected, not the Nines.
            self.assertEqual(result, [6, 'K', '9', None, None, None])

##### Two Pair #####

        def test_two_pair_positive(self):
            """Test correctly identifying a two pair"""
            table = Table()
            player = create_player("pair_twice", "aggressive", Chips(300))
            player.hand = [Card("Q", "♠"), Card("Q", "♦")]

            test_cards = [
                Card("8", "♣"),
                Card("8", "♠"),
                Card("K", "♦"),
                Card("4", "♥"),
                Card("2", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [2, "Q", "8", "K", None, None])

        def test_two_pair_with_three_pairs(self):
            """Test identifying the highest two pairs when three pairs are present"""
            table = Table()
            player = create_player("triple_pair", "tight", Chips(250))
            player.hand = [Card("J", "♦"), Card("J", "♠")]

            test_cards = [
                Card("9", "♠"),
                Card("9", "♣"),
                Card("6", "♠"),
                Card("6", "♦"),
                Card("3", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            # Should pick the two highest pairs (Jacks and Nines) and ignore the Sixes, with the highest other card.
            self.assertEqual(result, [2, "J", "9", "6", None, None])

        def test_not_two_pair_only_one_pair(self):
            """Test not a two pair due to only one pair being present"""
            table = Table()
            player = create_player("one_pair_guy", "loose", Chips(200))
            player.hand = [Card("7", "♠"), Card("7", "♦")]

            test_cards = [
                Card("5", "♣"),
                Card("3", "♠"),
                Card("K", "♦"),
                Card("2", "♣"),
                Card("4", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 2)  # Not a two pair

        def test_not_two_pair_full_house(self):
            """Test correctly not identifying a two pair when a full house is present"""
            table = Table()
            player = create_player("full_house_tester", "passive", Chips(175))
            player.hand = [Card("5", "♣"), Card("5", "♠")]

            test_cards = [
                Card("5", "♦"),  # Completes three of a kind
                Card("8", "♠"),
                Card("8", "♦"),  # Forms a pair, creating a full house
                Card("J", "♥"),
                Card("2", "♦")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 2)  # Should be a full house, not two pair

###### Pair ######

        def test_pair_positive(self):
            """Test correctly identifying a pair"""
            table = Table()
            player = create_player("pair_player", "aggressive", Chips(300))
            player.hand = [Card("5", "♠"), Card("5", "♦")]

            test_cards = [
                Card("K", "♣"),
                Card("J", "♠"),
                Card("8", "♦"),
                Card("2", "♠"),
                Card("3", "♠")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            # Expecting "Pair" with fives, highest other cards are K, J, 8
            self.assertEqual(result, [1, "5", "K", "J", "8"])

        def test_two_pairs_with_multiple_pairs(self):
            """Test identifying the two pair when multiple pairs are present"""
            table = Table()
            player = create_player("multiple_pairs", "tight", Chips(250))
            player.hand = [Card("Q", "♦"), Card("Q", "♠")]

            test_cards = [
                Card("J", "♠"),
                Card("J", "♦"),
                Card("A", "♣"),
                Card("9", "♦"),
                Card("8", "♣")
            ]
            table.set_community_cards(test_cards)
            # Should pick the highest pair (Queens) and include the highest other card (Ace)
            result = get_hand_rank(player=player, table=table)
            self.assertEqual(result, [2, 'Q', 'J', 'A', None, None])

        def test_not_pair_only_high_card(self):
            """Test correctly not identifying a pair when only high cards are present"""
            table = Table()
            player = create_player("high_card_only", "loose", Chips(200))
            player.hand = [Card("K", "♠"), Card("J", "♦")]

            test_cards = [
                Card("9", "♣"),
                Card("6", "♠"),
                Card("3", "♦"),
                Card("2", "♥"),
                Card("4", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 1)  # No pairs, should not be classified as a pair

####### High Card #######

        def test_high_card_positive(self):
            """Test correctly identifying a high card hand"""
            table = Table()
            player = create_player("high_card_king", "passive", Chips(300))
            player.hand = [Card("K", "♠"), Card("J", "♦")]

            test_cards = [
                Card("9", "♣"),
                Card("6", "♠"),
                Card("3", "♠"),
                Card("2", "♦"),
                Card("4", "♥")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            # Expecting "High Card" with King as the highest, then Jack, 9, 6, and 4
            self.assertEqual(result, [0, "K", "J", "9", "6", "4"])

        def test_high_card_with_non_sequential_cards(self):
            """Test identifying a high card hand from a random assortment of non-sequential cards"""
            table = Table()
            player = create_player("random_hand", "loose", Chips(250))
            player.hand = [Card("Q", "♦"), Card("7", "♠")]

            test_cards = [
                Card("5", "♣"),
                Card("3", "♦"),
                Card("9", "♥"),
                Card("J", "♠"),
                Card("2", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            # The hand should be ranked by the highest cards: Q, J, 9, 7, 5
            self.assertEqual(result, [0, "Q", "J", "9", "7", "5"])

        def test_not_high_card_due_to_pair(self):
            """Test correctly not identifying a high card when a pair is present"""
            table = Table()
            player = create_player("accidental_pair", "conservative", Chips(200))
            player.hand = [Card("8", "♠"), Card("8", "♦")]

            test_cards = [
                Card("K", "♣"),
                Card("4", "♠"),
                Card("2", "♥"),
                Card("6", "♦"),
                Card("J", "♣")
            ]
            table.set_community_cards(test_cards)
            result = get_hand_rank(player=player, table=table)
            self.assertNotEqual(result[0], 0)  # Not a high card due to the presence of a pair

if __name__ == "__main__":
    unittest.main()