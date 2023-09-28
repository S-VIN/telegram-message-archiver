import time

import sorm
import settings
import telegram
from telethon import functions
from telethon import types


from enum import Enum


class Peer(Enum):
    USER = 1
    CHANNEL = 2


db = sorm.Db(settings.DB_NAME, settings.USER, settings.PASSWORD, settings.HOST, settings.PORT)
tg = telegram.Telegram('lib_session', settings.API_ID, settings.API_HASH)


async def get_dialogs(count=None):
    async for dialog in tg.client.iter_dialogs():
        if count is not None:
            count -= 1
            if count <= 0:
                return


        print()
        print()
        await sync_messages_from_dialog(dialog, 1)




async def sync_messages_from_dialog(dialog, count=10):
    async for message in tg.client.iter_messages(dialog):
        print(message.peer_id)
        peer = telegram.Peer(0, Peer.USER, '')

        if type(message.peer_id) is types.PeerChannel:
            peer = await db.get_peer_by_id(message.peer_id.channel_id)
        if type(message.peer_id) is types.PeerUser:
            peer = await db.get_peer_by_id(message.peer_id.user_id)
        if type(message.peer_id) is types.PeerChat:
            peer = await db.get_peer_by_id(message.peer_id.chat_id)

        if peer is None or peer.id == 0:
            peer = await tg.get_peer_by_id(message.peer_id)
            db.add_peer(peer)
            print('peer was added to db: ', peer)
        else:
            print('peer was in db: ', peer)
        count -= 1
        if count <= 0:
            return

        # db.add_message(message)


async def main():
    await get_dialogs()

    # result = await client(functions.channels.List(
    #     hash=-12398745604826
    # ))
    # print(result)


with tg.client:
    tg.client.loop.run_until_complete(main())
