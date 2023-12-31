from poker_game.play_game import play_game
from poker_game.utils.players import Player
from utils.table import Table
from utils.game import TexasHoldemGame
from utils.objects_on_table import Chips, Deck
# from utils.start_round import start_round

if __name__ == "__main__":
    # Create a deck and a table
    deck = Deck()
    table = Table()

    # Ask for player names
    player1_name = input("Enter name for Player 1: ")
    player2_name = input("Enter name for Player 2: ")

    # Create players and add them to the table
    player1 = Player(player1_name, chips=Chips(100))
    player2 = Player(player2_name, chips=Chips(100))
    table.add_player(player1)
    table.add_player(player2)

    # Start the Texas Hold'em round
    # texas_holdem_game = TexasHoldemGame(table, deck)
    play_game(table, seed=1)