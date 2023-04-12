from binance.client import Client
import time
import os

# Replace with your own API keys
BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")

# Replace with the trading pairs you want to monitor
trading_pairs = ["BTCUSDT", "ETHUSDT", "ADAUSDT", "DOGEUSDT", "XRPUSDT"]

# Initialize the Binance client
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

while True:
    # Retrieve the latest price information for each trading pair
    prices = {}
    for pair in trading_pairs:
        ticker = client.get_ticker(symbol=pair)
        prices[pair] = float(ticker["lastPrice"])

    # Compare the prices to find profitable opportunities
    for i in range(len(trading_pairs)):
        for j in range(i + 1, len(trading_pairs)):
            pair1 = trading_pairs[i]
            pair2 = trading_pairs[j]
            spread = prices[pair1] - prices[pair2]
            fee_rate = 0.1  # Replace with your actual trading fee rate
            net_spread = spread * (
                1 - fee_rate * 2
            )  # Subtract fees from both sides of the transaction
            threshold = 0.1  # Replace with your desired threshold
            if net_spread > threshold:
                # Execute the arbitrage trade
                print(f"Arbitrage opportunity found between {pair1} and {pair2}")
                print(f"net_spread: {net_spread}, spread: {spread}")
                print(f"prices: {prices}")
                # Insert your code to execute the trade here, accounting for fees
                # Be sure to handle error cases such as insufficient funds and invalid orders

    # Wait for a certain amount of time before checking again
    time.sleep(10)  # Replace with your desired interval
