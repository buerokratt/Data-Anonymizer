## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```

```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```

```

### Train a custom model

https://github.com/buerokratt/Data-Anonymizer/issues/65

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/train.yml

```
curl -X "POST" "http://localhost:8080/train"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/training_status.yml

```
curl "http://localhost:8080/training_status"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/upsert_corpora_info.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/upsert_corpora_info" --data '{"corpora_id": "some-corpora-id"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/update_corpora_info.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/update_corpora_info" --data '{"corpora_id": "some-corpora-id"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/get_trained_corpora_info.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/get_trained_corpora_info"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/trained_corpora_info.yml

```
curl "http://localhost:8080/trained_corpora_info"
```
