import sorm
import settings
import telegram
from telethon import types
from user import User
from peer import Peer, PeerType
from message import Message


db = sorm.Db(settings.DB_NAME, settings.USER, settings.PASSWORD, settings.HOST, settings.PORT)
tg = telegram.Telegram('lib_session', settings.API_ID, settings.API_HASH)


async def get_dialogs():
    async for dialog in tg.client.iter_dialogs(archived=False):
        print()
        print('process dialog: ', dialog.name)
        await sync_messages_from_dialog(dialog)


async def get_peer(tg_peer):
    peer = db.get_peer_by_id(Peer(tg_peer).id)
    if peer is None or peer.id == 0:
        peer = await tg.get_peer_by_tg_peer(tg_peer)
        db.add_peer(peer)
        print('peer was added to db: ', peer)
    return peer


def process_tg_peer(tg_peer):
    peer = Peer(tg_peer)
    if db.get_peer_by_id(peer.id) is None:
        db.add_peer(peer)
        print('peer was add to db: ', peer)
    return peer

async def process_user_by_id(user_id):
    user = db.get_user_by_id(user_id)
    if user is None:
        tg_user = await tg.get_user_by_id(user_id)
        db.add_user(User(tg_user))
        print('user was add to db: ', user)
    return user

async def process_tg_message(tg_message):
    db_message = db.get_message_by_id(tg_message.id)
    if db_message is not None:
        return
    else:
        message = Message.from_tg_message(tg_message)
        db.add_message(message)
        if tg_message.photo:
            print('File Name :' + str(tg_message.file.name))
            path = await tg.client.download_media(tg_message.media, './media_from_dialogs')
            print('File saved to', path)  # printed after download is done
        print('message was add to db: ', message)
        return message



async def sync_messages_from_dialog(dialog):
    async for tg_message in tg.client.iter_messages(dialog):
        # добавляем если надо peer в db
        peer = process_tg_peer(tg_message.peer_id)

        # добавляем если надо user в db
        if peer.type != Peer.type.USER:
            user = await process_user_by_id(Peer(tg_message.from_id).id)
        else:
            user = await process_user_by_id(peer.id)

        # добавляем если надо message в db
        await process_tg_message(tg_message)



async def main():
    await get_dialogs()

    # result = await client(functions.channels.List(
    #     hash=-12398745604826
    # ))
    # print(result)
with tg.client:
    tg.client.loop.run_until_complete(main())
