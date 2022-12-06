## Functionalities

### Set up Ruuter instance

https://github.com/buerokratt/Data-Anonymizer/issues/61

Set up [Ruuter](Ruuter/) instance with a [docker-compose](docker-compose.yml) configuration.

### Set up ReSQL instance

https://github.com/buerokratt/Data-Anonymizer/issues/62

Set up [Resql](Resql/) instance, and added docker-compose containers for Resql and Postgres Database.

### Set up Data Model

https://github.com/buerokratt/Data-Anonymizer/issues/74

Add [Resql Query](Resql/templates/production/create_schema.sql) and a [bash script](Resql/listen_server.sh) to create database schema automatically.

### Upload private corpus to the database

https://github.com/buerokratt/Data-Anonymizer/issues/69

Add [Ruuter DSL File](Ruuter/DSL/POST/corpora.yml) and [Resql Query](Resql/templates/production/insert_corpora_task.sql) to create tasks in bulk (upload corpora).

### View list of Regex patterns added by user

https://github.com/buerokratt/Data-Anonymizer/issues/86

Add [Ruuter DSL File](Ruuter/DSL/GET/regex.yml) and [Resql Query](Resql/templates/production/list_regex.sql) to list regex patterns.

### Delete added Regex pattern from database

https://github.com/buerokratt/Data-Anonymizer/issues/63

Add [Ruuter DSL File](Ruuter/DSL/GET/delete_regex.yml) and [Resql Query](Resql/templates/production/delete_regex.sql) to delete a regex pattern.
