import psycopg2
import datetime
import utils

import pyrogram.enums.chat_type

chat_type = utils.EnumToIntConverter()

class MyMessage():
    text = ''
    author = ''


class Db:
    def __init__(self, database, user, password, host, port):
        self.connection = psycopg2.connect(
            database="telegram_my_messages", user='postgres', password='3228', host='127.0.0.1', port='5432'
        )

        self.connection.autocommit = True
        self.cursor = self.connection.cursor()

    def get_last_message(self):
        self.cursor.execute(
            'SELECT messages.text, user_name FROM messages JOIN users u on u.id = messages.user_id ORDER BY messages.id DESC LIMIT 1', )
        message_records = self.cursor.fetchall()
        result = ''
        for row in message_records:
            result += row[0]
            result += ' '
            result += row[1]
        return result


    def add_message(self, message):
        insert_message = (
            message.id,
            message.text,
            datetime.datetime.timestamp(message.date) * 1000,
            message.from_user.id,
            chat_type.enum_to_int(message.chat.type.value),
            1)
        self.cursor.execute(
            'INSERT INTO messages (id, text, datetime, user_id, chat_type, media_type) VALUES (%s,%s,%s,%s,%s,%s)',
            insert_message)

    def is_new_user(self, user):
        self.cursor.execute('SELECT * FROM users WHERE id = %s', [user.id])
        user_records = self.cursor.fetchall()
        if len(user_records) == 1:
            return False
        else:
            return True


    def add_user(self, user):
        insert_message = (
            user.id,
            user.first_name,
            user.last_name,
            user.username,
            user.is_bot,
            user.is_contact)
        self.cursor.execute(
            'INSERT INTO users (id, first_name, second_name, user_name, is_bot, is_in_contacts) VALUES (%s,%s,%s,%s,%s,%s)',
            insert_message)


    def add_unread_message(self, message):
        try:
            self.cursor.execute('INSERT INTO unread_messages (message_id) VALUES (%s)', [message.id])
        except psycopg2.errors.UniqueViolation:
            ...
        except psycopg2.errors.ForeignKeyViolation:
            ...


    def get_unread_messages(self):
        self.cursor.execute(
            'SELECT m.text, user_name FROM unread_messages '
            'JOIN messages m on m.id = unread_messages.message_id '
            'JOIN users u on u.id = m.user_id '
            'ORDER BY m.id ', )
        message_records = self.cursor.fetchall()
        result = list()
        for row in message_records:
            message = MyMessage()
            message.text = row[0]
            message.author = row[1]
            result.append(message)
        return result