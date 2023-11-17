from peer import Peer, PeerType
from enum import Enum
from telethon import types


class MessageType(Enum):
    UNKNOWN = 0
    TEXT = 1
    STICKER = 2
    PHOTO = 3
    DOCUMENT = 4
    VIDEO = 5
    AUDIO_MESSAGE = 6
    BUBBLE_MESSAGE = 7

    def __str__(self):
        return str(self.name)

class Message:
    @staticmethod
    def from_tg_message(tg_message):
        message = Message()
        message.id = tg_message.id
        message.text = tg_message.text
        message.datetime = tg_message.date
        peer = Peer.from_tg_peer(tg_message.peer_id)
        message.peer_id = peer.id
        
        if peer.type == PeerType.USER:
            message.from_user_id = peer.id
        else:
            message.from_user_id = tg_message.from_id

        if tg_message.text != '':
            message.type = MessageType.TEXT

        elif tg_message.media and type(tg_message.media) == types.MessageMediaDocument:
            if tg_message.media.document.mime_type == 'audio/ogg':
                message.type = MessageType.AUDIO_MESSAGE
            elif tg_message.media.document.mime_type == 'video/mp4':
                message.type = MessageType.BUBBLE_MESSAGE
            elif tg_message.media.document.mime_type == 'video/webm':
                message.type = MessageType.VIDEO
            elif tg_message.media.document.mime_type == 'image/webp':
                message.type = MessageType.STICKER
            else:
                message.type = MessageType.UNKNOWN
        elif tg_message.photo and type(tg_message.media) == types.MessageMediaPhoto:
            message.type = MessageType.PHOTO

        else:
            message.type = MessageType.UNKNOWN

        return message

    @staticmethod
    def from_args(id, text, datetime, peer_id, from_user_id, message_type):
        message = Message()
        message.id = id
        message.text = text
        message.datetime = datetime
        message.peer_id = peer_id
        message.from_user_id = from_user_id
        message.type = message_type
        return message

    def __str__(self):
        return str(
            'Message(' +
            str(self.id) + ', ' +
            str(self.text) + ', ' +
            str(self.datetime) + ', ' +
            str(self.from_user_id) + ', ' +
            str(self.peer_id) + ', ' +
            str(self.type) + ')')
