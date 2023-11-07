from telethon import TelegramClient
from telethon import functions
from telethon import types
from peer import Peer, PeerType
import utils


class Telegram(metaclass=utils.Singleton):
    def __init__(self, session, api_id, api_hash):
        self.client = TelegramClient(session, api_id, api_hash)

# Плохой способ вызывать эту функцию каждый раз, как приходит сообщение.
# Мы дудосим телеграм. Нужно получить сначала все пиры через get_dialogs,
# а потом уже тех, которых нет (должны быть все, кроме удаленных) смотреть через это.
    async def get_peer_by_tg_peer(self, tg_peer):
        if type(tg_peer) is types.PeerChannel:
            result = await self.client(functions.channels.GetFullChannelRequest(
                channel=tg_peer
            ))
            return Peer.from_tg_peer(tg_peer)

        if type(tg_peer) is types.PeerUser:
            result = await self.client(functions.users.GetFullUserRequest(tg_peer))
            print(result)
            return Peer.from_tg_peer(tg_peer)

        if type(tg_peer) is types.PeerChat:
            result = await self.client(functions.messages.GetPeerDialogsRequest(
                peers=[tg_peer]
            ))
            print(result.chats[0].title)
            return Peer.from_tg_peer(tg_peer)

    async def get_user_by_id(self, user_id):
        user = await self.client(functions.users.GetFullUserRequest(user_id))
        return user
