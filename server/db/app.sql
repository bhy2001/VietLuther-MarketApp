BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    student_id TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT,
    password_hash TEXT NOT NULL,
);


--
-- Structure for table buying request
--
DROP TABLE IF EXISTS buy_request;
CREATE TABLE buy_request (
    id INTEGER PRIMARY KEY,
    initiator_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    request_status TEXT NOT NULL, -- 1 means done; 0 means pending; 2 means has been declined
    request_time INTEGER NOT NULL,
    accepted_time INTEGER,
    price INTEGER, -- null means discuss price
    FOREIGN KEY (initiator_id) REFERENCES users (id),
    FOREIGN KEY (receiver_id) REFERENCES users (id)
);

--
-- Structure for table Items
--
DROP TABLE IF EXISTS item;
CREATE TABLE item (
    id INTEGER PRIMARY KEY,
    request_id INTEGER NOT NULL,
    item_name TEXT NOT NULL,
    item_quanity INTEGER NOT NULL,
    FOREIGN KEY (request_id) REFERENCES buy_request (id),

);

INSERT INTO users (id, username, student_id, email, phone_number, password_hash, password_salt) VALUES (1000, 'username1','112345', 'username1@example.com', '1234567890', 'password_hash_1', 'password_salt_1');
INSERT INTO users (id, username, student_id, email, phone_number, password_hash, password_salt) VALUES (1001, 'username2','212345', 'username2@example.com', '2234567890', 'password_hash_2', 'password_salt_2');
INSERT INTO users (id, username, student_id, email, phone_number, password_hash, password_salt) VALUES (1002, 'username3','312345', 'username3@example.com', '3234567890', 'password_hash_3', 'password_salt_3');

COMMIT TRANSACTION;
