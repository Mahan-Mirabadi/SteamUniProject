import requests
import time
import sqlite3

API_KEY = input("Please enter your Steam API Key: ")
START_USER_ID = input("Please Enter Your Starting Steam ID: ")
MAX_USERS = 3000

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('steam_users.db')
cursor = conn.cursor()

# Create table for Steam IDs
cursor.execute('''
CREATE TABLE IF NOT EXISTS steam_users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    steam_id TEXT UNIQUE
)
''')

# Commit the changes
conn.commit()

steam_ids = set()  # To store unique Steam IDs
user_queue = [START_USER_ID]  # Queue to process

def save_steam_id(steam_id):
    """Saves a new Steam ID to the SQLite database."""
    try:
        cursor.execute('INSERT OR IGNORE INTO steam_users (steam_id) VALUES (?)', (steam_id,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"Error saving Steam ID {steam_id}: {e}")

def get_friends(steam_id):
    """Fetches the friends list of a given Steam ID."""
    url = f"http://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={API_KEY}&steamid={steam_id}&relationship=friend"
    response = requests.get(url)
    if response.status_code == 200:
        friends_data = response.json()
        if 'friendslist' in friends_data:
            return [friend['steamid'] for friend in friends_data['friendslist']['friends']]
    return []

# Fetch Steam IDs and save to database
while len(steam_ids) < MAX_USERS and user_queue:
    current_id = user_queue.pop(0)
    
    if current_id not in steam_ids:
        steam_ids.add(current_id)
        save_steam_id(current_id)  # Save the ID to the database
        print(f"Collected: {len(steam_ids)} / {MAX_USERS}")
        
        # Get friends and add them to the queue
        friends = get_friends(current_id)
        user_queue.extend(friends)
        
        # To avoid hitting API rate limits
        time.sleep(1)

# Close the SQLite connection when done
conn.close()

print("Done!")
