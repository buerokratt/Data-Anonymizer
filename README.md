## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/insert_regex" --data '{"entity": "NAME", "regex": "test"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/regex" --data '{"entity": "NAME", "regex": "test"}'
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
