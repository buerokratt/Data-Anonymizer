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

### Automatically pre-label uploaded corpus

https://github.com/buerokratt/Data-Anonymizer/issues/66

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/annotate_corpora.yml

```
curl -X "POST" "http://localhost:8080/annotate_corpora"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/GET/prelabelling_status.yml

```
curl "http://localhost:8080/prelabelling_status"
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/get_latest_corpora.sql

```
curl -X "POST" "http://localhost:8082/get_latest_corpora"
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

### Anonymize/pseudonymize a sentence

https://github.com/buerokratt/Data-Anonymizer/issues/64

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/pseudonymise.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/pseudonymise" --data '{"texts":["hey"],"tokenize":true,"truecase":true,"pseudonymise":true,"thresholds":{"Nimi":2}}'
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

### Upload private corpus to the database

https://github.com/buerokratt/Data-Anonymizer/issues/69

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_corpora_info.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/insert_corpora_info" --data '{"source_file_name": "korpus.txt", "source_file_size": "42323"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/corpora_info.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/corpora_info" --data '{"source_file_name": "korpus.txt", "source_file_size": "42323"}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_corpora_task.sql

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8082/insert_corpora_task/batch" --data '{"queries":[{"raw_text":"Oktoobris oli kinnisvaraturu aktiivsus juba teist kuud languses","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Oktoobris sõlmiti Eesti kinnisvaraturul 3644 ostu-müügitehingut, mida on 32 protsenti vähem kui aasta tagasi samal ajal ning kaheksa protsenti vähem kui eelnenud kuul, selgub maa-ameti andmetest.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Eluruumina müüdud korteriomandiga tehti 1816 tehingut, mis oli 33 protsenti vähem kui 2021. aasta oktoobris.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Hoonestamata maa tehinguid oli 981 ja hoonestatud maa tehinguid 621, mida oli eelmise aasta oktoobriga võrreldes vastavalt 28 ja 38 protsenti vähem.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Tallinnas tehti 702 korteritehingut, mida oli 33 protsenti vähem kui aasta tagasi oktoobris. Septembriga võrdluses jäi pealinna korteritehingute arv samale tasemele. Seejuures esmamüük moodustas pealinna korteritehingutest 28 protsenti.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Tartus müüdi 109 korterit. Kuine tehinguaktiivsus oli viimati nii väike 2020. aasta kevadel. Tartu korteritehingute arv vähenes aastaga ligi 52 protsenti ning eelmise kuuga võrdluses kolmandiku.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Pärnus toimus 70 korteritehingut, mis oli 18 protsenti vähem kui eelmise aasta oktoobris.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Oktoobris maksis Tallinna korteri ruutmeeter keskmiselt 2979 eurot, aastaga kallines ruutmeetri hind 23 protsenti.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Tartus oli korteri ruutmeetri keskmine hind 2343 eurot, aastaga kallines ruutmeetri hind neljandiku. Pärnu korteri ruutmeetri keskmine hind oli oktoobris 2021 eurot, kasvades aastaga 29 protsenti.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"}]}'
```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/corpora.yml

```
curl -H "Content-Type: application/json" -X "POST" "http://localhost:8080/corpora" --data '{"tasks":[{"raw_text":"Oktoobris oli kinnisvaraturu aktiivsus juba teist kuud languses","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Oktoobris sõlmiti Eesti kinnisvaraturul 3644 ostu-müügitehingut, mida on 32 protsenti vähem kui aasta tagasi samal ajal ning kaheksa protsenti vähem kui eelnenud kuul, selgub maa-ameti andmetest.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Eluruumina müüdud korteriomandiga tehti 1816 tehingut, mis oli 33 protsenti vähem kui 2021. aasta oktoobris.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Hoonestamata maa tehinguid oli 981 ja hoonestatud maa tehinguid 621, mida oli eelmise aasta oktoobriga võrreldes vastavalt 28 ja 38 protsenti vähem.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Tallinnas tehti 702 korteritehingut, mida oli 33 protsenti vähem kui aasta tagasi oktoobris. Septembriga võrdluses jäi pealinna korteritehingute arv samale tasemele. Seejuures esmamüük moodustas pealinna korteritehingutest 28 protsenti.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Tartus müüdi 109 korterit. Kuine tehinguaktiivsus oli viimati nii väike 2020. aasta kevadel. Tartu korteritehingute arv vähenes aastaga ligi 52 protsenti ning eelmise kuuga võrdluses kolmandiku.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Pärnus toimus 70 korteritehingut, mis oli 18 protsenti vähem kui eelmise aasta oktoobris.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Oktoobris maksis Tallinna korteri ruutmeeter keskmiselt 2979 eurot, aastaga kallines ruutmeetri hind 23 protsenti.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"},{"raw_text":"Tartus oli korteri ruutmeetri keskmine hind 2343 eurot, aastaga kallines ruutmeetri hind neljandiku. Pärnu korteri ruutmeetri keskmine hind oli oktoobris 2021 eurot, kasvades aastaga 29 protsenti.","corpora_id":"097afbed-761e-4ede-b7d4-97cafdadc488","is_private":true,"created_at":"2022-11-29T14:49:38.090Z"}]}'
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
