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
    async def get_peer_by_id(self, peer_id):
        if type(peer_id) is types.PeerChannel:
            result = await self.client(functions.channels.GetFullChannelRequest(
                channel=peer_id
            ))
            return Peer(peer_id)

        if type(peer_id) is types.PeerUser:
            result = await self.client(functions.users.GetFullUserRequest(peer_id))
            print(result)
            return Peer(peer_id)

        if type(peer_id) is types.PeerChat:
            result = await self.client(functions.messages.GetPeerDialogsRequest(
                peers=[peer_id]
            ))
            print(result.chats[0].title)
            return Peer(peer_id)

    async def get_user_by_id(self, user_id):
        user = await self.client(functions.users.GetFullUserRequest(user_id))
        return user
