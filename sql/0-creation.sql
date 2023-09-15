DO $$
BEGIN
    -- CREATE DATABASE archiever_db;

    CREATE TABLE IF NOT EXISTS users (
      id BIGINT PRIMARY KEY,
      first_name TEXT,
      second_name TEXT,
      user_name TEXT,
      is_bot BOOL DEFAULT FALSE,
      is_in_contacts BOOL DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS messages (
     id BIGINT PRIMARY KEY,
     text TEXT,
     datetime BIGINT NOT NULL,
     user_id BIGINT REFERENCES users(id),
     chat_type INTEGER NOT NULL,
     media_type INTEGER DEFAULT NULL
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


