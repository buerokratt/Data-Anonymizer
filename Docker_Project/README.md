## Functionalities

### Set up Ruuter instance

https://github.com/buerokratt/Data-Anonymizer/issues/61

Set up [Ruuter](Ruuter/) instance with a [docker-compose](docker-compose.yml) configuration.

Always run `docker-compose up -d` to start all docker containers.

### Set up ReSQL instance

https://github.com/buerokratt/Data-Anonymizer/issues/62

Set up [Resql](Resql/) instance, and added docker-compose containers for Resql and Postgres Database.

### Set up Data Model

https://github.com/buerokratt/Data-Anonymizer/issues/74

Add [Resql Query](Resql/templates/production/create_schema.sql) and a [bash script](Resql/listen_server.sh) to create database schema automatically.
