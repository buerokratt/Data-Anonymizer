## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/insert_regex" --data '{"regex": "test", "entity": "NAME"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/regex" --data '{"regex": "test", "entity": "NAME"}'
```

### Automatically pre-label uploaded corpus

https://github.com/buerokratt/Data-Anonymizer/issues/66

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/annotate_corpora.yml

```
curl -X "POST" "http://localhost:8080/annotate_corpora"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/prelabelling_status.yml

```
curl "http://localhost:8080/prelabelling_status"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/get_latest_corpora.sql

```
curl -X "POST" "http://localhost:8082/get_latest_corpora"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/list_entity.sql

```
curl -X "POST" "http://localhost:8082/list_entity"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/entity.yml

```
curl "http://localhost:8080/entity"
```

### Add new entity

https://github.com/buerokratt/Data-Anonymizer/issues/89

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_entity.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/insert_entity" --data '{"name": "NAME", "description": "Name of a person"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/entity.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/entity" --data '{"name": "NAME", "description": "Name of a person"}'
```

### Describe Data Model for Application

https://github.com/buerokratt/Data-Anonymizer/issues/75

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/create_schema.sql

```
curl -X "POST" "http://localhost:8082/create_schema"
```

### Delete added Regex pattern from database

https://github.com/buerokratt/Data-Anonymizer/issues/63

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/delete_regex.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/delete_regex" --data '{"id": 32}'
```

https://github.com/buerokratt/Data-Anonymizer/blobgit/main/DSL.Ruuter/GET/delete_regex.yml

```
curl "http://localhost:8080/delete_regex?id=32"
```

### Anonymize/pseudonymize a sentence

https://github.com/buerokratt/Data-Anonymizer/issues/64

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/pseudonymise.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/pseudonymise" --data '{"texts":["hey"],"tokenize":true,"truecase":true,"pseudonymise":true,"thresholds":{"Nimi":2}}'
```
