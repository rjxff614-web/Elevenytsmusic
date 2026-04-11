from pyrogram import filters
from Elevenyts import app

WELCOME_DB = {}

@app.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Use: /setwelcome message")

    WELCOME_DB[message.chat.id] = message.text.split(None, 1)[1]

    await message.reply_text("✅ Welcome saved!")

@app.on_message(filters.group & filters.new_chat_members)
async def welcome(client, message):

    chat_id = message.chat.id
    template = WELCOME_DB.get(chat_id)

    for user in message.new_chat_members:

        first = user.first_name or "User"
        username = f"@{user.username}" if user.username else "No Username"
        user_id = user.id
        group = message.chat.title

        if template:
            text = template.format(
                first=first,
                username=username,
                id=user_id,
                group=group
            )
        else:
            text = f"👋 Welcome {first} in {group}"

        await message.reply_text(text)
