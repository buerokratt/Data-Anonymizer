## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
```

### Add new entity

https://github.com/buerokratt/Data-Anonymizer/issues/89

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_entity.sql
Sample Curl Request: curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/insert_entity" --data '{"name": "NAME", "description": "Name of a person"}'

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/entity.yml
Sample Curl Request: curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/entity" --data '{"name": "NAME", "description": "Name of a person"}'

```
```
