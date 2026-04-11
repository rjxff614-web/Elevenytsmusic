from pyrogram import Client, filters

# temporary storage (later MongoDB use kar sakte ho)
WELCOME_DB = {}

# =========================
# SET WELCOME COMMAND
# =========================
@Client.on_message(filters.command("setwelcome") & filters.group)
async def set_welcome(client, message):

    if len(message.command) < 2:
        return await message.reply_text("Use: /setwelcome your message")

    chat_id = message.chat.id
    text = message.text.split(None, 1)[1]

    WELCOME_DB[chat_id] = text

    await message.reply_text("✅ Custom welcome saved!")

# =========================
# AUTO WELCOME
# =========================
@Client.on_message(filters.new_chat_members)
async def welcome(client, message):

    chat_id = message.chat.id
    group_name = message.chat.title

    template = WELCOME_DB.get(chat_id)

    for user in message.new_chat_members:

        first = user.first_name
        username = f"@{user.username}" if user.username else "No Username"
        user_id = user.id

        if template:
            text = template.format(
                first=first,
                username=username,
                id=user_id,
                group=group_name
            )
        else:
            text = f"Welcome {first} 👋"

        await message.reply_text(text)
