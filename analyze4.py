import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def connect_to_database(db_name):
    """ Connect to the SQLite database. """
    return sqlite3.connect(db_name)

def fetch_data(query, conn):
    """ Execute a SQL query and return the results as a DataFrame. """
    return pd.read_sql(query, conn)

def plot_playtime_vs_price_scatter(playtime_price_data):
    """ Scatter plot for playtime vs price correlation with log scale for readability. """
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=playtime_price_data, x='price_usd', y='average_playtime', color='orange', alpha=0.6)
    sns.regplot(data=playtime_price_data, x='price_usd', y='average_playtime', scatter=False, color='blue', logx=True)
    plt.xscale('log')
    plt.yscale('log')
    plt.xlabel('Price (USD)')
    plt.ylabel('Average Playtime (Hours)')
    plt.title('Playtime vs Price Correlation (Log Scale)')
    plt.tight_layout()
    plt.savefig('playtime_vs_price_log_correlation.png', bbox_inches='tight')
    plt.show()

def plot_playtime_for_free_games(playtime_free_games):
    """ Bar plot for average playtime of free games. """
    plt.figure(figsize=(10, 6))
    bars = sns.barplot(data=playtime_free_games, x='game_name', y='average_playtime', palette='coolwarm')
    plt.xticks(rotation=90)
    plt.xlabel('Game Name')
    plt.ylabel('Average Playtime (Hours)')
    plt.title('Playtime of Free Games')
    plt.tight_layout()
    plt.savefig('playtime_for_free_games.png', bbox_inches='tight')
    plt.show()

def plot_playtime_by_price_category(playtime_price_category_data):
    """ Violin plot to show distribution of playtime across price categories. """
    plt.figure(figsize=(12, 8))
    sns.violinplot(data=playtime_price_category_data, x='price_category', y='average_playtime', scale='width', palette='pastel')
    plt.yscale('log')
    plt.xlabel('Price Category')
    plt.ylabel('Average Playtime (Log Scale)')
    plt.title('Playtime Distribution by Price Category')
    plt.tight_layout()
    plt.savefig('playtime_by_price_category.png', bbox_inches='tight')
    plt.show()

def categorize_price(row):
    """ Categorize price into ranges for visualization. """
    if row['price_usd'] == 0:
        return 'Free'
    elif row['price_usd'] <= 5:
        return '$1 - $5'
    elif row['price_usd'] <= 20:
        return '$6 - $20'
    elif row['price_usd'] <= 50:
        return '$21 - $50'
    else:
        return 'Above $50'

def main():
    conn_habits = connect_to_database('buy_habits.db')

    # Query to get playtime and price for all games
    playtime_price_query = '''
    SELECT AVG(playtime) AS average_playtime, price_usd
    FROM buying_habits
    GROUP BY game_name
    '''
    
    # Query to get playtime data for free games
    free_games_query = '''
    SELECT game_name, AVG(playtime) AS average_playtime
    FROM buying_habits
    WHERE price_usd = 0
    GROUP BY game_name
    ORDER BY average_playtime DESC
    LIMIT 20
    '''

    # Fetch data
    playtime_price_data = fetch_data(playtime_price_query, conn_habits)
    playtime_price_data = playtime_price_data[playtime_price_data['price_usd'] > 0]  # Exclude free games for scatter plot
    playtime_free_games = fetch_data(free_games_query, conn_habits)
    
    # Add price categories to playtime-price data
    playtime_price_data['price_category'] = playtime_price_data.apply(categorize_price, axis=1)
    
    # Violin plot data by price category
    playtime_price_category_data = playtime_price_data[['price_category', 'average_playtime']].copy()
    
    # Visualizations
    plot_playtime_vs_price_scatter(playtime_price_data)
    plot_playtime_for_free_games(playtime_free_games)
    plot_playtime_by_price_category(playtime_price_category_data)

    # Close the database connection
    conn_habits.close()

if __name__ == "__main__":
    main()
