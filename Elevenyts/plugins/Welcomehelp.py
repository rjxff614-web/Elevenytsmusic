from pyrogram import filters
from Elevenyts import app


@app.on_message(filters.command("welcomehelp") & filters.group)
async def welcome_help(client, message):

    help_text = """
🌸 Welcome Message Help

You can customize your group's welcome using the following variables:

• "{first}" - User's first name
• "{username}" - User's username (or first name if no username)
• "{mention}" - Mentions (tags) the user
• "{id}" - User's ID
• "{group}" - Group name

⚠️ Note:
All variables MUST be used inside "{}" to work properly.

📌 Example:
Welcome {mention} to {group} 🎉
"""

    await message.reply_text(help_text)
