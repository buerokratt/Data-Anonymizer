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


