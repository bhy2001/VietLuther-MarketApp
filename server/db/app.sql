BEGIN TRANSACTION;

DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    student_id TEXT NOT NULL,
    email TEXT NOT NULL,
    phone_number TEXT,
    password_hash TEXT NOT NULL
);


--
-- Structure for table buying request
--
DROP TABLE IF EXISTS buy_request;
CREATE TABLE buy_request (
    id INTEGER PRIMARY KEY,
    initiator_id INTEGER NOT NULL,
    receiver_id INTEGER,
    request_status TEXT NOT NULL, 
    request_time INTEGER NOT NULL,
    accepted_time INTEGER,
    price INTEGER,
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
    FOREIGN KEY (request_id) REFERENCES buy_request (id)

);

INSERT INTO users (id, username, student_id, email, phone_number, password_hash) VALUES (0, 'username1','112345', 'username1@example.com', '1234567890', 'password_hash_1');
INSERT INTO users (id, username, student_id, email, phone_number, password_hash) VALUES (1, 'username2','212345', 'username2@example.com', '2234567890', 'password_hash_2');
INSERT INTO users (id, username, student_id, email, phone_number, password_hash) VALUES (2, 'username3','312345', 'username3@example.com', '3234567890', 'password_hash_3');
INSERT INTO buy_request (id, initiator_id, receiver_id, request_status, request_time, accepted_time,price) VALUES (0, 0, NULL,'available', 000000000000, 100000000000, 30);
INSERT INTO buy_request (id, initiator_id, receiver_id, request_status, request_time, accepted_time,price) VALUES (1, 1, 0, 'accpeted', 000000000000, 200000000000, 40 );
INSERT INTO buy_request (id, initiator_id, receiver_id, request_status, request_time, accepted_time,price) VALUES (2, 2, 0, 'done', 000000000000, 300000000000, 50);

INSERT INTO item (id, request_id, item_name, item_quanity) VALUES (0, 0, "cais", 2);
INSERT INTO item (id, request_id, item_name, item_quanity) VALUES (1, 0,"djt", 3);
INSERT INTO item (id, request_id, item_name, item_quanity) VALUES (3, 1, "con", 4);
INSERT INTO item (id, request_id, item_name, item_quanity) VALUES (4, 1,"me", 5);
INSERT INTO item (id, request_id, item_name, item_quanity) VALUES (5, 2,"cais djt con me", 6);




COMMIT TRANSACTION;
