from pyrogram import Client, filters
from dotenv import load_dotenv
import os
import re

if os.path.isfile("config.env"):
    load_dotenv("config.env")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Define the list of banned usernames
BANNED_USERNAMES = ["*CP*", "*C P*"]

RaidenBot = Client(name="RaidenBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

@RaidenBot.on_message(filters.new_chat_members)
async def ban_new_members(RaidenBot, message):
    for user in message.new_chat_members:
        if user.username and any(re.search(username.replace("*", ".*"), user.username, re.IGNORECASE) for username in BANNED_USERNAMES):


            await RaidenBot.kick_chat_member(chat_id=message.chat.id, user_id=user.id)
            await RaidenBot.send_message(chat_id=message.chat.id, text=f"Banned user {user.first_name} ({user.username}) from joining the group.")

@RaidenBot.on_message(filters.command("ban_list"))
async def ban_command_handler(RaidenBot, message):
    for arg in message.command[1:]:
        if arg not in BANNED_USERNAMES:
            BANNED_USERNAMES.append(arg)
            await RaidenBot.send_message(chat_id=message.chat.id, text=f"Added username {arg} to the banned list.")

print("Running...")
RaidenBot.run()
