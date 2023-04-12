import asyncio
import os
from aiohttp import web

from bots.big_values import get_binance_big_values


async def handle(request):
    return web.Response(text="cryptobooot!")


app = web.Application()
app.router.add_get("/", handle)


async def main():
    while True:
        await get_binance_big_values()


if __name__ == "__main__":
    # web.run_app(app, port=8000)
    asyncio.run(main())
