# import requests
# import json

# def send_stock_data():
#     url = "http://127.0.0.1:8000/add_stock_data/"  # Replace with the actual URL of your Django view

#     # Example data to send
#     data = {
#         'symbol': 'SSSS',
#         'stock_data': [
#             {'Date': '2024-02-20', 'Open': 186.14999389648438, 'High': 186.85000610351562, 'Low': 184.69000244140625, 'Close': 185.02999877929688, 'Volume': 6457100, 'Dividends': 0.0, 'Stock_Splits': 0.0},
#             {'Date': '2024-02-18', 'Open': 153.0, 'High': 157.0, 'Low': 150.0, 'Close': 155.0, 'Volume': 1200000, 'Dividends': 0.0, 'Stock_Splits': 0.0},
#             # Add more data as needed
#         ]
#     }

#     # Convert data to JSON
#     json_data = json.dumps(data)

#     # Make the AJAX request
#     response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'})

#     # Check if the request was successful (status code 200)
#     if response.status_code == 200:
#         # Parse the JSON response
#         result = response.json()
#         print(result)
#     else:
#         # Handle errors
#         print(f"Error: {response.status_code} - {response.text}")

# if __name__ == "__main__":
#     send_stock_data()


import requests
import pandas as pd
import json

def send_stock_data_from_csv(csv_filename, symbol):
    url = "http://127.0.0.1:8000/add_stock_data/"  # Replace with the actual URL of your Django view

    # Read the CSV file into a pandas DataFrame
    # df = pd.read_csv(csv_filename)
    df = pd.read_csv(csv_filename, dtype={'Open': float})
    pd.set_option('display.float_format', '{:.6f}'.format)
    

    # Create a list of dictionaries from the DataFrame
    print("uploading data...")
    stock_data_list = []
    for index, row in df.iterrows():
        # print(row['Open'])
        stock_data = {
            'Date': row['Date'],
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

if __name__ == "__main__":
    symbol = 'IBM' # Replace with the desired stock symbol
    csv_filename = f"{symbol}.csv"  # Replace with the actual path to your CSV file

    send_stock_data_from_csv(csv_filename, symbol)
