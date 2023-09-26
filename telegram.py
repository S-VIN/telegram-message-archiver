from telethon import TelegramClient
from telethon import functions
from telethon import utils
from telethon import types

from enum import Enum


class Peer(Enum):
    USER = 1
    CHANNEL = 2


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Telegram(metaclass=Singleton):
    def __init__(self, session, api_id, api_hash):
        self.client = TelegramClient(session, api_id, api_hash)

    async def get_peer_by_id(self, peer_id):
        if type(peer_id) is types.PeerChannel:
            result = await self.client(functions.channels.GetFullChannelRequest(
                channel=peer_id
            ))
            print(result.chats[0].title)
        if type(peer_id) is types.PeerUser:
            result = await self.client(functions.users.GetFullUserRequest(
                peer_id
            ))
            print(result)