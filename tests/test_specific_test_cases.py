import unittest
from poker_game.utils.players import create_player
from poker_game.utils.start_round import start_round
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.logging_config import setup_logging
import logging
setup_logging()

logger = logging.getLogger('poker_game')

# this is a test where the person after the BB folds, making last raiser disappear
class TestTexasHoldemGame(unittest.TestCase):
    def test_fold_after_BB(self):
        table = Table()

        player1 = create_player("F", 'always fold', Chips(97))
        player2 = create_player("D", 'careful calculator', Chips(199))
        player3 = create_player("B", 'conservative', Chips(304))
        
        table.add_player(player1)
        table.add_player(player2)
        table.add_player(player3)

        player1.hand = [Card('3', '♥'), Card('3', '♣')] 
        player2.hand = [Card('Q', '♠'), Card('A', '♠')] 
        player3.hand = [Card('9', '♥'), Card('5', '♠')] 

        test_cards = [Card('5', '♦'), Card('7', '♣'), Card('8', '♦'), Card('9', '♣'), Card('T', '♣')] 

        expected_sum = sum([player.chips.amount for player in table.players])

        result = start_round(table=table, test_cards = test_cards)
        print(expected_sum)
        print(sum([player.chips.amount for player in result.players]))
        self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

    def test_pot_management(self):
        table = Table()

        player1 = create_player("A", 'raises with aces reduces with 12345', Chips(50))
        player2 = create_player("B", 'conservative', Chips(50))
        player3 = create_player("C", 'conservative', Chips(50))
        player4 = create_player("D", 'careful calculator', Chips(260))
        player5 = create_player("E", 'aggressive', Chips(90))
        player6 = create_player("F", 'always fold', Chips(100))
        
        table.add_player(player2)
        table.add_player(player3)
        table.add_player(player4)
        table.add_player(player5)
        table.add_player(player6)
        table.add_player(player1)

        player1.hand = [Card('4', '♣'), Card('6', '♠')] 
        player2.hand = [Card('2', '♦'), Card('T', '♦')] 
        player3.hand = [Card('2', '♣'), Card('A', '♦')]
        player4.hand = [Card('3', '♥'), Card('K', '♣')] 
        player5.hand = [Card('8', '♥'), Card('8', '♠')] 
        player6.hand = [Card('K', '♦'), Card('T', '♠')] 

        test_cards = [Card('7', '♦'), Card('9', '♠'), Card('K', '♥'), Card('9', '♦'), Card('4', '♦')] 

        expected_sum = sum([player.chips.amount for player in table.players])

        result = start_round(table=table, test_cards = test_cards)
        print(expected_sum)
        print(sum([player.chips.amount for player in result.players]))
        self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)


if __name__ == '__main__':
    unittest.main()