import requests
import pandas as pd
from datetime import datetime, timedelta
import yfinance as yf
import json


def get_stock_data_from_db(symbol):
    url = "http://127.0.0.1:8000/get_stock_data/"  # Replace with the actual URL of your Django view

    # Get the current date and time
    current_date = datetime.now()
    # Calculate the date of 10 days ago
    from_date = current_date - timedelta(days=30)
    to_date = current_date + timedelta(days=1)


    # Parameters for the AJAX request
    params = {
        'symbol': symbol,
        'start_date': from_date.strftime("%Y-%m-%d"),  # Fetch all data
        'end_date': to_date.strftime("%Y-%m-%d")
    }

    # Make the AJAX request
    response = requests.get(url, params=params)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        stock_data = data.get('stock_data', [])

        # Create a DataFrame from the list of dictionaries
        df = pd.DataFrame(stock_data)
        df['Date'] = pd.to_datetime(df['Date'])  # Convert Date column to datetime
        last_date = df.iloc[-1]
        last_date = last_date['Date']
        last_date = str(last_date)
        datetime_object = datetime.strptime(last_date, "%Y-%m-%d %H:%M:%S%z")
        date_only = datetime_object.date()
        # Convert date back to string
        date_only_string = date_only.strftime("%Y-%m-%d")

        return date_only_string
    else:
        # Handle errors
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_stock_data_from_yahoo(symbol, selected_date):
    try:
        print(selected_date)
        # Convert the selected date string to a datetime object
        selected_date_object = datetime.strptime(selected_date, "%Y-%m-%d")
        selected_date_object = selected_date_object + timedelta(days=1)
        current_date = datetime.now() + timedelta(days=1)

        # Fetch historical data from Yahoo Finance using yfinance
        ticker = yf.Ticker(symbol)

        # Set the start date to the selected date
        historical_data = ticker.history(start=selected_date_object, end=current_date)

        if not historical_data.empty:
            return historical_data
        else:
            print(f"No data available for {symbol} on {selected_date}")
            return None

    except Exception as e:
        print(f"Failed to fetch data from Yahoo Finance for {symbol}: {e}")
        return None

def send_stock_data(symbol, data_frame):
    url = "http://127.0.0.1:8000/add_stock_data/"  # Replace with the actual URL of your Django view

    df = pd.DataFrame(data_frame)

    # Create a list of dictionaries from the DataFrame
    stock_data_list = []
    for index, row in df.iterrows():
        print(row['Open'])
        stock_data = {
            'Date': index.strftime('%Y-%m-%d'),
            'Open': row['Open'],
            'High': row['High'],
            'Low': row['Low'],
            'Close': row['Close'],
            'Volume': row['Volume'],
            'Dividends': row['Dividends'],
            'Stock_Splits': row['Stock Splits']
        }
        stock_data_list.append(stock_data)

    # Prepare the data to send
    data = {
        'symbol': symbol,
        'stock_data': stock_data_list
    }

    # Convert data to JSON
    json_data = json.dumps(data)

    # Make the AJAX request
    response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the JSON response
        result = response.json()
        print(result)
    else:
        # Handle errors
        print(f"Error: {response.status_code} - {response.text}")

def update_symbol(symbol=None):
    if(symbol == None):
        return
    print(symbol, ":")
    selected_date = get_stock_data_from_db(symbol)
    df = get_stock_data_from_yahoo(symbol, selected_date)
    if df is None:
        print(f"No data available for {symbol} on {selected_date}")
    elif df.empty:
        print(f"{symbol} is already updated!!!")
    else:
        send_stock_data(symbol, df)

if __name__ == "__main__":
    symbols = ['MSFT', 'AAPL', 'TSLA', 'IBM']
    for symbol in symbols:
        update_symbol(symbol)
    

