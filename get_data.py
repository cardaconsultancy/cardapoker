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
SELECT player_type, COUNT(*) as count
FROM (
    SELECT player_1 as player_type FROM games
    UNION ALL
    SELECT player_2 FROM games
    UNION ALL
    SELECT player_3 FROM games
    UNION ALL
    SELECT player_4 FROM games
    UNION ALL
    SELECT player_5 FROM games
    UNION ALL
    SELECT player_6 FROM games
) AS player_types
GROUP BY player_type
ORDER BY count DESC
"""


cursor.execute(PLAYER_DISTRIBUTION)
QUERY = cursor.fetchall()
print('Query result', QUERY)