import unittest
from poker_game.utils.players import create_player
from poker_game.utils.play_round import start_round
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.logging_config import setup_logging
import logging
setup_logging()

logger = logging.getLogger('poker_game')

# this is a test where the person after the BB folds, making last raiser disappear
class TestTexasHoldemGame(unittest.TestCase):

# always_fold_B = create_player("always_fold_B", "always_fold", Chips(592))
# always_fold_E = create_player("always_fold_E", "always_fold", Chips(7))
# aggressive_F = create_player("aggressive_F", "aggressive", Chips(1))
# always_fold_B.hand = [Card("4", "♠"), Card("4", "♣")]
# always_fold_E.hand = [Card("2", "♣"), Card("K", "♠")]
# aggressive_F.hand = [Card("A", "♦"), Card("9", "♦")]
# SB-always_fold_B-8
# BB-always_fold_E-7
# aggressive_F-1-AI
# always_fold_B-F
# [Card("A", "♥"), Card("6", "♦"), Card("8", "♠"), Card("2", "♦"), Card("6", "♠")]
# always_fold_E-wins-12
# aggressive_F-wins-3
    def test_pot_does_not_add_up(self):
        table = Table()
        table.blind_size = 8
        always_fold_B = create_player("always_fold_B", "always_fold", Chips(592))
        always_fold_E = create_player("always_fold_E", "always_fold", Chips(7))
        aggressive_F = create_player("aggressive_F", "aggressive", Chips(1))

        table.add_player(aggressive_F)
        table.add_player(always_fold_B)
        table.add_player(always_fold_E)

        always_fold_B.hand = [Card("4", "♠"), Card("4", "♣")]
        always_fold_E.hand = [Card("2", "♣"), Card("K", "♠")]
        aggressive_F.hand = [Card("A", "♦"), Card("9", "♦")]

        test_cards = [Card("A", "♥"), Card("6", "♦"), Card("8", "♠"), Card("2", "♦"), Card("6", "♠")]
        expected_sum = sum([player.chips.amount for player in table.players])

        result = start_round(table=table, test_cards = test_cards)
        print(expected_sum)
        print(sum([player.chips.amount for player in result.players]))
        self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_SB_missed_betting_opportunity(self):
    #     table = Table()
    #     table.blind_size = 2
    #     A = create_player("A", "raises_with_aces_reduces_with_12345", Chips(512))
    #     C = create_player("C", "conservative", Chips(6))
    #     E = create_player("E", "aggressive", Chips(12))
    #     F = create_player("F", "always_fold", Chips(70))

    #     table.add_player(C)
    #     table.add_player(E)
    #     table.add_player(F)
    #     table.add_player(A)

    #     A.hand = [Card("5", "♦"), Card("6", "♠")]
    #     C.hand = [Card("5", "♣"), Card("6", "♥")]
    #     E.hand = [Card("K", "♣"), Card("9", "♦")]
    #     F.hand = [Card("3", "♣"), Card("A", "♦")]

    #     test_cards = [Card("2", "♣"), Card("3", "♥"), Card("K", "♥"), Card("2", "♠"), Card("J", "♠")]
    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_max_arg_is_empty_seq(self):
    #     table = Table()
    #     table.blind_size = 8
        
    #     B = create_player("B", "conservative", Chips(411))
    #     C = create_player("C", "conservative", Chips(6))
    #     D = create_player("D", "careful_calculator", Chips(171))
    #     F = create_player("F", "always_fold", Chips(12))

    #     table.add_player(C)
    #     table.add_player(D)
    #     table.add_player(F)
    #     table.add_player(B)

    #     B.hand = [Card("J", "♠"), Card("7", "♠")]
    #     C.hand = [Card("A", "♠"), Card("9", "♣")]
    #     D.hand = [Card("J", "♥"), Card("8", "♣")]
    #     F.hand = [Card("Q", "♣"), Card("3", "♣")]

    #     test_cards = [Card("2", "♣"), Card("3", "♥"), Card("K", "♥"), Card("2", "♠"), Card("J", "♠")]
    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_last_player_has_no_call_because_they_called_before(self):
    #     table = Table()
    #     table.blind_size = 4
    #     B = create_player("B", "conservative", Chips(5))
    #     C = create_player("C", "conservative", Chips(259))
    #     D = create_player("D", "careful_calculator", Chips(187))
    #     E = create_player("E", "aggressive", Chips(52))
    #     F = create_player("F", "always_fold", Chips(97))
        
    #     table.add_player(F)
    #     table.add_player(B)
    #     table.add_player(C)
    #     table.add_player(D)
    #     table.add_player(E)
        
    #     B.hand = [Card("T", "♠"), Card("5", "♥")]
    #     C.hand = [Card("T", "♥"), Card("4", "♥")]
    #     D.hand = [Card("4", "♠"), Card("A", "♦")]
    #     E.hand = [Card("3", "♣"), Card("5", "♣")]
    #     F.hand = [Card("J", "♠"), Card("7", "♣")]
    #     test_cards = [Card("3", "♠"), Card("7", "♠"), Card("6", "♦"), Card("Q", "♠"), Card("5", "♠")]
    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)



    # def test_not_adding_to_600_due_to_pot_removal(self):
    #     table = Table()
    #     table.blind_size = 4
    #     D = create_player("D", "careful_calculator", Chips(522))
    #     E = create_player("E", "aggressive", Chips(77))
    #     F = create_player("F", "always_fold", Chips(1))

    #     table.add_player(E)
    #     table.add_player(F)
    #     table.add_player(D)

    #     D.hand = [Card("4", "♣"), Card("Q", "♠")]
    #     E.hand = [Card("A", "♠"), Card("2", "♣")]
    #     F.hand = [Card("9", "♣"), Card("7", "♣")]
    #     test_cards = [Card("7", "♥"), Card("Q", "♣"), Card("4", "♠"), Card("Q", "♥"), Card("3", "♠")]
    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_F_is_not_allowed_to_fold_and_loses(self):
    #     table = Table()
    #     table.blind_size = 20
    #     A = create_player("A", 'raises_with_aces_reduces_with_12345', Chips(15))
    #     B = create_player("B", 'conservative', Chips(182))
    #     E = create_player("E", 'aggressive', Chips(399))
    #     F = create_player("F", 'always_fold', Chips(4))

    #     table.add_player(E)
    #     table.add_player(F)
    #     table.add_player(A)
    #     table.add_player(B)

    #     A.hand = [Card("Q", "♦"), Card("A", "♠")]
    #     B.hand = [Card("T", "♠"), Card("K", "♠")]
    #     E.hand = [Card("4", "♥"), Card("6", "♣")]
    #     F.hand = [Card("7", "♣"), Card("3", "♣")]

    #     test_cards = [Card("K", "♠"), Card("T", "♣"), Card("Q", "♦"), Card("5", "♥"), Card("2", "♥")]

    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_F_is_not_allowed_to_fold_and_loses(self):
    #     table = Table()
    #     table.blind_size = 20
    #     C = create_player("C", 'conservative', Chips(590))
    #     F = create_player("F", 'always_fold', Chips(10))    
 
    #     table.add_player(C)
    #     table.add_player(F) 

    #     C.hand = [Card("A", "♥"), Card("A", "♣")]
    #     F.hand = [Card("4", "♠"), Card("T", "♠")] 

    #     test_cards = [Card("A", "♥"), Card("A", "♦"), Card("8", "♠"), Card("5", "♠"), Card("J", "♠")]

    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_sum_error(self):
    #     table = Table()
    #     table.blind_size = 4
    #     D = create_player("D", 'careful_calculator', Chips(592))
    #     F = create_player("F", 'always_fold', Chips(8))    
 
    #     table.add_player(F)
    #     table.add_player(D) 

    #     D.hand = [Card("9", "♣"), Card("8", "♦")]
    #     F.hand = [Card("T", "♣"), Card("8", "♣")]  

    #     test_cards = [Card("J", "♣"), Card("J", "♦"), Card("8", "♠"), Card("5", "♠"), Card("J", "♠")]

    #     expected_sum = sum([player.chips.amount for player in table.players])
    #     print(table.players_game)
    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_fold_after_BB(self):
    #     table = Table()

    #     player1 = create_player("F", 'always_fold', Chips(97))
    #     player2 = create_player("D", 'careful_calculator', Chips(199))
    #     player3 = create_player("B", 'conservative', Chips(304))
        
    #     table.add_player(player1)
    #     table.add_player(player2)
    #     table.add_player(player3)

    #     player1.hand = [Card('3', '♥'), Card('3', '♣')] 
    #     player2.hand = [Card('Q', '♠'), Card('A', '♠')] 
    #     player3.hand = [Card('9', '♥'), Card('5', '♠')] 

    #     test_cards = [Card('5', '♦'), Card('7', '♣'), Card('8', '♦'), Card('9', '♣'), Card('T', '♣')] 

    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_pot_management(self):
    #     table = Table()

    #     player1 = create_player("A", 'raises_with_aces_reduces_with_12345', Chips(50))
    #     player2 = create_player("B", 'conservative', Chips(50))
    #     player3 = create_player("C", 'conservative', Chips(50))
    #     player4 = create_player("D", 'careful_calculator', Chips(260))
    #     player5 = create_player("E", 'aggressive', Chips(90))
    #     player6 = create_player("F", 'always_fold', Chips(100))
        
    #     table.add_player(player2)
    #     table.add_player(player3)
    #     table.add_player(player4)
    #     table.add_player(player5)
    #     table.add_player(player6)
    #     table.add_player(player1)

    #     player1.hand = [Card('4', '♣'), Card('6', '♠')] 
    #     player2.hand = [Card('2', '♦'), Card('T', '♦')] 
    #     player3.hand = [Card('2', '♣'), Card('A', '♦')]
    #     player4.hand = [Card('3', '♥'), Card('K', '♣')] 
    #     player5.hand = [Card('8', '♥'), Card('8', '♠')] 
    #     player6.hand = [Card('K', '♦'), Card('T', '♠')] 

    #     test_cards = [Card('7', '♦'), Card('9', '♠'), Card('K', '♥'), Card('9', '♦'), Card('4', '♦')] 

    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    # def test_equal_cards(self):
    #     table = Table()

    #     B = create_player("B", 'conservative', Chips(168))
    #     E = create_player("E", 'aggressive', Chips(422))
    #     F = create_player("F", 'always_fold', Chips(10))
        
    #     table.add_player(B)
    #     table.add_player(E)
    #     table.add_player(F)

    #     B.hand = [Card("5", "♣"), Card("8", "♥")]
    #     E.hand = [Card("6", "♦"), Card("8", "♠")]
    #     F.hand = [Card("9", "♣"), Card("Q", "♣")]

    #     test_cards = [Card("Q", "♥"), Card("3", "♣"), Card("A", "♠"), Card("2", "♣"), Card("9", "♦")] 

    #     expected_sum = sum([player.chips.amount for player in table.players])

    #     result = start_round(table=table, test_cards = test_cards)
    #     print(expected_sum)
    #     print(sum([player.chips.amount for player in result.players]))
    #     self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

if __name__ == '__main__':
    unittest.main()