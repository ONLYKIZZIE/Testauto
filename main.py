from pyrogram import Client
from pyromod import listen  # Import the listen method to patch the Client
from config import APP_ID, API_HASH, TG_BOT_TOKEN
from plugins.auto_post import process_queue

app = Client(
    "bot",
    api_id=APP_ID,
    api_hash=API_HASH,
    bot_token=TG_BOT_TOKEN,
    plugins={"root": "plugins"}
)

if __name__ == "__main__":
    app.run(process_queue(app))
