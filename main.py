import sorm
import settings
import telegram
from telethon import types
from user import User
from peer import Peer
from message import Message


db = sorm.Db(settings.DB_NAME, settings.USER, settings.PASSWORD, settings.HOST, settings.PORT)
tg = telegram.Telegram('lib_session', settings.API_ID, settings.API_HASH)


async def get_dialogs(count=None):
    async for dialog in tg.client.iter_dialogs():
        if count is not None:
            count -= 1
            if count <= 0:
                return
        print()
        await sync_messages_from_dialog(dialog)


async def sync_messages_from_dialog(dialog):
    async for tg_message in tg.client.iter_messages(dialog):
        peer = Peer()
        if type(tg_message.peer_id) is types.PeerChannel:
            peer = await db.get_peer_by_id(tg_message.peer_id.channel_id)
        if type(tg_message.peer_id) is types.PeerUser:
            peer = await db.get_peer_by_id(tg_message.peer_id.user_id)
        if type(tg_message.peer_id) is types.PeerChat:
            peer = await db.get_peer_by_id(tg_message.peer_id.chat_id)

        if peer is None or peer.id == 0:
            peer = await tg.get_peer_by_id(tg_message.peer_id)
            db.add_peer(peer)
            print('peer was added to db: ', peer)
        else:
            print('peer was in db: ', peer)

        db_user_id = 0
        if type(tg_message.peer_id) is types.PeerUser:
            db_user_id = tg_message.peer_id.user_id
        elif type(tg_message.peer_id) is types.PeerChat:
            db_user_id = tg_message.from_id.user_id
        else:
            db_message = await db.get_message_by_id(tg_message.id)
            if db_message is None:
                continue
            else:
                db.add_message(Message(tg_message))
                if tg_message.photo:
                    print('File Name :' + str(tg_message.file.name))
                    path = await tg.client.download_media(tg_message.media, './')
                    print('File saved to', path)  # printed after download is done
                continue

        user = await db.get_user_by_id(db_user_id)

        if user is None or user.id == 0:
            tg_user = await tg.get_user_by_id(db_user_id)
            print(tg_user)
            db.add_user(User(tg_user))

        db_message = await db.get_message_by_id(tg_message.id)
        if db_message is not None:
            continue
        else:
            db.add_message(Message(tg_message))
            if tg_message.photo:
                print('File Name :' + str(tg_message.file.name))
                path = await tg.client.download_media(tg_message.media, './')
                print('File saved to', path)  # printed after download is done


async def main():
    await get_dialogs()

    # result = await client(functions.channels.List(
    #     hash=-12398745604826
    # ))
    # print(result)


with tg.client:
    tg.client.loop.run_until_complete(main())
