CREATE TABLE IF NOT EXISTS "user"
(
    id            BIGSERIAL PRIMARY KEY,
    email         TEXT,
    name          TEXT,
    password_hash TEXT,
    login         VARCHAR(255) UNIQUE
);

CREATE TABLE IF NOT EXISTS user_authority
(
    user_id   BIGINT NOT NULL REFERENCES "user" (id),
    authority TEXT   NOT NULL
);

DELETE FROM user_authority;
DELETE FROM "user";

INSERT INTO "user" (id, login, email, name, password_hash)
VALUES (-1, 'admin', 'admin@example.com', 'Admin Name', '$2a$12$YlbrvfwwznrmQNM71UFFvO3krrFnUsKvGcN5zNDBNMpD2w9WDqHuO'), -- password=adminPassword
       (-2, 'user', 'user@example.com', 'User Name', '$2a$12$AXElLQmIKy1EZVSrlO2HnO0dTsHcf4LstadG7a5arYXUAGf5VCeZm'); -- password=userPassword

INSERT INTO user_authority (user_id, authority)
VALUES (-1, 'ADMIN'),
       (-2, 'USER');
