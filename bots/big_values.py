import time
import os

from binance import Client, exceptions

from bots.telegram_bot import send_message


BINANCE_API_KEY = os.environ.get("BINANCE_API_KEY")
BINANCE_API_SECRET = os.environ.get("BINANCE_API_SECRET")

MIN_ORDER_VALUE = 100000
THRESHOLD_PERCENT = 0.5 / 100
INTERVAL = Client.KLINE_INTERVAL_5MINUTE


async def send_high_value_notification(ticker, average_volume, high_value):
    await send_message(
        f"""
        {high_value['position']} {ticker["symbol"]}
        Volume: {high_value['value']} / {average_volume} = {high_value['value'] / average_volume}
        Price: {high_value['price']} usdt
        """
    )


def get_all_usdt_tickers(client):
    tickers = client.get_all_tickers()

    usdt_tickers = []
    for ticker in tickers:
        if ticker["symbol"].endswith("USDT"):
            usdt_tickers.append(ticker)

    return usdt_tickers


async def get_klines_average_volume(client, ticker):
    end_time = int(time.time() * 1000)
    start_time = end_time - (5 * 60 * 1000)

    klines = client.futures_klines(
        symbol=ticker["symbol"],
        interval=INTERVAL,
        startTime=start_time,
        endTime=end_time,
    )

    total_volume = 0
    for kline in klines:
        total_volume += float(kline[7])

    return total_volume / len(klines) if len(klines) > 0 else 0


def get_order_book_high_values(order_book, current_price):
    high_values = []
    for bid in order_book["bids"]:
        price, quantity = bid
        value = float(price) * float(quantity)
        if value >= MIN_ORDER_VALUE and float(price) < current_price * (
            1 - THRESHOLD_PERCENT
        ):
            high_values.append({"position": "LONG", "value": value, "price": price})

    for ask in order_book["asks"]:
        price, quantity = ask
        value = float(price) * float(quantity)
        if value >= MIN_ORDER_VALUE and float(price) > current_price * (
            1 + THRESHOLD_PERCENT
        ):
            high_values.append({"position": "SHORT", "value": value, "price": price})

    return high_values


async def get_binance_big_values():
    client = Client(BINANCE_API_KEY, BINANCE_API_SECRET)

    await send_message('Starting "Big Values" bot...')

    usdt_tickers = get_all_usdt_tickers(client)

    while True:
        for ticker in usdt_tickers:
            try:
                average_volume = await get_klines_average_volume(client, ticker)
            except exceptions.BinanceAPIException:
                continue

            order_book = client.get_order_book(
                symbol=ticker["symbol"],
                limit=10,
            )

            current_price = float(ticker["price"])

            order_book_high_values = get_order_book_high_values(
                order_book, current_price
            )
            for high_value in order_book_high_values:
                if high_value["value"] >= average_volume * 4:
                    await send_high_value_notification(
                        ticker, average_volume, high_value
                    )
                    time.sleep(0.3)

        time.sleep(30)
