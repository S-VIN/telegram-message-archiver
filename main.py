import sorm
import settings
import telegram
from telethon import types
from user import User
from peer import Peer, PeerType
from message import Message, MessageType
from utils import FileSystem
import os

db = sorm.Db(settings.DB_NAME, settings.USER, settings.PASSWORD, settings.HOST, settings.PORT)
tg = telegram.Telegram('lib_session', settings.API_ID, settings.API_HASH)


async def get_dialogs():
    async for dialog in tg.client.iter_dialogs(archived=False):
        print()
        print('process dialog: ', dialog.name)
        await sync_messages_from_dialog(dialog)


async def get_peer(tg_peer):
    peer = db.get_peer_by_id(Peer.from_tg_peer(tg_peer).id)
    if peer is None or peer.id == 0:
        peer = await tg.get_peer_by_tg_peer(tg_peer) # TODO шляпа
        db.add_peer(peer)
        print('peer was added to db: ', peer)
    return peer


def process_tg_peer(tg_peer):
    peer = Peer.from_tg_peer(tg_peer)
    if db.get_peer_by_id(peer.id) is None:
        db.add_peer(peer)
        print('peer was add to db: ', peer)
    return peer

async def process_user_by_id(user_id):
    user = db.get_user_by_id(user_id)
    if user is None:
        tg_user = await tg.get_user_by_id(user_id)
        db.add_user(User.from_tg_user(tg_user))
        print('user was add to db: ', user)
    return user

async def process_tg_message(tg_message):
    print(tg_message)
    db_message = db.get_message_by_id(tg_message.id)
    if db_message is None:
        message = Message.from_tg_message(tg_message)
        db.add_message(message)
        print('message was add to db: ', Message.from_tg_message(tg_message))
        print(tg_message)
    await process_photo_from_message(tg_message)
    await process_document_from_message(tg_message)


async def process_photo_from_message(tg_message):
    if tg_message.photo and type(tg_message.media) == types.MessageMediaPhoto:
        filename = str(tg_message.date.strftime('%Y-%m-%d')) + '_' + str(tg_message.id)
        filepath = settings.PATH_FOR_MEDIA + str(Peer.from_tg_peer(tg_message.peer_id).id) + '/'
        filename_with_path = filepath + filename

        try:
            if (filename + '.jpg') in os.listdir(filepath):
                print('file was in filesystem: ', filename)
                return
        except FileNotFoundError:
            pass
            # Игнорируем исключение, потому что после скачивания файла tg.client.download_media заведёт директорию

        path = await tg.client.download_media(tg_message.media, filename_with_path)
        print('file saved to', path, filename)  # printed after download is done


async def process_document_from_message(tg_message):
    message = Message.from_tg_message(tg_message)
    if tg_message.media and type(tg_message.media) == types.MessageMediaDocument and tg_message.media.document is not None:
        filename = str(tg_message.date.strftime('%Y-%m-%d')) + '_' + str(tg_message.id) + '_' + str(message.type)
        filepath = settings.PATH_FOR_MEDIA + str(Peer.from_tg_peer(tg_message.peer_id).id) + '/'
        filename_with_path = filepath + filename

        try:
            if FileSystem.is_file_in_filesystem(filename, filepath):
                print('file was in filesystem: ', filename)
                return
        except FileNotFoundError:
            pass
            # Игнорируем исключение, потому что после скачивания файла tg.client.download_media заведёт директорию

        path = await tg.client.download_media(tg_message.media, filename_with_path)
        print('file saved to', path, filename)  # printed after download is done



async def sync_messages_from_dialog(dialog):
    async for tg_message in tg.client.iter_messages(dialog):
        # добавляем если надо peer в db
        peer = process_tg_peer(tg_message.peer_id)

        # добавляем если надо user в db
        # В чатах есть сообщения от юзеров, которых тоже надо добавить
        if peer.type == PeerType.CHAT:
            user = await process_user_by_id(Peer.from_tg_peer(tg_message.from_id).id)
        # В ЛС с людьми, нужно добавить человека по пиру
        if peer.type == PeerType.USER:
            user = await process_user_by_id(peer.id)
        # В каналах есть сообщения от канала, их не надо добавлять
        # if peer.type == PeerType.CHANNEL:

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
