import pyrogram.enums.chat_type
from pyrogram import Client, filters
import sorm

bot = pyrogram.enums.chat_type.ChatType.BOT

api_id = 9387204
api_hash = "27324c79706b8e8c0f9819f9646076e9"

app = Client("user-bot", api_id=api_id, api_hash=api_hash)

db = sorm.Db(database="telegram_my_messages", user='postgres', password='3228', host='127.0.0.1', port='5432')





@app.on_message(filters.text & filters.private)
async def archive(client, message):
    if db.is_new_user(message.from_user):
        print('new user')
        db.add_user_to_db(message.from_user)
    db.add_message_to_db(message)
    async for dialog in app.get_dialogs():
        count_of_unread_messages = dialog.unread_messages_count
        messages = await client.get_messages([dialog.chat.id])
        for i in range(count_of_unread_messages):
            print(messages[i])



async def main():
    async with app:
        # "me" refers to your own chat (Saved Messages)
        async for message in app.get_chat_history("me"):
            print(message)



app.run()
