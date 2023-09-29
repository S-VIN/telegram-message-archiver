import psycopg2
import datetime

from telethon import types

import settings
import telegram
import utils

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

    # def get_last_message(self):
    #     self.cursor.execute(
    #         'SELECT messages.text, username FROM messages JOIN users u on u.id = messages.user_id ORDER BY messages.id DESC LIMIT 1', )
    #     message_records = self.cursor.fetchall()
    #     result = ''
    #     for row in message_records:
    #         result += row[0]
    #         result += ' '
    #         result += row[1]
    #     return result


    def add_message(self, message):
        insert_message = (
            message.id,
            message.text,
            message.datetime,
            message.peer_id,
            message.chat_type)

        self.cursor.execute(
            'INSERT INTO messages (id, text, datetime, peer_id, chat_type) VALUES (%s,%s,%s,%s,%s)',
            insert_message)




    def is_new_user(self, user_id):
        self.cursor.execute('SELECT * FROM users WHERE id = (%s)', [user_id])
        user_records = self.cursor.fetchall()
        if len(user_records) == 1:
            return False
        else:
            return True

    def add_peer(self, peer): # TODO change type to my peer
        insert_message = (
            peer.id,
            peer.type.value,
            peer.name
        )
        self.cursor.execute(
            'INSERT INTO peers (id, type, name) VALUES (%s,%s,%s) ON CONFLICT DO NOTHING',
            insert_message)


    async def get_message_by_id(self, message_id):
        self.cursor.execute(
            'SELECT * FROM peers WHERE id=%s', [message_id])
        message_records = self.cursor.fetchall()
        result = list()
        if len(message_records) == 0:
            return None
        if len(message_records) != 1:
            assert('message with same id')
            return None

        first_record = message_records[0]
        message = telegram.Message(first_record[0], first_record[1], first_record[2], first_record[3], first_record[4])
        return message

# Peer
    async def get_peer_by_id(self, peer_id):
        self.cursor.execute(
            'SELECT * FROM peers WHERE id=%s', [peer_id])
        message_records = self.cursor.fetchall()
        result = list()
        if len(message_records) == 0:
            return None
        if len(message_records) != 1:
            assert('peers with same id')
            return None

        first_record = message_records[0]
        peer = telegram.Peer(first_record[0], first_record[1], first_record[2])
        return peer


    async def get_user_by_id(self, user_id):
        self.cursor.execute(
            'SELECT * FROM users WHERE id=%s', [user_id])
        message_records = self.cursor.fetchall()
        result = list()
        if len(message_records) == 0:
            return None
        if len(message_records) != 1:
            assert('user with same id')
            return None

        first_record = message_records[0]
        user = telegram.User(first_record[0], first_record[1], first_record[2], first_record[3], first_record[4], first_record[5])
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


