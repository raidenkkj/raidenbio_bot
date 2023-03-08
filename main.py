# Raiden bot

from pyrogram import Client, filters
from dotenv import load_dotenv
import os


if os.path.isfile("config.env"):
    load_dotenv("config.env")


API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

RaidenBot = Client(name="RaidenBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)


@RaidenBot.on_message(filters.command("start"))
async def start_command_handler(RaidenBot, message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    log_message = f"{username} ({user_id}) started the bot"
    await RaidenBot.send_message(-827778569, log_message)

    await message.reply_photo(photo=".images/profile_picture.png", caption="<i>**Hello, this is still in development, please try again later!**</i>")


print("Running...")
RaidenBot.run()
