import psycopg2
import telegram
import utils
from peer import Peer
from user import User
from message import Message

chat_type = utils.EnumToIntConverter()


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Db(metaclass=Singleton):

    def __init__(self, database, user, password, host, port):
        self.connection = psycopg2.connect(
            database=database, user=user, password=password, host=host, port=port
        )

        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def add_message(self, message):
        insert_message = (
            message.id,
            message.text,
            message.datetime,
            message.peer_id)

        self.cursor.execute(
            'INSERT INTO messages (id, text, datetime, peer_id) VALUES (%s,%s,%s,%s)',
            insert_message)

    def is_new_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = (%s)', [user_id])
        user_records = self.cursor.fetchall()
        if len(user_records) == 1:
            return False
        else:
            return True

    def add_peer(self, peer):
        insert_message = (
            peer.id,
            peer.type.value,
            peer.name
        )
        self.cursor.execute(
            'INSERT INTO peers (id, type, name) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING',
            insert_message)

    def get_message_by_id(self, message_id):
        self.cursor.execute(
            'SELECT * FROM messages WHERE id=%s', [message_id])
        message_records = self.cursor.fetchall()
        result = list()
        if len(message_records) == 0:
            return None
        if len(message_records) != 1:
            assert 'message with same id'
            return None

        first_record = message_records[0]
        message = Message.from_args(first_record[0], first_record[1], first_record[2], first_record[3], first_record[4])
        return message

# Peer
    def get_peer_by_id(self, peer_id):
        self.cursor.execute(
            'SELECT * FROM peers WHERE id=%s', [peer_id])
        message_records = self.cursor.fetchall()
        result = list()
        if len(message_records) == 0:
            return None
        if len(message_records) != 1:
            assert 'peers with same id'
            return None

        first_record = message_records[0]
        peer = Peer()
        peer.id = first_record[0]
        peer.type = first_record[1]
        peer.name = first_record[2]
        return peer

        async def is_peer_in_db(self, peer_id):
            peer = self.get_peer_by_id(peer_id)
            return peer is not None

    def get_user_by_id(self, user_id):
        self.cursor.execute(
            'SELECT * FROM users WHERE id=%s', [user_id])
        message_records = self.cursor.fetchall()
        result = list()
        if len(message_records) == 0:
            return None
        if len(message_records) != 1:
            assert 'user with same id'
            return None

        first_record = list(message_records[0])
        first_record[1] = '' if first_record[1] is None else first_record[1]
        first_record[2] = '' if first_record[2] is None else first_record[2]
        first_record[3] = '' if first_record[3] is None else first_record[3]

        user = User()
        user.id = first_record[0]
        user.first_name = first_record[1]
        user.last_name = first_record[2]
        user.username = first_record[3]
        user.bot = first_record[4]
        user.contact = first_record[5]
        return user

# User
    def add_user(self, user):
        insert_message = (
            user.id,
            user.first_name,
            user.last_name,
            user.username,
            user.bot,
            user.contact)
        self.cursor.execute(
            'INSERT INTO users (id, first_name, last_name, username, bot, contact) VALUES (%s,%s,%s,%s,%s,%s)',
            insert_message)


