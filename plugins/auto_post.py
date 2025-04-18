from pyrogram import Client, filters
import asyncio
import subprocess
import os
from config import STOCKED_CHANNEL_ID, POSTING_CHANNEL_ID

def generate_thumbnail(video_path, output_path="thumb.jpg"):
    subprocess.run([
        "ffmpeg", "-i", video_path, "-ss", "00:00:01", "-vframes", "1", output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path

@Client.on_message(filters.chat(STOCKED_CHANNEL_ID) & (filters.video | filters.document))
async def handle_stocked_video(client, message):
    # Simulate user sending the file to the bot
    forwarded = await message.copy(chat_id=message.from_user.id if message.from_user else message.chat.id)

    try:
        # Listen for the bot's reply with the generated link
        response = await client.listen(chat_id=forwarded.chat.id, timeout=60)

        if response.text and "t.me" in response.text:
            video_link = response.text.strip()

            # Download the video and create a thumbnail
            downloaded = await message.download()
            thumb_path = generate_thumbnail(downloaded)

            # Post to the target channel
            await client.send_photo(
                chat_id=POSTING_CHANNEL_ID,
                photo=thumb_path,
                caption=f"**Video Link:** [Click Here]({video_link})",
                parse_mode="markdown"
            )

            # Clean up
            os.remove(downloaded)
            os.remove(thumb_path)

    except asyncio.TimeoutError:
        print("No response from bot logic (timeout)")
