from poker_game.utils.players import Player
from utils.table import Table
from utils.game import TexasHoldemGame
from utils.objects_on_table import Deck

# Example usage:
if __name__ == "__main__":
    # Create a deck and a table
    deck = Deck()
    table = Table()

    # Create players and add them to the table
    player1 = Player("Player 1")
    player2 = Player("Player 2")
    table.add_player(player1)
    table.add_player(player2)

    # Start the Texas Hold'em game
    texas_holdem_game = TexasHoldemGame(table, deck)
    texas_holdem_game.start_round()

    # Display the current state of the table
    texas_holdem_game.display_table()