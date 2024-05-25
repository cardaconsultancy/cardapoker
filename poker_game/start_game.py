from poker_game.play_game import play_game
from poker_game.utils.players import Player
from poker_game.utils.table import Table
from poker_game.utils.objects_on_table import Chips, Deck

if __name__ == "__main__":
    # Create a deck and a table
    deck = Deck()
    table = Table()

    # Ask for player names
    # player1_name = input("Enter name for Player 1: ")
    # player2_name = input("Enter name for Player 2: ")

    # Create players and add them to the table
    player1 = Player("A", chips=Chips(100))
    player2 = Player("B", chips=Chips(100))
    player3 = Player("C", chips=Chips(100))
    player4 = Player("D", chips=Chips(100))
    table.add_player(player1)
    table.add_player(player2)
    table.add_player(player3)
    table.add_player(player4)

    # Start the Texas Hold'em game
    play_game(table, seed=2)
