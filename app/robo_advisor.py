#app/robo_advisor.py

import requests
import json

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
# Info outputs

# this is the "app/robo_advisor.py" file

print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print(f"LATEST DAY: {last_refreshed}")
print(f"LATEST CLOSE: {to_usd(float(latest_close))}")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")