import pyrogram.enums.chat_type
from pyrogram import Client, filters
import sorm
import asyncio
import time
from apscheduler.schedulers.asyncio import AsyncIOScheduler


bot = pyrogram.enums.chat_type.ChatType.BOT
api_id = 9387204
api_hash = "*"
app = Client("user-bot", api_id=api_id, api_hash=api_hash)



@app.on_message(filters.chat)
async def archive(client, message):
    if db.is_new_user(message.from_user):
        db.add_user(message.from_user)
    db.add_message(message)

async def update_unread_messages():
    async for dialog in app.get_dialogs():
        count_of_unread_messages = dialog.unread_messages_count
        if count_of_unread_messages > 0:
            messages = app.get_chat_history(dialog.chat.id, count_of_unread_messages)
            async for message in messages:
                db.add_unread_message(message)

scheduler = AsyncIOScheduler()
scheduler.add_job(update_unread_messages, "interval", seconds=5)

scheduler.start()
app.run()
