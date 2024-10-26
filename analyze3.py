import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

def connect_to_database(db_name):
    """ Connect to the SQLite database. """
    return sqlite3.connect(db_name)

def fetch_currency_data(query, conn):
    """ Execute a SQL query and return the results as a DataFrame. """
    return pd.read_sql(query, conn)

def plot_currency_distribution(currency_data):
    """ Plot a pie chart of the currency distribution. """
    # Calculate total and percentage
    total_count = currency_data['count'].sum()
    currency_data['percentage'] = (currency_data['count'] / total_count) * 100

    # Create 'Others' category for currencies with less than 1%
    others_count = currency_data[currency_data['percentage'] < 1]['count'].sum()
    others_row = pd.DataFrame({'currency': ['Others'], 'count': [others_count]})
    
    # Filter out the 'Others' and keep the rest
    currency_data = currency_data[currency_data['percentage'] >= 1]._append(others_row, ignore_index=True)

    # Plotting
    plt.figure(figsize=(10, 8))  # Set figure size
    plt.pie(currency_data['count'], labels=currency_data['currency'], autopct='%1.1f%%', startangle=140)
    plt.title('Most Popular Currencies in the Database', fontsize=20)
    plt.axis('equal')  # Equal aspect ratio ensures that pie chart is circular.
    
    # Save and show the pie chart
    plt.savefig('currency_distribution.png', bbox_inches='tight')
    plt.show()

def main():
    # Connect to the buying habits database
    conn_habits = connect_to_database('buy_habits.db')

    # Query to get the count of each currency in the database
    currency_query = '''
    SELECT currency, COUNT(*) AS count
    FROM buying_habits
    GROUP BY currency
    ORDER BY count DESC
    '''

    # Fetch currency data
    currency_data = fetch_currency_data(currency_query, conn_habits)

    # Plot the currency distribution pie chart
    plot_currency_distribution(currency_data)

    # Close connection
    conn_habits.close()

if __name__ == "__main__":
    main()
