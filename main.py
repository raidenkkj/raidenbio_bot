## bot do raiden

import os
from pyrogram import Client, filters
from dotenv import load_dotenv


if os.path.isfile("config.env"):
    load_dotenv("config.env")


API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

RaidenBot = Client(name="RaidenBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)


@RaidenBot.on_message(filters.command("start"))
async def start_message(RaidenBot, message):
    await RaidenBot.send_photo(message.chat.id, photo=".images/profile_picture.png", caption="<b><i>Hello, this is still in development, please try again later!</i><bi>")


print("Running...")
RaidenBot.run()
