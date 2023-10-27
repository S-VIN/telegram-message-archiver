from enum import Enum
from telethon import types


class PeerType(Enum):
    def __str__(self):
        return str(self.value)

    USER = 1
    CHANNEL = 2
    CHAT = 3


class Peer:
    type = PeerType.USER
    id = 0
    name = ''

    def __init__(self, tg_peer=None, name=''):
        if tg_peer is None:
            return
        self.name = name
        if type(tg_peer) is types.PeerChannel:
            self.type = PeerType.CHANNEL
            self.id = tg_peer.channel_id
        if type(tg_peer) is types.PeerUser:
            self.type = PeerType.USER
            self.type = tg_peer.user_id
        if type(tg_peer) is types.PeerChat:
            self.type = PeerType.CHAT
            self.id = tg_peer.chat_id

    def __str__(self):
        return str('Peer(' + str(self.id) + ', ' + str(self.type) + ', ' + self.name + ')')

    # @staticmethod
    # def convert(tg_peer):
