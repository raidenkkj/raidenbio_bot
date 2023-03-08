# Raiden bot

import requests
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


@RaidenBot.on_message(filters.command("gitprofile"))
async def gitprofile_command_handler(RaidenBot, message):
    query = message.text.split(" ", 1)[1]
    url = f"https://api.github.com/users/{query}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        profile_picture_url = data["avatar_url"]
        name = data["name"]
        bio = data["bio"]
        followers = data["followers"]
        following = data["following"]
        public_repos = data["public_repos"]

        caption = f"<b>{name}</b>\n<b>Followers:</b> {followers}\n<b>Following:</b> {following}\n<b>Public Repos:</b> {public_repos}"

        await RaidenBot.send_photo(chat_id=message.chat.id, photo=profile_picture_url, caption=caption)
    else:
        await message.reply_text("User not found.")


print("Running...")
RaidenBot.run()
