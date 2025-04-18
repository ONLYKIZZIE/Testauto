from pyrogram import Client, filters
import asyncio
import subprocess
import os
from config import STOCKED_CHANNEL_ID, POSTING_CHANNEL_ID, BOT_USERNAME

video_queue = asyncio.Queue()

def generate_thumbnail(video_path, output_path="thumb.jpg"):
    subprocess.run([
        "ffmpeg", "-i", video_path, "-ss", "00:00:01", "-vframes", "1", output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

@Client.on_message(filters.chat(STOCKED_CHANNEL_ID) & (filters.video | filters.document))
async def queue_stocked_video(client, message):
    await video_queue.put(message)
    print(f"Queued video {message.id}")

async def process_queue(client: Client):
    await client.start()
    while True:
        message = await video_queue.get()
        try:
            print(f"Processing video {message.id}")

            downloaded = await message.download()
            thumb_path = generate_thumbnail(downloaded)

            # Simulate user sending the video to the bot itself
            user_msg = await message.copy(chat_id=message.chat.id)

            # Wait for the bot’s reply to that message
            video_link = None
            async for msg in client.get_chat_history(message.chat.id, limit=10):
                if msg.reply_to_message and msg.reply_to_message.message_id == user_msg.message_id:
                    if msg.text and "t.me/" in msg.text:
                        video_link = msg.text.strip()
                        break

            if video_link:
                # Send video and thumbnail to the posting channel
                await client.send_photo(
                    chat_id=POSTING_CHANNEL_ID,
                    photo=thumb_path,
                    caption=f"**Video Link:** [Click Here]({video_link})",
                    parse_mode="markdown"
                )

            os.remove(downloaded)
            os.remove(thumb_path)

        except Exception as e:
            print(f"Error processing message: {e}")

        await asyncio.sleep(60)  # Wait 1 minute before next post
