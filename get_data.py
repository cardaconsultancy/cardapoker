import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('logs/poker_game.db')
cursor = conn.cursor()

# cursor.execute("SELECT * FROM games")
# game_activities = cursor.fetchall()
# print('game_activities', game_activities)

# cursor.execute("SELECT * FROM rounds")
# round_activities = cursor.fetchall()
# print('round_activities', round_activities)

# cursor.execute("SELECT * FROM players")
# active_players = cursor.fetchall()
# print('players', active_players)

# cursor.execute("SELECT * FROM betting_activities")
# betting_activities = cursor.fetchall()
# print('betting_activities', betting_activities)

# cursor.execute("SELECT * FROM round_winners")
# round_winners = cursor.fetchall()
# print('round_winners', round_winners)

# try some SQL queries

WINNING_STRATEGY_QUERY = """
SELECT strategy_winner,
count(*) as nr_of_games
FROM games
group by strategy_winner
order by nr_of_games
DESC
"""

WINNING_SEAT_QUERY = """
SELECT seat_winner,
count(*) as nr_of_games
FROM games
group by seat_winner
order by nr_of_games
DESC
"""

PLAYER_DISTRIBUTION = """
SELECT seat_winner,
count(*) as nr_of_games
FROM games
group by seat_winner
order by nr_of_games
DESC
"""


cursor.execute(WINNING_STRATEGY_QUERY)
WINNING_STRATEGY_QUERY = cursor.fetchall()
print('Query result', WINNING_STRATEGY_QUERY)