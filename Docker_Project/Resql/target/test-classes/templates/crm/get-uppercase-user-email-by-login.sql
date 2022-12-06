SELECT upper(email) AS email
FROM "user"
WHERE login = :login;
