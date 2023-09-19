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

    result = await client(functions.contacts.GetContactsRequest(
        hash=-12398745604826
    ))


    for user in result.users:
        print(user)
        db.add_user(user)



    # async for message in client.iter_messages(dialog):
    #     print(message.id, message.text)
    #
    #     sorm.Db.add_message()



    #
    # # You can print the message history of any chat:
    # async for message in client.iter_messages('533844145'):
    #     print(message.id, message.text)



with client:
    client.loop.run_until_complete(main())
