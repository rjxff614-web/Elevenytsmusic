from pyrogram import filters
from Elevenyts import app

@app.on_message(filters.command(["tagall", "all"]) & filters.group)
async def tagall(client, message):

    members = []

    async for m in client.get_chat_members(message.chat.id):
        if m.user and not m.user.is_bot:
            members.append(m.user.mention)

        if len(members) >= 50:
            break

    if not members:
        return await message.reply_text("❌ No members found")

    text = "🔥 TAG ALL 🔥\n\n"
    text += " ".join(members)

    await message.reply_text(text)
