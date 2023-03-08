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
    await RaidenBot.send_photo(message.chat.id, photo=".images/profile_picture.png", caption="<i>**Hello, this is still in development, please try again later!**</i>")

log_chat_id = -827778569

@RaidenBot.on_message(filters.private & filters.command("start"))
async def start_command_handler(RaidenBot, message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    log_message = f"{username} ({user_id}) started the bot"
    await RaidenBot.send_message(log_chat_id, log_message)


print("Running...")
RaidenBot.run()
