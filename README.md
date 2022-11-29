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

