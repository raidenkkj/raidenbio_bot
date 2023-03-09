# Power (raiden bot).

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

# Create a SQLite database and table to store the banned usernames
conn = sqlite3.connect('banned_usernames.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS banned_usernames
             (group_id INTEGER, banned_usernames TEXT)''')
conn.commit()

# Define a function to get the banned usernames for a group from the database
def get_banned_usernames(group_id):
    c.execute("SELECT banned_usernames FROM banned_usernames WHERE group_id = ?", (group_id,))
    banned_usernames = c.fetchone()
    if banned_usernames is None:
        return []
    else:
        return banned_usernames[0].split(',')

# Define a function to add a banned username for a group to the database
def add_banned_username(group_id, username):
    banned_usernames = get_banned_usernames(group_id)
    if username not in banned_usernames:
        banned_usernames.append(username)
        c.execute("INSERT INTO banned_usernames (group_id, banned_usernames) VALUES (?, ?)", (group_id, ','.join(banned_usernames)))
        conn.commit()

# Define a function to remove a banned username for a group from the database
def remove_banned_username(group_id, username):
    banned_usernames = get_banned_usernames(group_id)
    if username in banned_usernames:
        banned_usernames.remove(username)
        c.execute("UPDATE banned_usernames SET banned_usernames = ? WHERE group_id = ?", (','.join(banned_usernames), group_id))
        conn.commit()

# Define a function to get the banned usernames for all groups from the database
def get_all_banned_usernames():
    c.execute("SELECT group_id, banned_usernames FROM banned_usernames")
    banned_usernames = c.fetchall()
    return {group_id: usernames.split(',') for group_id, usernames in banned_usernames}

# Define the list of banned usernames for all groups
BANNED_USERNAMES = get_all_banned_usernames()

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
    # Check if the message was sent in a group chat or supergroup
    chat_type = message.chat.type
    if chat_type == "group" or chat_type == "supergroup":
        pass
    else:
        await RaidenBot.send_message(chat_id=message.chat.id, text="This command can only be used in groups and supergroups.")
        return

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
    # Check if the message was sent in a group chat or supergroup
    chat_type = message.chat.type
    if chat_type == "group" or chat_type == "supergroup":
        pass
    else:
        await RaidenBot.send_message(chat_id=message.chat.id, text="This command can only be used in groups and supergroups.")
        return

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
    # Check if the message was sent in a group chat or supergroup
    chat_type = message.chat.type
    if chat_type == "group" or chat_type == "supergroup":
        pass
    else:
        await RaidenBot.send_message(chat_id=message.chat.id, text="This command can only be used in groups and supergroups.")
        return

    banned_users_text = "Banned users in this group are:\n"
    if BANNED_USERNAMES:
        banned_users_text += "\n".join(BANNED_USERNAMES)
    else:
        banned_users_text += "No banned users."
    
    await RaidenBot.send_message(chat_id=message.chat.id, text=banned_users_text)

@RaidenBot.on_message(filters.command("teste"))
def testeeeeee_teste(client, message):
    if pyrogram.types.Chat == "BOT":
        RaidenBot.send_message(message.chat.id, "This command cannot be used in private chats.")
    else:
        RaidenBot.send_message(message.chat.id, "Hello, group members!")

print("Running...")
RaidenBot.run()
