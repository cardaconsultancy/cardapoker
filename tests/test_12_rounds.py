import unittest
from poker_game.utils.players import create_player
from poker_game.utils.start_round import start_round
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.logging_config import setup_logging
setup_logging()

class TestTexasHoldemGame(unittest.TestCase):
    def test_play_round(self):
        ranks = ['2','3','4','5','6','7','8','9','T','J','Q','K','A']
        for nr in range(0, len(ranks)):

            print('+++++++++++++++++++++++++++++++++')
            print('++++++ Number: ', nr, '++++++++')
            print('+++++++++++++++++++++++++++++++++')
            
            table = Table()

            player1 = create_player("Grietje", 'raises_with_aces_reduces_with_12345', Chips(100))
            player2 = create_player("Jan", 'conservative', Chips(100))
            player3 = create_player("Martin", 'raises_with_aces_reduces_with_12345', Chips(100))
            
            table.add_player(player1)
            table.add_player(player2)
            table.add_player(player3)

            player1.hand = [Card(ranks[nr], '♠'), Card(ranks[nr], '♥')] 
            player2.hand = [Card(ranks[nr-1], '♠'), Card(ranks[nr-1], '♥')] 
            player3.hand = [Card(ranks[nr-2], '♠'), Card(ranks[nr-2], '♥')] 

            test_cards = [Card('5', '♦'), Card('7', '♣'), Card('8', '♦'), Card('9', '♣'), Card('T', '♣')] 

            expected_sum = sum([player.chips.amount for player in table.players])

            result = start_round(table=table, test_cards = test_cards)
            print(expected_sum)
            print(sum([player.chips.amount for player in result.players]))
            self.assertEqual(sum([player.chips.amount for player in result.players]), expected_sum)

if __name__ == '__main__':
    unittest.main()