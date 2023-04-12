import time
import os

from binance import Client, exceptions

from bots.telegram_bot import send_message


BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")


def get_all_usdt_tickers(client):
    tickers = client.get_all_tickers()

    for ticker in tickers:
        if ticker["symbol"].endswith("USDT"):
            yield ticker


async def send_high_value_notification(ticker, average_volume, high_values):
    print("HIGH VOLUME!!!!!!!!!!!", ticker["symbol"], average_volume, high_values)
    print("---------------------")

    await send_message(
        f"""
        HIGH VOLUME!!!!!!!!!!!\n
        Ticker: {ticker["symbol"]}\n
        Average volume in the last 5 minutes: {average_volume}
        Values: {high_values}
        """
    )


async def get_binance_big_values():
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

    min_order_value = 100000
    threshold_percent = 0.5 / 100
    interval = Client.KLINE_INTERVAL_5MINUTE

    await send_message('Starting "Big Values" bot...')

    for ticker in get_all_usdt_tickers(client):
        try:
            end_time = int(time.time() * 1000)
            start_time = end_time - (5 * 60 * 1000)

            klines = client.futures_klines(
                symbol=ticker["symbol"],
                interval=interval,
                startTime=start_time,
                endTime=end_time,
            )

            total_volume = 0
            for kline in klines:
                total_volume += float(kline[7])

            average_volume = total_volume / len(klines) if len(klines) > 0 else 0
        except exceptions.BinanceAPIException:
            continue

        order_book = client.get_order_book(
            symbol=ticker["symbol"],
            limit=10,
        )

        current_price = float(ticker["price"])

        for bid in order_book["bids"]:
            price, quantity = bid
            value = float(price) * float(quantity)
            if value >= min_order_value and float(price) < current_price * (
                1 - threshold_percent
            ):
                if value > average_volume * 4:
                    await send_high_value_notification(
                        ticker,
                        average_volume,
                        ("LONG ⬆️", f"Value: {value}", f"Price: {price}"),
                    )

        for ask in order_book["asks"]:
            price, quantity = ask
            value = float(price) * float(quantity)
            if value >= min_order_value and float(price) > current_price * (
                1 + threshold_percent
            ):
                if value > average_volume * 4:
                    await send_high_value_notification(
                        ticker,
                        average_volume,
                        ("SHORT ⬇️", f"Value: {value}", f"Price: {price}"),
                    )

        time.sleep(0.3)
