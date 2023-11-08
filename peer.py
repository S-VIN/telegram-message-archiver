from enum import Enum
from telethon import types


class PeerType(Enum):
    USER = 1
    CHANNEL = 2
    CHAT = 3

    def __str__(self):
        return str(self.value)


class Peer:

    @staticmethod
    def from_args(id, type, name=''):
        peer = Peer()
        peer.id = id
        peer.type = type
        peer.name = name
        return peer

    @staticmethod
    def from_tg_peer(tg_peer, name=''):
        if tg_peer is None:
            return
        peer = Peer()
        peer.name = name
        if type(tg_peer) is types.PeerChannel:
            peer.type = PeerType.CHANNEL
            peer.id = tg_peer.channel_id
            peer.name = 'channel '
        if type(tg_peer) is types.PeerUser:
            peer.type = PeerType.USER
            peer.id = tg_peer.user_id
            peer.name = 'user '
        if type(tg_peer) is types.PeerChat:
            peer.type = PeerType.CHAT
            peer.id = tg_peer.chat_id
            peer.name = 'chat '
        return peer

    def __str__(self):
        return str('Peer(' + str(self.id) + ', ' + str(self.type.name) + ', ' + self.name + ')')

