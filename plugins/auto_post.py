from pyrogram import Client, filters
import os
import subprocess
from config import STOCKED_CHANNEL_ID, POSTING_CHANNEL_ID, BOT_USERNAME


def generate_thumbnail(video_path, output_path="thumb.jpg"):
    subprocess.run([
        "ffmpeg", "-i", video_path, "-ss", "00:00:01", "-vframes", "1", output_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return output_path


@Client.on_message(filters.chat(STOCKED_CHANNEL_ID) & (filters.video | filters.document))
async def handle_stocked_video(client, message):
    try:
        # Step 1: Download the video
        downloaded = await message.download()
        print("Downloaded:", downloaded)

        # Step 2: Generate a thumbnail
        thumb_path = generate_thumbnail(downloaded)
        print("Thumbnail generated")

        # Step 3: Forward the message to the bot itself to trigger the link logic
        forwarded = await message.forward(BOT_USERNAME)
        print("Forwarded to bot")

        # Step 4: Wait for the bot's reply with the generated link
        @Client.on_message(filters.reply & filters.private)
        async def reply_handler(_, reply_msg):
            if reply_msg.text and "t.me/" in reply_msg.text:
                video_link = reply_msg.text.strip()

                # Step 5: Post to the target channel
                await client.send_photo(
                    chat_id=POSTING_CHANNEL_ID,
                    photo=thumb_path,
                    caption=f"**Video Link:** [Click Here]({video_link})",
                    parse_mode="markdown"
                )

                # Clean up
                os.remove(downloaded)
                os.remove(thumb_path)
                print("Posted to channel")

    except Exception as e:
        print("Error:", e)
