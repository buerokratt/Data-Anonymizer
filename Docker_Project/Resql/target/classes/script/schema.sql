-- Test schema
CREATE TABLE IF NOT EXISTS user_type
(
    id   bigserial not null primary key,
    type varchar(255)
);

CREATE TABLE IF NOT EXISTS "user"
(
    id            bigserial not null primary key,
    email         varchar(255),
    name          varchar(255),
    username      varchar(255) unique,
    user_type_id  bigint references user_type (id)
);

-- test data

DELETE FROM "user";
DELETE FROM user_type;

INSERT INTO user_type (id, type)
VALUES (1, 'type 1');

INSERT INTO user_type (id, type)
VALUES (2, 'type 2');

INSERT INTO "user" (id, username, email, name, user_type_id)
VALUES (1, 'user1', 'user1@example.com', 'User Number 1', 1);

INSERT INTO "user" (id, username, email, name, user_type_id)
VALUES (2, 'user2', 'user2@example.com', 'User Number 2', 2);
