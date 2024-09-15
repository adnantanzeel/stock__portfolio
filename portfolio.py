import random
import requests
import pandas as pd

# Constants for API and base URL
API_KEY = '7ewdqewjrjwq8weq/q]ewqmoiewfwqnmcew23832rn2'
BASE_URL = 'https://www.alphavantage.co/query'

# Stock portfolio
portfolio = {}

# Function to get real-time stock data
def get_stock_data(symbol):
    params = {
        'function': 'TIME_SERIES_INTRADAY',
        'symbol': symbol,
        'interval': '5min',
        'apikey': API_KEY
    }
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    if "Time Series (5min)" not in data:
        print(f"Error fetching data for {symbol}. Check if the stock symbol is correct.")
        return None
    
    latest_time = next(iter(data["Time Series (5min)"]))
    latest_data = data["Time Series (5min)"][latest_time]
    price = float(latest_data['4. close'])
    
    return price

# Function to add a stock to the portfolio
def add_stock(symbol, quantity, purchase_price):
    curprice=random.randint(int(purchase_price/5),int(purchase_price*10))
    purprice=purchase_price
    portfolio[symbol] = {
        'quantity': quantity,
        'purchase_price': purchase_price,
        'current_price': curprice,
        'performance': f"{purprice/curprice*100:.2f}%"
    }

# Function to remove a stock from the portfolio
def remove_stock(symbol):
    if symbol in portfolio:
        del portfolio[symbol]
        print(f"{symbol} removed from portfolio.")
    else:
        print(f"{symbol} not found in portfolio.")

# Function to update current prices and performance of each stock
def update_portfolio():
    for symbol in portfolio:
        current_price = get_stock_data(symbol)
        if current_price:
            portfolio[symbol]['current_price'] = current_price
            purchase_price = portfolio[symbol]['purchase_price']
            quantity = portfolio[symbol]['quantity']
            performance = ((current_price - purchase_price) / purchase_price) * 100
            portfolio[symbol]['performance'] = round(performance, 2)

# Function to display the portfolio
def display_portfolio():
    if not portfolio:
        print("Portfolio is empty.")
        return
    
    df = pd.DataFrame(portfolio).T
    df['total_value'] = df['quantity'] * df['current_price']
    print(df[['quantity', 'purchase_price', 'current_price', 'performance', 'total_value']])

# Main loop for user interaction
def main():
    while True:
        print("\nStock Portfolio Menu:")
        print("1. Add Stock")
        print("2. Remove Stock")
        print("3. View Portfolio")
        print("4. Update Portfolio")
        print("5. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            symbol = input("Enter stock symbol: ").upper()
            quantity = int(input("Enter quantity: "))
            purchase_price = float(input("Enter purchase price: "))
            add_stock(symbol, quantity, purchase_price)
        
        elif choice == '2':
            symbol = input("Enter stock symbol to remove: ").upper()
            remove_stock(symbol)
        
        elif choice == '3':
            display_portfolio()
        
        elif choice == '4':
            update_portfolio()
            print("Portfolio updated.")
        
        elif choice == '5':
            print("Exiting portfolio tracker.")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
