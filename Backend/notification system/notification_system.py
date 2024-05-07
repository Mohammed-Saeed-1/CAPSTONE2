import mysql.connector
from datetime import datetime
import yfinance as yf

symbols_to_notified = []

PERCENT = 10 #to send message, the price percent change should be either >= PERCENT% or <= -PERCENT%

# Connect to MySQL database
mydb = mysql.connector.connect(
    host="utrade-db-1.c5iagq4kq5e6.us-west-2.rds.amazonaws.com",
    user="admin",
    password="utradedb123",
    database="utradedb"
)

# Get cursor
mycursor = mydb.cursor()

def update_stock_data(symbol):
    try:
        # Get today's date
        today_date = datetime.now().strftime("%Y-%m-%d")

        # Check if symbol exists in the database
        sql_select = "SELECT * FROM notification WHERE symbol = %s"
        mycursor.execute(sql_select, (symbol,))
        result = mycursor.fetchone()

        if result:
            # print(result)
            # If the date in the database is not today's date, update the data
            if result[2].strftime("%Y-%m-%d") != today_date:
                open_day_price = float([yf.Ticker(symbol).history(period="1d", interval="1m")["Open"].iloc[0]][0])

                # Update data in database
                sql_update = "UPDATE notification SET Open = %s, Date = %s WHERE symbol = %s"
                val = (open_day_price, today_date, symbol)
                mycursor.execute(sql_update, val)

                # Commit changes
                mydb.commit()
                print(f"Data for symbol {symbol} updated successfully.")

                symbols_to_notified.append([symbol, 0.0])
            else:
                print(f"Data for symbol {symbol} is already up to date.")
                
                open_day_price = float(result[1])
                # print(open_day_price)

                current_minute_price = float([yf.Ticker(symbol).history(period="1d", interval="1m")["Close"].iloc[-1]][0])
                current_minute_price = round(current_minute_price, 2)
                # print(current_minute_price)

                percent_change = ((current_minute_price - open_day_price) / open_day_price) * 100
                percent_change = round(percent_change, 2)
                # print(percent_change)

                if percent_change >= PERCENT or percent_change <= -PERCENT:
                    # Update open price in database with the new open price (current_minute_price)
                    sql_update = "UPDATE notification SET Open = %s WHERE symbol = %s"
                    val = (current_minute_price, symbol)
                    mycursor.execute(sql_update, val)

                    # Commit changes
                    mydb.commit()
                    print(f"Open price for symbol {symbol} updated successfully with value{current_minute_price}.")
                
                symbols_to_notified.append([symbol, percent_change])
        else:
            print(f"Symbol {symbol} not found in the database.")
    except Exception as e:
        print(f"Error updating data for symbol {symbol}: {e}")

#update stock data
symbols = ['IBM', 'AAPL', 'AMZN', 'GOOGL', '^IXIC', 'INTC', 'META', 'MSFT', 'NVDA', 'TSLA']  # Change this to the list of symbols you want to update
for symbol in symbols:
    update_stock_data(symbol)




existing_notification = False

for stock in symbols_to_notified:
    symbol = stock[0]
    price_precent_change = stock[1]
    if price_precent_change >= PERCENT or price_precent_change <= -PERCENT:
        existing_notification = True
    print(f"Symbol: {symbol}, Price Precent Change: {price_precent_change}")




import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_email(employee_emails, message, subject):

    company_email = 'utrade4321@gmail.com'
    password = 'rpgs phnw sqja ldkh'

    # Set up the SMTP server
    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(company_email, password)

    # Compose the message
    msg = MIMEMultipart()
    msg['From'] = company_email
    msg['Subject'] = subject

    # Body of the email
    body = message

    # Add body to the message
    msg.attach(MIMEText(body, 'plain'))

    # Send the email to each employee
    for employee_email in employee_emails:
        msg['To'] = employee_email
        smtp_server.sendmail(company_email, employee_email, msg.as_string())

    # Quit SMTP server
    smtp_server.quit()

# employee_emails = ['univmohammed@gmail.com']
# message = "Hello,\n\nThis is an automated message."
# send_email(employee_emails, message)





import json
# Get cursor
mycursor = mydb.cursor()

def get_users_data():
    try:
        # Execute the SQL query
        mycursor.execute("SELECT id, email FROM auth_user WHERE id != 1")
        
        # Fetch all rows
        rows = mycursor.fetchall()
        
        return rows
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def get_plans_data():
    try:
        # Execute the SQL query
        mycursor.execute("SELECT user_id, plans FROM utrade_userprofile")
        
        # Fetch all rows
        rows = mycursor.fetchall()
        
        return rows
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

# for optimization
if existing_notification:

    # Example usage
    users_data = get_users_data()
    users_plans = get_plans_data()


    users = []
    for i in range(len(users_data)):
        plans_json = users_plans[i][1]

        # Parse JSON string
        plans = json.loads(plans_json)

        # Set to store unique symbols
        unique_symbols = set()

        # Iterate through plans and data
        for plan in plans:
            for data in plan['data']:
                unique_symbols.add(data['symbol'])

        if len(unique_symbols) == 0:
            unique_symbols = []
        else:
            unique_symbols = list(unique_symbols)

        users.append([users_data[i][1], unique_symbols])

    # print(users)



    for stock in symbols_to_notified:
        symbol = stock[0]
        price_precent_change = stock[1]

        if price_precent_change >= PERCENT or price_precent_change <= -PERCENT:
            print(symbol)
            send_for_emails = []
            for user in users:
                if symbol in user[1]:
                    send_for_emails.append(user[0])
            if price_precent_change > 0:    
                message = f"Dear valued customer,\n\nWe'd like to inform you that there has been a significant change in the stock price of {symbol}, one of the stocks you are tracking. The current price has increased by {price_precent_change}%.\n\nPlease review your investment strategy accordingly.\n\nBest regards,\nUTRADE"
                
            else:
                message = f"Dear valued customer,\n\nWe'd like to inform you that there has been a significant change in the stock price of {symbol}, one of the stocks you are tracking. The current price has decreased by {abs(price_precent_change)}%.\n\nPlease review your investment strategy accordingly.\n\nBest regards,\nUTRADE"
            
            subject = f"Stock Price Alert: {symbol}"

            send_email(send_for_emails, message, subject)