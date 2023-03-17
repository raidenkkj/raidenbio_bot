from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from dotenv import load_dotenv
import requests
import datetime
import time
import os


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

# Define a command handler for /frase command
@app.on_message(filters.command("frase"))
async def frase_handler(app, message):
    # Get a random phrase of the day from the API
    response = requests.get("https://phrases-api.herokuapp.com/phrases/pt-br/today")
    if response.status_code == 200:
        phrase = response.json()["phrase"]
        message.reply_text(phrase)
    else:
        message.reply_text("Desculpe, não foi possível obter uma frase no momento. Tente novamente mais tarde.")

# Define a function to send the phrase of the day at a specified time
def send_phrase():
    # Get the current date and time
    now = datetime.datetime.now()

    # Check if the current time is after 9am (local time)
    if now.hour >= 9:
        # Get a random phrase of the day from the API
        response = requests.get("https://phrases-api.herokuapp.com/phrases/pt-br/today")
        if response.status_code == 200:
            phrase = response.json()["phrase"]
            # Send the phrase to all users
            for chat_id in app.get_dialogs():
                try:
                    app.send_message(chat_id=chat_id.id, text=phrase)
                except PeerIdInvalid:
                    # Skip invalid peer IDs (e.g. deleted chats)
                    pass
        else:
            # Log an error message if we couldn't get a phrase from the API
            print("Error: couldn't get phrase from API")

# Schedule a job to send the phrase of the day every day at 9am (local time)
def schedule_job():
    scheduler = app.scheduler
    scheduler.add_job(send_phrase, 'cron', hour=9, minute=0)

# Start the bot and schedule the job
app.start()
schedule_job()
app.idle()
app.stop()
