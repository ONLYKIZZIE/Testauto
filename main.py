from pyromod import Client  # Pyromod patch to support listening
from config import APP_ID, API_HASH, TG_BOT_TOKEN
from plugins.auto_post import process_queue
import asyncio
import logging

# Optional: enable logs for debugging
logging.basicConfig(level=logging.INFO)

# Create Pyromod-compatible bot client
app = Client("bot", api_id=APP_ID, api_hash=API_HASH, bot_token=TG_BOT_TOKEN, plugins={"root": "plugins"})

# Start the bot and run your custom post-processing loop
async def main():
    await app.start()
    logging.info("Bot started")
    await process_queue(app)  # your function that processes posts
    await app.idle()

if __name__ == "__main__":
    asyncio.run(main())
