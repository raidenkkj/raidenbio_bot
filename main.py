from pyrogram import Client, filters
from dotenv import load_dotenv
import os
import re

if os.path.isfile("config.env"):
    load_dotenv("config.env")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# Define the ID of the log group
LOG_GROUP_ID = -827778569

# Function to send log message
async def send_log_message(message):
    # Get user info
    user = message.from_user
    user_info = f"{user.id} ({user.first_name} {user.last_name})"

    # Create log message
    log_message = f"Bot started by {user_info} in chat {message.chat.id} ({message.chat.title})"

    # Send log message to log group
    await RaidenBot.send_message(chat_id=LOG_GROUP_ID, text=log_message)

@RaidenBot.on_command("start")
async def start_command_handler(RaidenBot, message):
    # Check if the user is the developer
    if message.from_user.id == 1123864418:
        text = "Hello master, i don't need to explain what i do because you already know ^^"
    else:
        text = "Hi, i'm Power! I am a group management bot. Use the /help command to see a list of available commands."
    
    # Send the message
    await RaidenBot.send_message(chat_id=message.chat.id, text=text)

    # Send log message
    await send_log_message(message)

# Define the list of banned usernames
BANNED_USERNAMES = ["*CP*"]

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

@RaidenBot.on_message(filters.command("ban_list"))
async def ban_command_handler(RaidenBot, message):
    # Create a list of banned usernames as clickable buttons
    banned_usernames_list = []
    for banned_username in BANNED_USERNAMES:
        banned_usernames_list.append([InlineKeyboardButton(banned_username, callback_data=f"unban_{banned_username}")])
    # Create a markup object to display the banned usernames list
    markup = InlineKeyboardMarkup(banned_usernames_list)
    # Send the list of banned usernames as a message
    await RaidenBot.send_message(chat_id=message.chat.id, text="List of banned usernames:", reply_markup=markup)

@RaidenBot.on_callback_query()
async def callback_query_handler(RaidenBot, query):
    # Check if the query is a request to unban a user
    if query.data.startswith("unban_"):
        banned_username = query.data.split("_")[1]
        if banned_username in BANNED_USERNAMES:
            # Remove the banned username from the list
            BANNED_USERNAMES.remove(banned_username)
            # Edit the original message with the updated banned usernames list
            banned_usernames_list = []
            for banned_username in BANNED_USERNAMES:
                banned_usernames_list.append([InlineKeyboardButton(banned_username, callback_data=f"unban_{banned_username}")])
            markup = InlineKeyboardMarkup(banned_usernames_list)
            await RaidenBot.edit_message_reply_markup(chat_id=query.message.chat.id, message_id=query.message.message_id, reply_markup=markup)
            # Send a confirmation message
            await RaidenBot.answer_callback_query(query.id, text=f"Unbanned {banned_username}")

print("Running...")
RaidenBot.run()
