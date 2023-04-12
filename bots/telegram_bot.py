import telegram
import os


TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN")
TG_CHAT_ID = os.environ.get("TG_CHAT_ID")


async def send_message(message):
    bot = telegram.Bot(token=TG_BOT_TOKEN)
    return await bot.send_message(chat_id=TG_CHAT_ID, text=message)
