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

def plot_spending_by_game(spending_data):
    """ Plot total spending by game with numbers on the bars. """
    plt.figure(figsize=(16, 12))  # Increased figure size
    bars = sns.barplot(data=spending_data, x='total_spending', y='game_name', palette='viridis', ci=None)
    
    # Annotate bars with total spending values
    for bar in bars.patches:
        total_spending = bar.get_width()
        y_pos = bar.get_y() + bar.get_height() / 2
        
        if total_spending < 100:
            plt.text(total_spending + 0.5, y_pos, f'{total_spending:.2f}', 
                     va='center', ha='left', fontsize=12, fontweight='bold', color='black')
        else:
            plt.text(total_spending - 10, y_pos, f'{total_spending:.2f}', 
                     va='center', ha='right', fontsize=12, fontweight='bold', color='black')

    plt.xlabel('Total Spending (USD)', fontsize=16)
    plt.ylabel('Game Name', fontsize=16)
    plt.title('Total Spending by Game', fontsize=20)
    plt.xlim(0, spending_data['total_spending'].max() + 20)
    plt.tight_layout(pad=5.0)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.savefig('total_spending_by_game.png', bbox_inches='tight')
    plt.show()

def plot_average_price_by_game(average_price_data):
    """ Plot average price spent by game with numbers on the bars. """
    plt.figure(figsize=(16, 12))  # Increased figure size
    bars = sns.barplot(data=average_price_data, x='average_price', y='game_name', palette='plasma', ci=None)

    # Annotate bars with average price values
    for bar in bars.patches:
        average_price = bar.get_width()
        y_pos = bar.get_y() + bar.get_height() / 2
        
        if average_price < 10:
            plt.text(average_price + 0.1, y_pos, f'{average_price:.2f}', 
                     va='center', ha='left', fontsize=12, fontweight='bold', color='black')
        else:
            plt.text(average_price - 0.5, y_pos, f'{average_price:.2f}', 
                     va='center', ha='right', fontsize=12, fontweight='bold', color='black')

    plt.xlabel('Average Price (USD)', fontsize=16)
    plt.ylabel('Game Name', fontsize=16)
    plt.title('Average Price Spent by Game', fontsize=20)
    plt.xlim(0, average_price_data['average_price'].max() + 5)  # Set x-axis limit with some padding
    plt.tight_layout(pad=5.0)
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.savefig('average_price_by_game.png', bbox_inches='tight')
    plt.show()

def main():
    # Connect to the buying habits database
    conn_habits = connect_to_database('buy_habits.db')

    # Query to get total spending by game
    total_spending_query = '''
    SELECT game_name, SUM(price_usd) AS total_spending
    FROM buying_habits
    GROUP BY game_name
    ORDER BY total_spending DESC
    LIMIT 20
    '''

    # Fetch total spending data
    total_spending_data = fetch_data(total_spending_query, conn_habits)

    # Plot total spending by game
    plot_spending_by_game(total_spending_data)

    # Query to get average price spent by game
    average_price_query = '''
    SELECT game_name, AVG(price_usd) AS average_price
    FROM buying_habits
    GROUP BY game_name
    ORDER BY average_price DESC
    LIMIT 20
    '''

    # Fetch average price data
    average_price_data = fetch_data(average_price_query, conn_habits)

    # Plot average price by game
    plot_average_price_by_game(average_price_data)

    # Close connection
    conn_habits.close()

if __name__ == "__main__":
    main()
