## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
``` 

### Anonymize/pseudonymize a sentence

https://github.com/buerokratt/Data-Anonymizer/issues/64

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/pseudonymise.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/pseudonymise" --data '{"texts":["hey"],"tokenize":true,"truecase":true,"pseudonymise":true,"thresholds":{"Nimi":2}}'
```
