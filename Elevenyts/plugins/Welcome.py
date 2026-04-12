from pyrogram import filters
from Elevenyts import app

WELCOME_DB = {}
WELCOME_MEDIA = {}

@app.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome(client, message):
    chat_id = message.chat.id

    if message.reply_to_message and (
        message.reply_to_message.photo
        or message.reply_to_message.video
        or message.reply_to_message.animation
    ):
        media = message.reply_to_message
        WELCOME_MEDIA[chat_id] = media
        WELCOME_DB[chat_id] = message.text.split(None, 1)[1] if len(message.command) > 1 else ""
        return await message.reply_text("✅ Media welcome saved!")

    if len(message.command) < 2:
        return await message.reply_text("Use: /setwelcome message or reply to media")

    WELCOME_DB[chat_id] = message.text.split(None, 1)[1]
    WELCOME_MEDIA.pop(chat_id, None)

    await message.reply_text("✅ Text welcome saved!")


@app.on_message(filters.group & filters.new_chat_members)
async def auto_welcome(client, message):
    chat_id = message.chat.id

    template = WELCOME_DB.get(chat_id)
    media = WELCOME_MEDIA.get(chat_id)

    for user in message.new_chat_members:

        first = user.first_name or "User"
        username = f"@{user.username}" if user.username else "No Username"
        user_id = user.id
        group = message.chat.title

        text = template.format(
            first=first,
            username=username,
            id=user_id,
            group=group
        ) if template else f"👋 Welcome {first}"

        if media:
            if media.photo:
                await message.reply_photo(media.photo.file_id, caption=text)
            elif media.video:
                await message.reply_video(media.video.file_id, caption=text)
            elif media.animation:
                await message.reply_animation(media.animation.file_id, caption=text)
        else:
            await message.reply_text(text)


@app.on_message(filters.command("disablewelcome") & filters.group)
async def disable_welcome(client, message):
    chat_id = message.chat.id
    WELCOME_DB.pop(chat_id, None)
    WELCOME_MEDIA.pop(chat_id, None)
    await message.reply_text("❌ Welcome disabled!")


@app.on_message(filters.command("welcome") & filters.group)
async def show_welcome(client, message):
    chat_id = message.chat.id

    text = WELCOME_DB.get(chat_id)
    media = WELCOME_MEDIA.get(chat_id)

    if not text and not media:
        return await message.reply_text("❌ No welcome set")

    if media:
        caption = text if text else "👋 Welcome"

        if media.photo:
            await message.reply_photo(media.photo.file_id, caption=caption)
        elif media.video:
            await message.reply_video(media.video.file_id, caption=caption)
        elif media.animation:
            await message.reply_animation(media.animation.file_id, caption=caption)
    else:
        await message.reply_text(text)
