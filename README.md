## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
```

### Automatically pre-label uploaded corpus

https://github.com/buerokratt/Data-Anonymizer/issues/66

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/annotate_corpora.yml

```
curl -X "POST" "http://localhost:8080/annotate_corpora"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/get_latest_corpora.sql

```
curl -X "POST" "http://localhost:8082/get_latest_corpora"
```

