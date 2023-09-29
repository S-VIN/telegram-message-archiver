from telethon import TelegramClient
from telethon import functions
from telethon import utils
from telethon import types


from enum import Enum


class PeerType(Enum):
    def __str__(self):
        return str(self.value)

    USER = 1
    CHANNEL = 2
    CHAT = 3


class Peer():
    type = PeerType.USER
    id = 0
    name = ''

    def __init__(self, id, peer_type, name):
        self.id = id
        self.type = peer_type
        self.name = name

    def __str__(self):
        return str('Peer(' + str(self.id) + ', ' + str(self.type) + ', ' + self.name + ')')

class Message():
    def __init__(self, id, text, datetime, peer_id, chat_type):
        self.id = id
        self.text = text
        self.datetime = datetime
        self.peer_id = peer_id
        self.chat_type = chat_type


class User():
    def __init__(self, id, first_name, last_name, username, bot, contact):
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.bot = bot
        self.contact = contact

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Telegram(metaclass=Singleton):
    def __init__(self, session, api_id, api_hash):
        self.client = TelegramClient(session, api_id, api_hash)

# Плохой способ вызывать эту функцию каждый раз, как приходит сообщение. Мы дудосим телеграм. Нужно получить сначала все пиры через get_dialogs,
# а потом уже тех, которых нет (должны быть все, кроме удаленных) смотреть через это.
    async def get_peer_by_id(self, peer_id):
        if type(peer_id) is types.PeerChannel:
            result = await self.client(functions.channels.GetFullChannelRequest(
                channel=peer_id
            ))
            return Peer(result.chats[0].id, PeerType.CHAT, result.chats[0].title)

        if type(peer_id) is types.PeerUser:
            result = await self.client(functions.users.GetFullUserRequest(peer_id))
            print(result)
            return Peer(
                result.full_user.id,
                PeerType.USER,
                (result.users[0].first_name if result.users[0].first_name is not None else '')
                    + ((' ' + result.users[0].last_name) if result.users[0].last_name is not None else ''))

        if type(peer_id) is types.PeerChat:
            result = await self.client(functions.messages.GetPeerDialogsRequest(
                peers=[peer_id]
            ))
            print(result.chats[0].title)
            return Peer(result.chats[0].id, PeerType.CHAT, result.chats[0].title)

    async def get_user_by_id(self, user_id):
        user = await self.client(functions.users.GetFullUserRequest(user_id))
        return user
