#app/robo_advisor.py

import requests
import json
import os
import csv
from datetime import datetime
from dotenv import load_dotenv
import pandas as pd
import plotly.express as px

load_dotenv()

# Function to_usd was reused from the Shopping Cart project, where Professor Rossetti provided this function.
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    """
    return f"${my_price:,.2f}" #> $12,000.71

# INFO inputs
tickers = []
print("Welcome to Kristina's Robo Advisor!")

while True:
    
    # Due to API rate limit, this program can accept 5 tickers before it causes an error.
    if len(tickers) < 4:
        user_input = input("Please enter a stock ticker, or type DONE if there are no more. ")
    #Warning the user that this is the last ticker they can enter.
    if len(tickers) == 4:
        #Cannot accept any more due to API rate limit.
        print("Due to rate limits, the program can accept one more ticker.") 
        user_input = input("Please enter a stock ticker, or type DONE if there are no more. ")
    
    if len(tickers) == 5:
        #Cannot accept any more due to API rate limit.
        print("Program accepts a maximum of 5 tickers at a time.")
        print("Feel free to run the program again.") 
        break

    if user_input == "DONE" or user_input == "done":
        
        #if user has not entered anything yet, force them to enter at least one ticker
        if len(tickers) == 0:
            print("Please enter at least one ticker.")
        #End while loop if user typed "DONE"
        else:
            break

    else:

        # verify the user input
        stock = str(user_input)
        #checking length of the ticker
        if (len(stock) > 0 and len(stock)) < 6:

            # check if user input is all characters a-z by looping through the string
            valid = False
            for char in stock:
                
                # Checking for upper case by converting to ASCII codes
                # This is adapted from studytonight.com, although I am already familiar 
                # with this approach from previous coding classes
                if ord(char) >= 65 and ord(char) <= 90:
                    #all good, no errors
                    valid = True
                elif ord(char) >= 97 and ord(char) <= 122:
                    #all good, no errors
                    valid = True
                else:

                    #Error
                    print("Please make sure the ticker does not include any numbers and try again.")
                    valid = False
                    break
            if valid == True:
                tickers.append(stock)

        else:
            print("The ticker should be between 1 and 5 characters in length")

print(" ")
print(f"You have requested to process data on {len(tickers)} tickers. The outputs will be processed below:")
print("-------------------------")
now = datetime.now()

print("INFO REQUESTED ON ", now.strftime("%B %d, %Y at %I:%M %p"))
print("-------------------------")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA NOW:")

api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

for symbol in tickers:
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    
    print(" ")
    print("-------------------------")
    print(f"SELECTED SYMBOL: {symbol}")
    print(" ")

    try:
        response = requests.get(request_url)
        
        parsed_response = json.loads(response.text)

        #last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]
        
        tsd = parsed_response["Time Series (Daily)"]
        
        dates = list(tsd.keys()) # TO DO: assumes first day is on top,
        # consider sorting to ensure that the latest day is first
        latest_day = dates[0]

        latest_close = tsd[latest_day]["4. close"]

        # get the high price from each day
        high_prices = []
        low_prices = []

        for date in dates:
            high_price = tsd[date]["2. high"]
            high_prices.append(float(high_price))
            low_price = tsd[date]["3. low"]
            low_prices.append(float(low_price))
        #maximum of all the high prices
        recent_high = max(high_prices)
        #minimum of all the low prices
        recent_low = min(low_prices)
        # Info outputs
        

        csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"prices_{symbol}.csv")
        #"data/prices.csv" # a relative filepath

        csv_headers = ["timestamp", "open", "high", "low", "close", "volume"]
        with open(csv_file_path, "w") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
            writer.writeheader()

            #looping to write each row
            for date in dates:
                daily_prices = tsd[date]
                writer.writerow({
                    "timestamp": date,
                    "open": daily_prices["1. open"],
                    "high": daily_prices["2. high"],
                    "low": daily_prices["3. low"],
                    "close": daily_prices["4. close"],
                    "volume": daily_prices["5. volume"],
                })
        
        
        print(f"LATEST DAY: {latest_day}")
        print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
        print(f"RECENT HIGH: {to_usd(float(recent_high))}")
        print(f"RECENT LOW: {to_usd(float(recent_low))}")
        print(" ")
        # Recommendation to buy or sell:
        if float(latest_close) <= float(recent_low) * 1.20:
            print("RECOMMENDATION: BUY")
            percent = (float(latest_close)-float(recent_low))/float(recent_low)*100
            print(f"RECOMMENDATION REASON: {symbol} is trading at only {percent:.2f}% above its recent low.")
        elif float(latest_close) <= float(recent_high) * 0.9:
            print("RECOMMENDATION: SELL")
            percent = (1 - (float(latest_close)/float(recent_high)))*100
            print(f"RECOMMENDATION REASON: {symbol} is trading at only {percent:.2f}% below its recent high.")
        else:
            print("RECOMMENDATION: HOLD")
            print(f"RECOMMENDATION REASON: {symbol} is trading more than 20% above its recent low and more than 10% below its recent high.")

        
        print(" ")
        print(f"Writing data to CSV: {csv_file_path}...")
        print("Opening price chart...")
        print(" ")

        #Plotting price chart
        #This code was adapted from plotly.com/python/plot-data-from-csv/
        df = pd.read_csv(csv_file_path)
        fig = px.line(df, x = 'timestamp', y = 'close', labels = {"timestamp": "date", "close": "price"}, title = f'{symbol} prices over the last 3 months')
        fig.show()



        print("-------------------------")
        
    except:
        print(f"No data found for {symbol}.")
        # If this is NOT the last ticker requested, the program will let the user know that the other results will still be printed
        if symbol != tickers[len(tickers) - 1]:
            print("While this ticker did not work, we will still print the results of any remaining tickers that you requested.")
        print("-------------------------")

print("All done! HAPPY INVESTING!")
print("-------------------------")
