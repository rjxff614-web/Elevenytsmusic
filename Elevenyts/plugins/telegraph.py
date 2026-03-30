import os
import tempfile
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from PRINCEMUSIC import app
import requests
import aiohttp
import asyncio


async def upload_file(file_path):
    """Upload file to catbox.moe"""
    url = "https://catbox.moe/user/api.php"
    
    # Use aiohttp for async upload
    async with aiohttp.ClientSession() as session:
        data = aiohttp.FormData()
        data.add_field('reqtype', 'fileupload')
        data.add_field('json', 'true')
        data.add_field('fileToUpload', open(file_path, 'rb'), filename=os.path.basename(file_path))
        
        try:
            async with session.post(url, data=data) as response:
                if response.status == 200:
                    response_text = await response.text()
                    return True, response_text.strip()
                else:
                    response_text = await response.text()
                    return False, f"Error: {response.status} - {response_text}"
        except Exception as e:
            return False, f"Upload failed: {str(e)}"


@app.on_message(filters.command(["tgm", "tgt", "telegraph", "tl"]))
async def get_link_group(client, message):
    """Handle media upload to catbox.moe"""
    if not message.reply_to_message:
        return await message.reply_text(
            "❍ Please reply to a media to upload on Catbox"
        )

    media = message.reply_to_message
    file_size = 0
    
    # Get file size based on media type
    if media.photo:
        file_size = media.photo.file_size
    elif media.video:
        file_size = media.video.file_size
    elif media.document:
        file_size = media.document.file_size
    else:
        return await message.reply_text("❍ Please reply to a photo, video, or document.")

    # Catbox limit is 200MB
    if file_size > 200 * 1024 * 1024:
        return await message.reply_text("❍ Please provide a media file under 200MB.")

    processing_msg = None
    local_path = None
    
    try:
        processing_msg = await message.reply("❍ Processing...")

        # Download with progress
        async def progress(current, total):
            if processing_msg and total > 0:
                try:
                    percent = (current * 100) / total
                    if percent % 10 < 1:  # Update every 10% to avoid spam
                        await processing_msg.edit_text(
                            f"❍ Downloading... {percent:.1f}%"
                        )
                except Exception:
                    pass

        # Download the media
        local_path = await media.download(progress=progress)
        
        if not local_path or not os.path.exists(local_path):
            raise Exception("Failed to download media")

        await processing_msg.edit_text("❍ Uploading to Catbox...")

        # Upload the file
        success, result = await upload_file(local_path)

        if success:
            # Create inline keyboard with the link
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("❍ Click Here For Link", url=result)]
            ])
            
            await processing_msg.edit_text(
                f"❍ Upload successful!\n\n[Tap to view]({result})",
                reply_markup=keyboard,
                disable_web_page_preview=True
            )
        else:
            await processing_msg.edit_text(
                f"❍ An error occurred while uploading your file\n\nError: {result}"
            )

    except Exception as e:
        error_msg = f"❍ File upload failed\n\nReason: {str(e)}"
        if processing_msg:
            await processing_msg.edit_text(error_msg)
        else:
            await message.reply_text(error_msg)
    
    finally:
        # Clean up downloaded file
        if local_path and os.path.exists(local_path):
            try:
                os.remove(local_path)
            except Exception:
                pass
