# import requests

# def get_stock_data():
#     url = "http://127.0.0.1:8000/get_stock_data/"  # Replace with the actual URL of your Django view

#     # Parameters for the AJAX request
#     params = {
#         'symbol': 'MSFT',  # Replace with the desired stock symbol
#         'start_date': '2024-01-11',  # Replace with the desired start date
#         'end_date': '2024-02-16'  # Replace with the desired end date
#     }

#     # Make the AJAX request
#     response = requests.get(url, params=params)

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the JSON response
#         data = response.json()
#         stock_data = data.get('stock_data', [])
#         print(stock_data)
#     else:
#         # Handle errors
#         print(f"Error: {response.status_code} - {response.text}")

# if __name__ == "__main__":
#     get_stock_data()


import requests
import pandas as pd

def get_stock_data(symbol, start_date, end_date):
    url = "http://127.0.0.1:8000/get_stock_data/"  # Replace with the actual URL of your Django view

    # Parameters for the AJAX request
    params = {
        'symbol': symbol,
        'start_date': start_date,
        'end_date': end_date
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

        # Write the DataFrame to a CSV file
        csv_filename = f"{symbol}.csv"
        df['Date'] = pd.to_datetime(df['Date'])
        df.to_csv(csv_filename, index=False)
        print(df.head())

        print(f"Data has been written to {csv_filename}")
    else:
        # Handle errors
        print(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    symbol = 'MSFT'              # Replace with the desired stock symbol
    start_date = '2009-01-01'     # Replace with the desired start date
    end_date = '2024-04-01'      # Replace with the desired end date
    get_stock_data(symbol, start_date, end_date)
