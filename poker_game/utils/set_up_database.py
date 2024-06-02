""" Creating database """

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("logs/poker_game.db")
cursor = conn.cursor()

# there can only be six players at the table, so we can hardcode the number of players

# Create a table for games
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS games (
    game_id TEXT PRIMARY KEY,
    game_seed INTEGER,
    winner TEXT,
    seat_winner INTEGER,
    strategy_winner TEXT,
    number_of_rounds INTEGER,
    player_1 TEXT,
    player_2 TEXT,
    player_3 TEXT,
    player_4 TEXT,
    player_5 TEXT,
    player_6 TEXT
)
"""
)

# Create a table for rounds
cursor.execute(
    """
CREATE TABLE IF NOT EXISTS rounds (
    round_id TEXT PRIMARY KEY, 
    game_id TEXT,
    card_1_rank TEXT, 
    card_1_suit TEXT,
    card_2_rank TEXT,
    card_2_suit TEXT,
    card_3_rank TEXT,
    card_3_suit TEXT,
    card_4_rank TEXT,
    card_4_suit TEXT,
    card_5_rank TEXT,
    card_5_suit TEXT,
    FOREIGN KEY(game_id) REFERENCES games(game_id)
)
"""
)

# Create a table for active players
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS players (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        round_id TEXT,
        player_name TEXT,
        player_strategy TEXT,
        player_card_1_rank TEXT,
        player_card_1_suit TEXT,
        player_card_2_rank TEXT,
        player_card_2_suit TEXT,
        FOREIGN KEY(round_id) REFERENCES rounds(round_id)
    )
"""
)

# create a table for betting activities
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS betting_activities (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        round_id TEXT,
        player_name TEXT,
        amount INTEGER,
        FOREIGN KEY(round_id) REFERENCES rounds(round_id)
    )
"""
)

# create a table for Round winners
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS round_winners (
        activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
        round_id TEXT,
        winner TEXT,
        winner_amount INTEGER,
        FOREIGN KEY(round_id) REFERENCES rounds(round_id)
    )
"""
)
conn.commit()


def log_game(
    game_id,
    game_seed,
    winner,
    seat_winner,
    strategy_winner,
    number_of_rounds,
    player_1=None,
    player_2=None,
    player_3=None,
    player_4=None,
    player_5=None,
    player_6=None
):
    cursor.execute(
        "INSERT INTO games (game_id, game_seed, winner, seat_winner, strategy_winner, number_of_rounds, player_1, player_2, player_3, player_4, player_5, player_6) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (game_id, game_seed, winner, seat_winner, strategy_winner, number_of_rounds, player_1, player_2, player_3, player_4, player_5, player_6),
    )
    conn.commit()


def log_round_players_chips_cards(
    round_id=None,
    card_1_rank=None,
    card_1_suit=None,
    card_2_rank=None,
    card_2_suit=None,
    card_3_rank=None,
    card_3_suit=None,
    card_4_rank=None,
    card_4_suit=None,
    card_5_rank=None,
    card_5_suit=None,  # ,
    # player1_card_1_rank=None,
    # player1_card_1_suit=None,
    # player1_card_2_rank=None,
    # player1_card_2_suit=None,
    # player2_card_1_rank=None,
    # player2_card_1_suit=None,
    # player2_card_2_rank=None,
    # player2_card_2_suit=None,
    # player3_card_1_rank=None,
    # player3_card_1_suit=None,
    # player3_card_2_rank=None,
    # player3_card_2_suit=None,
    # player4_card_1_rank=None,
    # player4_card_1_suit=None,
    # player4_card_2_rank=None,
    # player4_card_2_suit=None,
    # player5_card_1_rank=None,
    # player5_card_1_suit=None,
    # player5_card_2_rank=None,
    # player5_card_2_suit=None,
    # player6_card_1_rank=None,
    # player6_card_1_suit=None,
    # player6_card_2_rank=None,
    # player6_card_2_suit=None,
    # player1_chips_end=None,
    # player2_chips_end=None,
    # player3_chips_end=None,
    # player4_chips_end=None,
    # player5_chips_end=None,
    # player6_chips_end=None,
    # , player1, player2, player3, player4, player5, player6, player1_card_1_rank, player1_card_1_suit, player1_card_2_rank, player1_card_2_suit, player2_card_1_rank, player2_card_1_suit, player2_card_2_rank, player2_card_2_suit, player3_card_1_rank, player3_card_1_suit, player3_card_2_rank, player3_card_2_suit, player4_card_1_rank, player4_card_1_suit, player4_card_2_rank, player4_card_2_suit, player5_card_1_rank, player5_card_1_suit, player5_card_2_rank, player5_card_2_suit, player6_card_1_rank, player6_card_1_suit, player6_card_2_rank, player6_card_2_suit, player1_chips_end, player2_chips_end, player3_chips_end, player4_chips_end, player5_chips_end, player6_chips_end
    # ,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?
):
    cursor.execute(
        "INSERT INTO rounds (round_id, card_1_rank, card_1_suit, card_2_rank, card_2_suit, card_3_rank, card_3_suit, card_4_rank, card_4_suit, card_5_rank, card_5_suit) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
        (
            round_id,
            card_1_rank,
            card_1_suit,
            card_2_rank,
            card_2_suit,
            card_3_rank,
            card_3_suit,
            card_4_rank,
            card_4_suit,
            card_5_rank,
            card_5_suit,  # ,
            # player1,
            # player2,
            # player3,
            # player4,
            # player5,
            # player6,
            # player1_card_1_rank,
            # player1_card_1_suit,
            # player1_card_2_rank,
            # player1_card_2_suit,
            # player2_card_1_rank,
            # player2_card_1_suit,
            # player2_card_2_rank,
            # player2_card_2_suit,
            # player3_card_1_rank,
            # player3_card_1_suit,
            # player3_card_2_rank,
            # player3_card_2_suit,
            # player4_card_1_rank,
            # player4_card_1_suit,
            # player4_card_2_rank,
            # player4_card_2_suit,
            # player5_card_1_rank,
            # player5_card_1_suit,
            # player5_card_2_rank,
            # player5_card_2_suit,
            # player6_card_1_rank,
            # player6_card_1_suit,
            # player6_card_2_rank,
            # player6_card_2_suit,
            # player1_chips_end,
            # player2_chips_end,
            # player3_chips_end,
            # player4_chips_end,
            # player5_chips_end,
            # player6_chips_end,
        ),
    )
    conn.commit()
    return cursor.lastrowid  # Get the new round ID after insertion


def log_active_players(
    round_id,
    player_name,
    player_strategy,
    player_card_1_rank,
    player_card_1_suit,
    player_card_2_rank,
    player_card_2_suit,
):
    cursor.execute(
        "INSERT INTO players (round_id, player_name, player_strategy, player_card_1_rank, player_card_1_suit, player_card_2_rank, player_card_2_suit) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            round_id,
            player_name,
            player_strategy,
            player_card_1_rank,
            player_card_1_suit,
            player_card_2_rank,
            player_card_2_suit,
        ),
    )
    conn.commit()


# def log_round_players_chips_cards(
#     round_id=None,
#     card_1_rank=None,
#     card_1_suit=None,
#     card_2_rank=None,
#     card_2_suit=None,
#     card_3_rank=None,
#     card_3_suit=None,
#     card_4_rank=None,
#     card_4_suit=None,
#     card_5_rank=None,
#     card_5_suit=None,
# ):
#     cursor.execute(
#         "INSERT INTO rounds (round_id, card_1_rank, card_1_suit, card_2_rank, card_2_suit, card_3_rank, card_3_suit, card_4_rank, card_4_suit, card_5_rank, card_5_suit) VALUES (?,?,?,?,?,?,?,?,?,?,?)",
#         (
#             round_id,
#             card_1_rank,
#             card_1_suit,
#             card_2_rank,
#             card_2_suit,
#             card_3_rank,
#             card_3_suit,
#             card_4_rank,
#             card_4_suit,
#             card_5_rank,
#             card_5_suit,
#         ),
#     )
#     conn.commit()
#     return cursor.lastrowid  # Get the new round ID after insertion


# def log_chips_player(chips_start, chips_end):
#     cursor.execute("INSERT INTO rounds (chips_start, chips_end) VALUES (?, ?)", (chips_start, chips_end))
#     conn.commit()


def log_cards_player(player_id, card_1_rank, card_1_suit, card_2_rank, card_2_suit):
    cursor.execute(
        "INSERT INTO players (player_id, card_1_rank, card_1_suit, card_2_rank, card_2_suit) VALUES (?, ?, ?, ?, ?)",
        (player_id, card_1_rank, card_1_suit, card_2_rank, card_2_suit),
    )
    conn.commit()


def log_betting_activity(round_id, player_name, amount):
    cursor.execute(
        "INSERT INTO betting_activities (round_id, player_name, amount) VALUES (?, ?, ?)",
        (round_id, player_name, amount),
    )
    conn.commit()


def log_round_winner(round_id, winner, winner_amount):
    cursor.execute(
        "INSERT INTO round_winners (round_id, winner, winner_amount) VALUES (?, ?, ?)",
        (round_id, winner, winner_amount),
    )
    conn.commit()
