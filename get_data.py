import sqlite3
import json

# Connect to the SQLite database
conn = sqlite3.connect('poker_game.db')
cursor = conn.cursor()

cursor.execute("SELECT * FROM rounds")
round_activities = cursor.fetchall()
print('round_activities', round_activities)

# for activity in activities:
#     print('a', activity[1])
    # action_detail = json.loads(activity[2])  # Decode the JSON data
    # print(action_detail)

# cursor.execute("SELECT * FROM betting_activities")
# activities = cursor.fetchall()

# for activity in activities:
#     print(activity)