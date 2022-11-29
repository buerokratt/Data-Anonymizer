## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql
Sample Curl Request: curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/insert_regex" --data '{"regex": "test", "entity": "NAME"}'
```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml
Sample Curl Request: curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/regex" --data '{"regex": "test", "entity": "NAME"}'

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/list_entity.sql
Sample Curl Request: curl -X "POST" "http://localhost:8082/list_entity

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/entity.yml
Sample Curl Request: curl "http://localhost:8080/entity

```
```
