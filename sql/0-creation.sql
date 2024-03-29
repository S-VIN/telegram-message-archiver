DO $$
BEGIN
    -- CREATE DATABASE archiver_db;

    CREATE TABLE IF NOT EXISTS users (
      id BIGINT PRIMARY KEY,
      first_name TEXT,
      last_name TEXT,
      username TEXT,
      bot BOOL DEFAULT FALSE,
      contact BOOL DEFAULT TRUE
    );

    CREATE TABLE IF NOT EXISTS peers (
     id BIGINT PRIMARY KEY,
     type INT NOT NULL,
     name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS messages (
     id BIGINT PRIMARY KEY,
     text TEXT,
     datetime TIMESTAMP NOT NULL,
     peer_id BIGINT REFERENCES peers(id),
     from_user_id BIGINT REFERENCES users(id),
     type BIGINT
--      media_name TEXT DEFAULT NULL
    );
END;
$$;


