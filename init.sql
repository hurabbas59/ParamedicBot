-- init.sql

-- User Table
CREATE TABLE IF NOT EXISTS "user" (
    user_id VARCHAR PRIMARY KEY,
    user_name VARCHAR NOT NULL,
    email VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL
);

-- ChatHistory Table
CREATE TABLE IF NOT EXISTS "chat_history" (
    chat_id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES "user"(user_id),
    chat_hist JSON NOT NULL
);

-- Subscription Table
CREATE TABLE IF NOT EXISTS "subscription" (
    sub_id VARCHAR PRIMARY KEY,
    user_id VARCHAR REFERENCES "user"(user_id),
    license_level VARCHAR NOT NULL,
    sub_plan VARCHAR NOT NULL
);
