## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
``` 

### Show list of sentences

https://github.com/buerokratt/Data-Anonymizer/issues/46

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/get_corpora.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/get_corpora" --data '{"where_condition": "corpora_id = '\''c25d0570-dc99-46d6-afb7-80ad46439b3c'\''", "sort_condition": "Corpora_Tasks.\"id\" DESC", "page": "1", "page_size": "30"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/tasks.yml

```
curl "http://localhost:8080/tasks?page=1&page_size=30&where_condition=corpora_id%20=%20%27c25d0570-dc99-46d6-afb7-80ad46439b3c%27&sort_condition=Corpora_Tasks."id"+DESC"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/get_task.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/get_task" --data '{"corpora_id": "c25d0570-dc99-46d6-afb7-80ad46439b3c", "id": 931986}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/task.yml

```
curl "http://localhost:8080/task?id=931986&project=c25d0570-dc99-46d6-afb7-80ad46439b3c"
```

