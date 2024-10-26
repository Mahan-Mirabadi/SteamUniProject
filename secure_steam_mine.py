import requests
import sqlite3
import json
import time

# Prompt the user for Steam API key and Steam ID when running the script
API_KEY = input("Please enter your Steam API Key: ")

# Option to use a specific Steam ID or fetch all from the database
USE_SPECIFIC_STEAM_ID = input("Do you want to use a specific Steam ID? (yes/no): ").strip().lower() == 'yes'
SPECIFIC_STEAM_ID = None
if USE_SPECIFIC_STEAM_ID:
    SPECIFIC_STEAM_ID = input("Please enter the specific Steam ID: ")

# Connect to the existing SQLite databases
conn_users = sqlite3.connect('steam_users.db')
cursor_users = conn_users.cursor()

conn_habits = sqlite3.connect('buy_habits.db')
cursor_habits = conn_habits.cursor()

# Create the buying_habits table with review-related columns
cursor_habits.execute(''' 
CREATE TABLE IF NOT EXISTS buying_habits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    steam_id TEXT NOT NULL,
    game_name TEXT,
    app_id INTEGER,
    playtime REAL,
    genres TEXT,
    on_sale BOOLEAN,
    price REAL,
    discount_percentage REAL,
    release_date TEXT,
    developer TEXT,
    publisher TEXT,
    metacritic_score INTEGER,
    platforms TEXT,
    currency TEXT,
    steam_rating REAL,
    number_of_reviews INTEGER,
    tags TEXT
)
''')

# Decide which Steam IDs to process
if USE_SPECIFIC_STEAM_ID:
    users = [(SPECIFIC_STEAM_ID,)]
    print(f"Using specific Steam ID: {SPECIFIC_STEAM_ID}")
else:
    cursor_users.execute('SELECT steam_id FROM steam_users')
    users = cursor_users.fetchall()
    print(f"Fetched {len(users)} Steam IDs from the database.")

api_call_count = 0

for steam_id_counter, user in enumerate(users, 1):
    steam_id = user[0]
    print(f"[{steam_id_counter}] Processing Steam ID: {steam_id}")

    cursor_habits.execute('SELECT COUNT(*) FROM buying_habits WHERE steam_id = ?', (steam_id,))
    if cursor_habits.fetchone()[0] > 0:
        print(f"Buying habits for Steam ID {steam_id} already exist, skipping...")
        continue

    url = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/?key={API_KEY}&steamid={steam_id}&include_appinfo=1&include_played_free_games=1"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'response' in data and 'games' in data['response']:
            games = data['response']['games']
            print(f"Found {len(games)} games for Steam ID: {steam_id}")

            for game in games:
                appid = game.get('appid')
                game_name = game.get('name')
                playtime = game.get('playtime_forever') / 60  # Convert to hours

                if playtime > 100000:
                    print(f"WARNING: High playtime for {game_name} ({playtime:.2f} hours) - skipping...")
                    continue

                # Initialize store data variables
                genres, on_sale, price, discount_percentage = [], False, None, None
                release_date, developer, publisher, metacritic_score = None, None, None, None
                platforms, steam_rating, number_of_reviews, tags = None, None, None, []

                try:
                    store_url = f'https://store.steampowered.com/api/appdetails?appids={appid}'
                    store_response = requests.get(store_url)
                    api_call_count += 1
                    store_data = store_response.json()

                    if not store_data or str(appid) not in store_data or not store_data[str(appid)]['success']:
                        raise ValueError(f"Failed to fetch valid data for appid {appid}")

                    app_data = store_data[str(appid)]['data']
                    genres = [genre['description'] for genre in app_data.get('genres', [])]
                    on_sale = app_data.get('is_free', False)
                    price_info = app_data.get('price_overview', {})
                    price = price_info.get('final', 0) / 100
                    discount_percentage = price_info.get('discount_percent', 0)
                    release_date = app_data.get('release_date', {}).get('date')
                    developer = app_data.get('developers', [None])[0]
                    publisher = app_data.get('publishers', [None])[0]
                    metacritic_score = app_data.get('metacritic', {}).get('score')
                    platforms = ', '.join(app_data.get('platforms', {}).keys())
                    tags = app_data.get('categories', [])

                    # Fetch review data
                    steam_rating = app_data.get('review_score', None)
                    number_of_reviews = app_data.get('reviews_count', None)

                    cursor_habits.execute(''' 
                    INSERT INTO buying_habits (steam_id, game_name, app_id, playtime, genres, on_sale, price, 
                                               discount_percentage, release_date, developer, publisher, 
                                               metacritic_score, platforms, currency, steam_rating, 
                                               number_of_reviews, tags)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        steam_id, game_name, appid, playtime, json.dumps(genres), on_sale,
                        f"{price:.2f}" if price is not None else None, discount_percentage,
                        release_date, developer, publisher, metacritic_score, platforms, "USD",
                        steam_rating, number_of_reviews, json.dumps(tags)
                    ))
                    print(f"Inserted data for {game_name} (appid: {appid})")

                except (requests.exceptions.RequestException, ValueError) as e:
                    print(f"Error for {game_name}: {e}. Skipping...")

            conn_habits.commit()
            print(f"Updated buying habits for Steam ID: {steam_id}")

        else:
            print(f"No games found for Steam ID {steam_id}")
    else:
        print(f"Failed to fetch games for Steam ID {steam_id}: {response.status_code}")

    time.sleep(1)

conn_habits.close()
conn_users.close()
print(f"Finished processing. Total Steam API calls made: {api_call_count}")
