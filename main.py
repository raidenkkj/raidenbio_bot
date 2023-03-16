# Power source code, a telegram bot.

from pyrogram import Client, filters
from dotenv import load_dotenv
import os
import re
import sqlite3

if os.path.isfile("config.env"):
    load_dotenv("config.env")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

RaidenBot = Client(name="RaidenBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# handle commands
@RaidenBot.on_message(filters.command(["admin", "report"]) & filters.group)
def mention_admins(client, message):
    chat_id = message.chat.id
    admins = client.get_chat_members(chat_id, filter="administrators").participants
    mention_text = "All admins have been mentioned."
    for admin in admins:
        if admin.user.is_bot == False:
            client.send_chat_action(chat_id, "typing")
            client.send_message(chat_id, f"@{admin.user.username}")

# start the bot
RaidenBot.run()
