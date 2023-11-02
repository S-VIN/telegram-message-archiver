from peer import Peer


class Message:
    def __init__(self, tg_message=None):
        if tg_message is None:
            return
        self.id = tg_message.id
        self.text = tg_message.text
        self.datetime = tg_message.date
        self.peer_id = Peer(tg_message.peer_id).id
        self.from_user_id = tg_message.from_id

    def __str__(self):
        return str('Message(' + str(self.id) + ', ' + str(self.text) + ', ' + self.datetime + ', ' + self.from_user_id + ')')
