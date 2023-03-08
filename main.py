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
        name = data.get("name", "N/A")
        login = data.get("login", "N/A")
        company = data.get("company", "N/A")
        blog = data.get("blog", "N/A")
        location = data.get("location", "N/A")
        bio = data.get("bio", "N/A")
        followers = data.get("followers", 0)
        following = data.get("following", 0)
        public_repos = data.get("public_repos", 0)
        public_gists = data.get("public_gists", 0)
        created_at = data.get("created_at", "N/A")
        updated_at = data.get("updated_at", "N/A")
        repos_url = data.get("repos_url")
        avatar_url = data.get("avatar_url")

        # Get the 5 most recently updated repositories
        response = requests.get(repos_url)
        repos = response.json()[:5]
        repo_list = "\n".join([f"[{repo['name']}]({repo['html_url']})" for repo in repos])

        message_text = (
            f"👤 Name : {name}\n"
            f"🔧 Type : User\n"
            f"🏢 Company : {company}\n"
            f"🔭 Blog : {blog}\n"
            f"📍 Location : {location}\n"
            f"📝 Bio : {bio}\n"
            f"❤️ Followers : *{followers}*\n"
            f"👁 Following : *{following}*\n"
            f"📊 Public Repos : *{public_repos}*\n"
            f"📄 Public Gists : *{public_gists}*\n"
            f"🔗 Profile Created : {created_at}\n"
            f"✏️ Profile Updated : {updated_at}\n"
            f"🔍 Some Repos : {repo_list}"
        )

        # Send message with photo
        await RaidenBot.send_photo(
            chat_id=message.chat.id,
            photo=avatar_url,
            caption=message_text,
            parse_mode="Markdown",
        )
    else:
        await message.reply_text("User not found.")


print("Running...")
RaidenBot.run()
