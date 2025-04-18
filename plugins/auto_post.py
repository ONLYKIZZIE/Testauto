import os
import logging
from pyrogram import Client
from pyrogram.types import InputMediaPhoto
from config import POSTING_CHANNEL_ID

# Set up logger
logger = logging.getLogger(__name__)

async def process_queue(app: Client):
    from queue import queue  # make sure your project has a working `queue` module or structure

    while True:
        if queue.empty():
            await asyncio.sleep(5)
            continue

        data = queue.get()

        try:
            message = data["message"]
            user_id = data["user_id"]
            file_id = data["file_id"]

            logger.info(f"Downloading media from {user_id}")
            file_path = await download_media(app, file_id)

            logger.info("Generating thumbnail...")
            thumb_path = generate_thumbnail(file_path)

            logger.info("Uploading post...")
            video_link = f"https://t.me/{app.me.username}/{message.id}"

            await app.send_photo(
                chat_id=POST_CHANNEL,
                photo=thumb_path,
                caption=f"[Watch Video]({video_link})",
                parse_mode="markdown"
            )

            logger.info("Post sent successfully.")

            os.remove(file_path)
            if os.path.exists(thumb_path):
                os.remove(thumb_path)

        except Exception as e:
            logger.exception("Error during post processing: %s", e)
