import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def connect_to_database(db_name):
    """ Connect to the SQLite database. """
    return sqlite3.connect(db_name)

def fetch_data(query, conn):
    """ Execute a SQL query and return the results as a DataFrame. """
    return pd.read_sql(query, conn)

def plot_average_price_by_genre(avg_price_data):
    """ Plot average price by genre with numbers in front of each bar. """
    plt.figure(figsize=(12, 8))
    bars = sns.barplot(data=avg_price_data, x='avg_price_usd', y='genre', hue='genre', palette='viridis', legend=False)
    
    for i, bar in enumerate(bars.patches):
        plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.2f}', 
                 va='center', ha='left', fontsize=10, fontweight='bold', color='black')

    plt.xlabel('Average Price (USD)', fontsize=14)
    plt.ylabel('Genre', fontsize=14)
    plt.title('Average Price (USD) by Genre', fontsize=16)
    plt.tight_layout()
    plt.savefig('avg_price_by_genre.png', bbox_inches='tight')
    plt.show()

def plot_top_developers(top_developers):
    """ Plot top developers based on game count with numbers on the bars. """
    plt.figure(figsize=(12, 8))
    bars = sns.barplot(data=top_developers, x='game_count', y='developer', hue='developer', palette='magma', legend=False)
    
    for i, bar in enumerate(bars.patches):
        plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.0f}', 
                 va='center', ha='left', fontsize=10, fontweight='bold', color='black')

    plt.xlabel('Number of Games', fontsize=14)
    plt.ylabel('Developer', fontsize=14)
    plt.title('Top Developers by Number of Games', fontsize=16)
    plt.tight_layout()
    plt.savefig('top_developers.png', bbox_inches='tight')
    plt.show()

def plot_top_publishers(top_publishers):
    """ Plot top publishers based on game count with numbers on the bars. """
    plt.figure(figsize=(12, 8))
    bars = sns.barplot(data=top_publishers, x='game_count', y='publisher', hue='publisher', palette='plasma', legend=False)
    
    for i, bar in enumerate(bars.patches):
        plt.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height() / 2, f'{bar.get_width():.0f}', 
                 va='center', ha='left', fontsize=10, fontweight='bold', color='black')

    plt.xlabel('Number of Games', fontsize=14)
    plt.ylabel('Publisher', fontsize=14)
    plt.title('Top Publishers by Number of Games', fontsize=16)
    plt.tight_layout()
    plt.savefig('top_publishers.png', bbox_inches='tight')
    plt.show()

def discount_analysis(discount_data):
    """ Print discount analysis results. """
    print("Average Price of Games on Sale (USD): {:.2f}".format(discount_data['avg_price_on_sale_usd'].values[0]))
    print("Average Price of Games After Discount (USD): {:.2f}".format(discount_data['avg_price_after_discount_usd'].values[0]))

def plot_genre_distribution(genre_distribution):
    """ Plot the genre distribution of games. """
    total_count = genre_distribution['count'].sum()
    genre_distribution['percentage'] = (genre_distribution['count'] / total_count) * 100
    genre_distribution.loc[genre_distribution['percentage'] < 3, 'genre'] = 'Other'
    genre_distribution = genre_distribution.groupby('genre', as_index=False).sum()

    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 8))
    plt.pie(genre_distribution['count'], labels=genre_distribution['genre'], autopct='%1.1f%%', startangle=140,
            colors=sns.color_palette("pastel", n_colors=len(genre_distribution)))
    plt.title('Genre Distribution of Games', fontsize=16)
    plt.axis('equal')
    plt.savefig('genre_distribution.png', bbox_inches='tight')
    plt.show()

def plot_average_playtime(average_playtime):
    """ Plot average playtime of the top 30 games. """
    plt.figure(figsize=(12, 8))
    bars = plt.barh(average_playtime['game_name'], average_playtime['average_playtime'], color=sns.color_palette("Set2", n_colors=30)[:len(average_playtime)])

    for i, bar in enumerate(bars):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{bar.get_width():.1f}', 
                 va='center', ha='left', fontsize=10, fontweight='bold', color='black')

    plt.xlabel('Average Playtime (Hours)', fontsize=14)
    plt.title('Top 30 Games by Average Playtime (Per Hour)', fontsize=16)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('average_playtime.png', bbox_inches='tight')
    plt.show()

def plot_most_owned_games(most_owned_games):
    """ Plot most owned games. """
    plt.figure(figsize=(12, 8))
    bars_owned = plt.barh(most_owned_games['game_name'], most_owned_games['owner_count'], color=sns.color_palette("Set2", n_colors=30)[:len(most_owned_games)])

    for i, bar in enumerate(bars_owned):
        plt.text(bar.get_width() + 1, bar.get_y() + bar.get_height()/2, f'{bar.get_width():d}', 
                 va='center', ha='left', fontsize=10, fontweight='bold', color='black')

    plt.xlabel('Number of Owners', fontsize=14)
    plt.title('Top 10 Most Owned Games', fontsize=16)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('most_owned_games.png', bbox_inches='tight')
    plt.show()

def plot_price_distribution(price_data):
    """ Plot the price distribution of games. """
    plt.figure(figsize=(12, 8))
    sns.histplot(price_data['price_usd'], bins=30, kde=True, color='blue')
    plt.xlabel('Price (USD)', fontsize=14)
    plt.ylabel('Frequency', fontsize=14)
    plt.title('Price Distribution of Games', fontsize=16)
    plt.tight_layout()
    plt.savefig('price_distribution.png', bbox_inches='tight')
    plt.show()

def plot_playtime_vs_price(playtime_price_data):
    """ Plot playtime vs price correlation. """
    plt.figure(figsize=(12, 8))
    sns.scatterplot(data=playtime_price_data, x='price_usd', y='average_playtime', color='orange')
    sns.regplot(data=playtime_price_data, x='price_usd', y='average_playtime', scatter=False, color='blue')
    plt.xlabel('Price (USD)', fontsize=14)
    plt.ylabel('Average Playtime (Hours)', fontsize=14)
    plt.title('Playtime vs Price Correlation', fontsize=16)
    plt.tight_layout()
    plt.savefig('playtime_vs_price_correlation.png', bbox_inches='tight')
    plt.show()

def main():
    # Connect to the buying habits database
    conn_habits = connect_to_database('buy_habits.db')

    # Queries
    genre_query = '''
    SELECT json_each.value AS genre, COUNT(*) AS count
    FROM buying_habits, json_each(genres)
    GROUP BY genre
    ORDER BY count DESC
    '''

    playtime_query = '''
    SELECT game_name, AVG(playtime) AS average_playtime
    FROM buying_habits
    GROUP BY game_name
    HAVING COUNT(DISTINCT steam_id) > 30
    ORDER BY average_playtime DESC
    LIMIT 30
    '''

    most_owned_query = '''
    SELECT game_name, COUNT(*) AS owner_count
    FROM buying_habits
    GROUP BY game_name
    ORDER BY owner_count DESC
    LIMIT 10
    '''

    avg_playtime_by_genre_query = '''
    SELECT genre.value AS genre, AVG(playtime) AS avg_playtime
    FROM buying_habits
    JOIN json_each(genres) AS genre ON 1=1
    GROUP BY genre.value
    ORDER BY avg_playtime DESC
    '''

    # Query to get average price by genre
    avg_price_by_genre_query = '''
    SELECT genre.value AS genre, AVG(price_usd) AS avg_price_usd
    FROM buying_habits
    JOIN json_each(genres) AS genre ON 1=1
    GROUP BY genre.value
    ORDER BY avg_price_usd ASC
    '''

    # Query to get top developers
    top_developers_query = '''
    SELECT developer, COUNT(*) AS game_count
    FROM buying_habits
    GROUP BY developer
    ORDER BY game_count DESC
    LIMIT 10
    '''

    # Query to get top publishers
    top_publishers_query = '''
    SELECT publisher, COUNT(*) AS game_count
    FROM buying_habits
    GROUP BY publisher
    ORDER BY game_count DESC
    LIMIT 10
    '''

    # Query for discount analysis
    discount_analysis_query = '''
    SELECT 
        AVG(price_usd) AS avg_price_on_sale_usd,
        AVG(price_usd * (1 - discount_percentage / 100.0)) AS avg_price_after_discount_usd
    FROM buying_habits
    WHERE discount_percentage > 0
    '''

    # Fetch data
    genre_distribution = fetch_data(genre_query, conn_habits)
    average_playtime = fetch_data(playtime_query, conn_habits)
    most_owned_games = fetch_data(most_owned_query, conn_habits)
    avg_playtime_by_genre = fetch_data(avg_playtime_by_genre_query, conn_habits)
    avg_price_data = fetch_data(avg_price_by_genre_query, conn_habits)
    top_developers = fetch_data(top_developers_query, conn_habits)
    top_publishers = fetch_data(top_publishers_query, conn_habits)
    discount_data = fetch_data(discount_analysis_query, conn_habits)

    # Price Distribution Analysis
    price_data = fetch_data("SELECT price_usd FROM buying_habits", conn_habits)
    plot_price_distribution(price_data)

    # Playtime vs Price Correlation
    playtime_price_data = fetch_data("SELECT AVG(playtime) AS average_playtime, AVG(price_usd) AS price_usd FROM buying_habits GROUP BY game_name", conn_habits)
    plot_playtime_vs_price(playtime_price_data)

    # Visualization
    plot_average_price_by_genre(avg_price_data)
    plot_top_developers(top_developers)
    plot_top_publishers(top_publishers)
    discount_analysis(discount_data)
    plot_genre_distribution(genre_distribution)
    plot_average_playtime(average_playtime)
    plot_most_owned_games(most_owned_games)

    # Close connection
    conn_habits.close()

if __name__ == "__main__":
    main()
