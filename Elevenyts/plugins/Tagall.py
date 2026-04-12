from pyrogram import filters
from Elevenyts import app
import asyncio

@app.on_message(filters.command(["tagall", "all"]) & filters.group)
async def tagall(client, message):

    members = []

    async for m in client.get_chat_members(message.chat.id):
        if m.user and not m.user.is_bot:
            members.append(m.user.mention)

        if len(members) >= 400:
            break

    if not members:
        return await message.reply_text("❌ No members found")

    await message.reply_text("🔥 TAGGING STARTED...")

    chunk_size = 10

    for i in range(0, len(members), chunk_size):
        chunk = members[i:i+chunk_size]
        text = "🔥 TAG ALL 🔥\n\n" + " ".join(chunk)

        await message.reply_text(text)
        await asyncio.sleep(7)
