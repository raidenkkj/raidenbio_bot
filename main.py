## bot do raiden

import os
from pyrogram import Client, filters
from dotenv import load_dotenv


if os.path.isfile("config.env"):
    load_dotenv("config.env")


API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

RaidenBot = Client(name="useless", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)


@RaidenBot.on_message(filters.command("start"))
async def start_message(useless, message):
    await useless.send_message(message.chat.id, "")


print("Running...")
RaidenBot.run()