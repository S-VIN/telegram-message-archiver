DO $$
BEGIN
    -- CREATE DATABASE archiever_db;

    CREATE TABLE IF NOT EXISTS users (
      id BIGINT PRIMARY KEY,
      first_name TEXT,
      last_name TEXT,
      username TEXT,
      bot BOOL DEFAULT FALSE,
      contact BOOL DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS messages (
     id BIGINT PRIMARY KEY,
     text TEXT,
     datetime TIMESTAMP NOT NULL,
     peer_id BIGINT REFERENCES peers(id),
     chat_type INTEGER NOT NULL
    );

    CREATE TABLE IF NOT EXISTS peers (
     id BIGINT PRIMARY KEY,
     type INT NOT NULL,
     name TEXT NOT NULL
    );

    CREATE TABLE  IF NOT EXISTS unread_messages (
        message_id BIGINT REFERENCES messages(id) UNIQUE
    );

    CREATE TABLE IF NOT EXISTS last_used_script (
        onerow_id bool PRIMARY KEY DEFAULT TRUE,
        script_name TEXT,
        CONSTRAINT onerow_uni CHECK (onerow_id)
    );
END;
$$;


