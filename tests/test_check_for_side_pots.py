import unittest
from poker_game.utils.players import Player, ActualPlayerTemplate, create_player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Deck, Chips, Card, Pot
from poker_game.utils.game import TexasHoldemGame
from poker_game.utils.pot_management import check_for_side_pots

class TestTexasHoldemGame(unittest.TestCase):
    def test_play_round(self, p1bet=20):
        deck = Deck()
        table = Table()
        pot = Pot()

        player1 = create_player("John Doe", Chips(50))
        player2 = Player("Jan", Chips(0))
        player3 = Player("Piet", Chips(0))
        player2.all_in = True
        player3.all_in = True

        player1.total_bet_betting_round = p1bet
        player2.total_bet_betting_round = 50
        player3.total_bet_betting_round = 10
        
        pot.players = [player1, player2, player3]
        pot.amount = 0

        table.pots.append(pot)

        table.add_player(player1)
        table.add_player(player2)
        table.add_player(player3)

        game = TexasHoldemGame(table, deck)
        check_for_side_pots(table)

        # check if pots are the sum of the bets
        self.assertEqual(0, sum([player1.total_bet_betting_round, player2.total_bet_betting_round, player3.total_bet_betting_round]))

        # check if all bets are reduced to zero in the end
        self.assertEqual(0, sum([player1.total_bet_betting_round, player2.total_bet_betting_round, player3.total_bet_betting_round]))


# if __name__ == '__main__':
#     unittest.main()