#app/robo_advisor.py

import requests
import json
import os
import csv

from dotenv import load_dotenv

load_dotenv()

# Function to_usd was reused from the Shopping Cart project, where Professor Rossetti provided this function.
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    """
    return f"${my_price:,.2f}" #> $12,000.71

# INFO inputs
tickers = []

while True:
    
    user_input = input("Please enter a stock ticker, or type DONE if there are no more.")

    if user_input == "DONE":
        
        #End while loop if user typed "DONE"
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



api_key = os.environ.get("ALPHAVANTAGE_API_KEY")

for symbol in tickers:
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"
    response = requests.get(request_url)
    #print(type(response)) #> class
    #print(response.status_code) #> 200
    #print(response.text) #> string version of a dictionary

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

    csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", f"prices.{symbol}.csv")
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
    
    


print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
from datetime import datetime
now = datetime.now()

print("INFO REQUESTED ON: ", now.strftime("%d/%m/%Y at %I:%M %p"))
print("-------------------------")
print(f"LATEST DAY: {latest_day}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY or SELL!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"Writing data to CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")