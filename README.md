## Functionalities

### Add new Regex pattern to the database

https://github.com/buerokratt/Data-Anonymizer/issues/59

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Resql/insert_regex.sql

```

```

https://github.com/buerokratt/Data-Anonymizer/blob/main/DSL.Ruuter/POST/regex.yml

```

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
