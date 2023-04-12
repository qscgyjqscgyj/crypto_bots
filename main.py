import asyncio
import os

from threading import Thread
from flask import Flask

from bots.big_values import get_binance_big_values


PORT = os.environ.get("PORT", 8000)

app = Flask(__name__)


@app.route("/")
def home():
    return "cryptobooot!!!"


async def main():
    await get_binance_big_values()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    # Start the Flask app in a separate thread
    flask_thread = Thread(
        target=app.run, kwargs={"debug": False, "host": "0.0.0.0", "port": PORT}
    )
    flask_thread.start()

    # Start the asyncio loop in the main thread
    loop.run_until_complete(main())
