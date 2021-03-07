#app/robo_advisor.py

import requests
import json
import os
import csv

# Function to_usd was reused from the Shopping Cart project, where Professor Rossetti provided this function.
def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    """
    return f"${my_price:,.2f}" #> $12,000.71

# INFO inputs

request_url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
response = requests.get(request_url)
#print(type(response)) #> class
#print(response.status_code) #> 200
#print(response.text) #> string version of a dictionary

parsed_response = json.loads(response.text)

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

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

csv_file_path = os.path.join(os.path.dirname(__file__), "..", "data", "prices.csv")
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
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print(f"RECENT HIGH: {to_usd(float(recent_high))}")
print(f"RECENT LOW: {to_usd(float(recent_low))}")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print(f"Writing data to CSV: {csv_file_path}...")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")