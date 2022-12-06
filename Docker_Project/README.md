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

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

- Add [Ruuter DSL File](Ruuter/DSL/POST/regex.yml) and [Resql Query](Resql/templates/production/insert_regex.sql) to add a regex pattern.
- Add [Ruuter DSL File](Ruuter/DSL/GET/entity.yml) and [Resql Query](Resql/templates/production/list_entity.sql) to list entities.

### Add new entity

https://github.com/buerokratt/Data-Anonymizer/issues/89

Add [Ruuter DSL File](Ruuter/DSL/POST/entity.yml) and [Resql Query](Resql/templates/production/insert_entity.sql) to add an entity.

### Show list of sentences and Filter sentences by ID

https://github.com/buerokratt/Data-Anonymizer/issues/46
https://github.com/buerokratt/Data-Anonymizer/issues/47

- Add [Ruuter DSL File](Ruuter/DSL/GET/tasks.yml) and [Resql Query](Resql/templates/production/get_corpora.sql) to list corpora tasks based on pagination and filters.
- Add [Ruuter DSL File](Ruuter/DSL/GET/task.yml) and [Resql Query](Resql/templates/production/get_task.sql) to get a particular task detail.
- Add [Ruuter DSL File](Ruuter/DSL/GET/project.yml) and [Resql Query](Resql/templates/production/project.sql) to get latest corpora id.

### Label a sentence

https://github.com/buerokratt/Data-Anonymizer/issues/43

Add [Ruuter DSL File](Ruuter/DSL/POST/annotate.yml) and [Resql Query](Resql/templates/production/upsert_corpora_task.sql) to annotate a particular sentence with labels.
