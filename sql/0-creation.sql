-- CREATE DATABASE telegram_my_messages;

CREATE TABLE users (
  id BIGINT PRIMARY KEY,
  first_name TEXT,
  second_name TEXT,
  user_name TEXT,
  is_bot BOOL DEFAULT FALSE,
  is_in_contacts BOOL DEFAULT TRUE
);

CREATE TABLE messages (
 id BIGINT PRIMARY KEY,
 text TEXT,
 datetime BIGINT NOT NULL,
 user_id BIGINT REFERENCES users(id),
 chat_type INTEGER NOT NULL,
 media_type INTEGER DEFAULT NULL
);

CREATE TABLE unread_messages (
    message_id BIGINT REFERENCES messages(id)
)

