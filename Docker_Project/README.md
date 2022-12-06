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

### Set up Label Studio

https://github.com/buerokratt/Data-Anonymizer/issues/45

Set up [Label Studio Frontend](Label-Studio/) React Application, and add docker-compose configuration. Environment Variable for Backend (Ruuter Application) should be set up [here](Label-Studio/.env.defaults). The website url for this application should be added list of [whitelisted urls](Ruuter/src/main/java/ee/buerokratt/ruuter/controller/DslController.java#L28) for Ruuter.

### Setup React Application for Data Management Frontend Application

https://github.com/buerokratt/Data-Anonymizer/issues/93

Set up [Data Management Frontend](dm/) React Application, and add docker-compose configuration.

### Define routes for Anonymizer and Training Pages

https://github.com/buerokratt/Data-Anonymizer/issues/94

Define [routes](dm/src/App.js) for [Anonymizer](dm/src/components/Anonymizer.js) and [Training](dm/src/components/Treening.js) components.

### Implement UI Design for Page Header, Navigation, Drawer and Footer

https://github.com/buerokratt/Data-Anonymizer/issues/95

Add UI Components for [Header](dm/src/components/Header.js), [Navigation Mobile Drawer](dm/src/components/Drawer.js), [Footer](dm/src/components/Footer.js) and [Github Section](dm/src/components/GithubSection.js)

### Implement UI Design for Anonymizer Page

https://github.com/buerokratt/Data-Anonymizer/issues/98

Add UI Component for [Anonymizer](dm/src/components/Anonymizer.js) Page.

### Implement UI Design for Training Page

https://github.com/buerokratt/Data-Anonymizer/issues/96

Add UI Component for [Training](dm/src/components/Treening.js) Page.

### UI Backend API Integration

https://github.com/buerokratt/Data-Anonymizer/issues/97

Add [Services](dm/src/RestService.js) to call Backend REST APIs, integrate Anonymizer and Training Pages, and add website url of this application to list of [whitelisted urls](Ruuter/src/main/java/ee/buerokratt/ruuter/controller/DslController.java#L28) for Ruuter.

### Add i18n support to Data Management Interface front end app

https://github.com/buerokratt/Data-Anonymizer/issues/79

Install [i18next](dm/package.json#L10) and [react-i18next](dm/package.json#L13) packages, add [translations](dm/src/translations/et.json), and transform all text in the UI utilize the translations. Languages can be modfied [here](dm/src/index.js#L10).

### Train a custom model

https://github.com/buerokratt/Data-Anonymizer/issues/65

Add [Model Training Service](ml-long-process-service), [docker-compose configuration](docker-compose.yml#L63) and Ruuter DSL Files to [train model](Ruuter/DSL/POST/train.yml) and [get training status](Ruuter/DSL/POST/train.yml).

### Anonymize/pseudonymize a sentence

https://github.com/buerokratt/Data-Anonymizer/issues/64

Add [Anonymizer Service](anonymisation_internal), docker-compose configurations and Ruuter [DSL File](Ruuter/DSL/POST/pseudonymise.yml) to pseudonymise a sentence. The prediction endpoint in Anonymizer Service can be found [here](anonymisation_internal/anonymisation_api/anonymise/accept_request.py).

### Automatically pre-label uploaded corpus

https://github.com/buerokratt/Data-Anonymizer/issues/66

Add Ruuter [DSL File](Ruuter/DSL/POST/annotate_corpora.yml) to pre-label list of corpora sentences and a [ReSQL](Resql/templates/production/get_latest_corpora.sql) query to get full corpora. The annotation endpoint (/annotate_corpora) in Anonymizer Service can be found [here](anonymisation_internal/anonymisation_api/anonymise/accept_request.py).

### Make script to upload a new public NER corpus

https://github.com/buerokratt/Data-Anonymizer/issues/73

Add [script](Upload_Corpora_Git_Script) to upload latest corpora to GitHub. Steps to execute the script:

```
cd Upload_Corpora_Git_Script
npm install
GIT_OWNER="<GIT_OWNER_ID>" GIT_REPO="<GIT_REPO_ID>" GIT_TOKEN="<GIT_PERSONAL_ACCESS_TOKEN>" API_URL="<RUUTER_URL>" node index.js
```
