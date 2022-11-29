## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```
```

### Label a sentence

https://github.com/buerokratt/Data-Anonymizer/issues/43

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/upsert_corpora_task.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/upsert_corpora_task" --data '{"corpora_id": "097afbed-761e-4ede-b7d4-97cafdadc488", "id":932021,"annotated_text":"text","sentences_annotations":"[{\"value\":{\"start\":44,\"end\":48,\"text\":\"2343\",\"labels\":[\"Aadress\"]},\"id\":\"AFPMDbFSpq\",\"from_name\":\"label\",\"to_name\":\"text\",\"type\":\"labels\",\"origin\":\"manual\"}]","annotate_existing_task":false,"project":"097afbed-761e-4ede-b7d4-97cafdadc488"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/annotate.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/annotate?project=097afbed-761e-4ede-b7d4-97cafdadc488" --data '{"id":932021,"annotated_text":"text","sentences_annotations":"[{\"value\":{\"start\":44,\"end\":48,\"text\":\"2343\",\"labels\":[\"Aadress\"]},\"id\":\"AFPMDbFSpq\",\"from_name\":\"label\",\"to_name\":\"text\",\"type\":\"labels\",\"origin\":\"manual\"}]","annotate_existing_task":false,"project":"097afbed-761e-4ede-b7d4-97cafdadc488"}'
```
