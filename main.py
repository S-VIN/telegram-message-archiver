import time

import sorm
import settings
from telethon import TelegramClient
from telethon import functions

import psycopg2
# conn = psycopg2.connect(dbname=settings.DB_NAME, user=settings.USER, password=settings.PASSWORD, host=settings.HOST)
# cursor = conn.cursor()

db = sorm.Db(settings.DB_NAME, settings.USER, settings.PASSWORD, settings.HOST, settings.PORT)

client = TelegramClient('lib_session', settings.API_ID, settings.API_HASH)
# class SS(object):
# def sprint(user):
#     print(user)

async def main():
    # # Getting information about yourself
    # me = await client.get_me()
    #
    #
    # # "me" is a user object. You can pretty-print
    # # any Telegram object with the "stringify" method:
    # print(me.stringify())
    #
    # # When you print something, you see a representation of it.
    # # You can access all attributes of Telegram objects with
    # # the dot operator. For example, to get the username:
    # username = me.username
    # print(username)
    # print(me.phone)

    i = 0
    async for dialog in client.iter_dialogs():
        i += 1
        if i == 10:
            break

        print(dialog)
        j = 0


        try:
            if not dialog.entity.contact:
                continue
        except(AttributeError):
            continue

        async for message in client.iter_messages(dialog):
            print(message.id, message.text)
            db.add_message(message)

    # result = await client(functions.contacts.GetContactsRequest(
    #     hash=-12398745604826
    # ))
    #
    #
    # for user in result.users:
    #     print(user)
    #     db.add_user(user)







    #
    # # You can print the message history of any chat:
    # async for message in client.iter_messages('533844145'):
    #     print(message.id, message.text)



with client:
    client.loop.run_until_complete(main())
