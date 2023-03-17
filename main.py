# Source code of this shit

from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from dotenv import load_dotenv
import requests
import datetime
import schedule
import time
import os
import threading

if os.path.isfile("config.env"):
    load_dotenv("config.env")

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(name="app", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, in_memory=True)

# Define a command handler for /start command
@app.on_message(filters.command("start"))
async def start_command_handler(app, message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    log_message = f"{username} ({user_id}) started the bot"
    await app.send_message(-827778569, log_message)

    await message.reply_photo(photo=".images/hello.png", caption="<i>**Olá, eu sou um bot que manda frases diariamente em seus grupos!**</i>")

import pyrogram
import requests
from datetime import datetime
import time

# Create a Pyrogram client instance
app = pyrogram.Client("my_bot_token", api_id=123456, api_hash="my_api_hash")

# Define a function to get the daily quote
def get_daily_quote():
    response = requests.get("https://api.quotable.io/random?language=pt")
    if response.status_code == 200:
        data = response.json()
        return data["content"]
    else:
        return None

# Define a function to send the daily quote to the current chat
def send_daily_quote(chat_id):
    quote = get_daily_quote()
    if quote:
        # Format the message to include today's date and the daily quote
        message = f"A frase diária de hoje é:\n\n{quote}"
        # Send the message to the current chat
        with app:
            app.send_message(chat_id, message)

# Define a command handler for the /frase command
@app.on_message(filters.command("frase"))
def frase_command_handler(client, message):
    # Send the daily quote to the current chat
    send_daily_quote(message.chat.id)

# Define a job that runs every day to send the daily quote
def daily_quote_job():
    # Set the time for the daily quote to be sent (replace with your preferred time)
    daily_quote_time = "09:00"
    while True:
        now = datetime.now()
        # Check if it's time to send the daily quote
        if now.strftime("%H:%M") == daily_quote_time:
            # Send the daily quote to all active chats
            for chat in app.get_dialogs():
                if chat.chat.type in ["group", "supergroup"]:
                    send_daily_quote(chat.chat.id)
        # Wait for 1 minute before checking again
        time.sleep(60)

# Start the Pyrogram client
app.start()

# Start the daily quote job in a separate thread
import threading
threading.Thread(target=daily_quote_job).start()

# Run the client until it's stopped
app.run() 
