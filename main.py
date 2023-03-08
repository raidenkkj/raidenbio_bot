# Power (raiden bot).

from pyrogram import Client, filters
from dotenv import load_dotenv
import os
import re

if os.path.isfile("config.env"):
    load_dotenv("config.env")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

RaidenBot = Client(name="RaidenBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# Define the list of banned usernames
BANNED_USERNAMES = []

@RaidenBot.on_message(filters.command("start"))
async def start_command_handler(RaidenBot, message):
    # Check if the user is the developer
    if message.from_user.id == 1123864418:
        text = "Hello master, i don't need to explain what i do because you already know ^^"
    else:
        text = f"Hi {message.from_user.first_name}, i'm Power! I am a group management bot. Use the /help command to see a list of available commands."
    
    # Send the message and reply directly to the user who sent the command
    await RaidenBot.send_message(
    chat_id=message.chat.id,
    text=text,
    reply_to_message_id=message.id
    )

    # Send log message
    user_id = message.from_user.id
    username = message.from_user.username

    log_message = f"{username} ({user_id}) started the bot"
    await RaidenBot.send_message(-827778569, log_message)

@RaidenBot.on_message(filters.command("add"))
async def add_command_handler(RaidenBot, message):
    # Extract the command argument
    command_parts = message.text.split()
    if len(command_parts) != 2:
        await RaidenBot.send_message(chat_id=message.chat.id, text="Please specify a username to remove.")
        return
    username = command_parts[1]

    # Add the username to the banned list
    username = message.text.split()[1]
    if username not in BANNED_USERNAMES:
        BANNED_USERNAMES.append(username)
        await RaidenBot.send_message(chat_id=message.chat.id, text=f"Added username {username} to the banned list.")
    else:
        await RaidenBot.send_message(chat_id=message.chat.id, text=f"{username} is already in the banned list.")

@RaidenBot.on_message(filters.command("remove"))
async def remove_command_handler(RaidenBot, message):
    # Extract the command argument
    command_parts = message.text.split()
    if len(command_parts) != 2:
        await RaidenBot.send_message(chat_id=message.chat.id, text="Please specify a username to remove.")
        return
    username = command_parts[1]

    # Remove the username from the banned list
    if username in BANNED_USERNAMES:
        BANNED_USERNAMES.remove(username)
        await RaidenBot.send_message(chat_id=message.chat.id, text=f"Removed username {username} from the banned list.")
    else:
        await RaidenBot.send_message(chat_id=message.chat.id, text=f"{username} is not in the banned list.")

@RaidenBot.on_message(filters.command("banlist"))
async def banlist_command_handler(RaidenBot, message):
    banned_users_text = "Banned users in this group are:\n"
    if BANNED_USERNAMES:
        banned_users_text += "\n".join(BANNED_USERNAMES)
    else:
        banned_users_text += "No banned users."
    
    await RaidenBot.send_message(chat_id=message.chat.id, text=banned_users_text)

print("Running...")
RaidenBot.run()
