from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from plugins.auto_post import process_queue

app = Client("bot", api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins={"root": "plugins"})

if __name__ == "__main__":
    app.run(process_queue(app))
