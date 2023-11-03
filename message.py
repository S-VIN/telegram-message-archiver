from peer import Peer


class Message:
    @staticmethod
    def from_tg_message(tg_message):
        message = Message()
        message.id = tg_message.id
        message.text = tg_message.text
        message.datetime = tg_message.date
        peer = Peer(tg_message.peer_id)
        message.peer_id = peer.id
        if peer.type == Peer.type.USER:
            message.from_user_id = peer.id
        else:
            message.from_user_id = tg_message.from_id

        return message

    @staticmethod
    def from_args(id, text, datetime, peer_id, from_user_id):
        message = Message()
        message.id = id
        message.text = text
        message.datetime = datetime
        message.peer_id = peer_id
        message.from_user_id = from_user_id
        return message

    def __str__(self):
        return str(
            'Message(' +
            str(self.id) + ', ' +
            str(self.text) + ', ' +
            str(self.datetime) + ', ' +
            str(Peer(self.from_user_id)) + ')') # TODO тут сделать вывод и не преобразовывать к Peer
