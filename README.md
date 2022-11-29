## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
``` 

### View list of Regex patterns added by user

https://github.com/buerokratt/Data-Anonymizer/issues/60

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/list_regex.sql

```
curl -X "POST" "http://localhost:8082/list_regex"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/regex.yml

```
curl "http://localhost:8080/regex"
```
