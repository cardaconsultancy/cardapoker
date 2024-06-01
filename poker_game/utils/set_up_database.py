""" Creating database """

import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("poker_game.db")
cursor = conn.cursor()

# Create a table for rounds
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS rounds (
        round_id TEXT PRIMARY KEY, 
        card_1_rank TEXT, 
        card_1_suit TEXT,
        card_2_rank TEXT,
        card_2_suit TEXT,
        card_3_rank TEXT,
        card_3_suit TEXT,
        card_4_rank TEXT,
        card_4_suit TEXT,
        card_5_rank TEXT,
        card_5_suit TEXT
    )
"""
)

# # create a table for players
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS players_hands (
#         round_id TEXT PRIMARY KEY,
#         card_1_rank TEXT,
#         card_1_suit TEXT,
#         card_2_rank TEXT,
#         card_2_suit TEXT,
#         chips_start INTEGER,
#         chips_end INTEGER
#         FOREIGN KEY(round_id) REFERENCES rounds(round_id)
#     )
# ''')

# # Create a table for betting activities
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS betting_activities (
#         activity_id INTEGER PRIMARY KEY AUTOINCREMENT,
#         player_name TEXT,
#         amount INTEGER,
#         FOREIGN KEY(round_id) REFERENCES rounds(round_id)
#     )
# ''')

conn.commit()


def log_round_and_communal_cards(
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
    card_5_suit=None,
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
            card_5_suit,
        ),
    )
    conn.commit()
    return cursor.lastrowid  # Get the new round ID after insertion


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
