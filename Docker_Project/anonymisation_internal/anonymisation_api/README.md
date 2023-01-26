## Anonymisation API 

API is composed of three docker images: web, celery and redis. Web contains the api itself, celery is for handling the 
long-running task (training) and redis is a backend and broker for celery. 

Read more about the anonymisation pipeline here: <a href="">Anonymisation pipeline README </a>.

### To get models:  
   1. Clone the repo's in `anonymise/models` folder  
              `git clone https://huggingface.co/buerokratt/bert-truecaser`  
              `git clone https://huggingface.co/buerokratt/ner_old`  
              `git clone https://huggingface.co/buerokratt/ner_new`  
              `git clone https://huggingface.co/buerokratt/ner_gdpr`  
   2. Rename folowing folders accordingly  
              `mv ner_old/ bert_old`  
              `mv ner_new/ bert_new`  
              `mv ner_gdpr/ gdpr_model` 
   3. Install `git lfs`  
   
```
sudo apt instal git-lfs
```
   4. Use `git lfs install` and `git lfs pull` inside every model folder to pull and update the larger files

### To run the API: 
1. Put the models in correct folders under `anonymise/models` folder. Models needed (use the same folder name):
   1. `bert-truecaser`
   2. `bert_new` - trained on new Estonian NER dataset
   3. `bert_old` - trained on old Estonian NER dataset
   4. `bert_restricted` - only GDPR labels included
2. Put the pretrained EstNER model in the `anonymise/training/model` that you wish to fine-tune further.
3. Execute command in the `anonymisation_api` folder: 
   
   `$ make all `


## Using the API: 

### Anonymisation endpoint 
To anonymise text, you can use following command: 

   `$ wget -S --header="Accept-Encoding: gzip, deflate" --header='Accept-Charset: UTF-8' --header='Content-Type: application/json'  --post-data '{"texts":["Tartus laupäev 23.07. KAOTATUD suur summa raha heleroosas peegelpinnaga helkivas lukuga kosmeetikakotis, kas Ringtee 7 majas/maja ees,K-Rauta ehituspoes/parklas kell 17-18 vahel. Iga info vajalik,kes ka nägi kedagi sellist kotti millalgi maast üles võtmas või kes teab kedagi, kes alates laupäevast on ootamatult rikastunud ja võis nendes kohtades liikuda, palun anna teada. Korralik vaevatasu ausale tagastajale ja leidjani viiva info jagajale! Tel. +372 55596739"], "tokenize":true, "truecase":true, "pseudonymise":true, "thresholds":{}}'  http://0.0.0.0:5001/predict`

### Output 
Output of the API is a list of dictionaries containing keys `Mapping`, `anonümiseeritud_tekst`, `pseudonümiseeritud_tekst` and `sisendtekst`.
`Mapping` contains list of words (from the input text), each word is represented as a dictionary containing keys: `Algne`, `Asendatud` and `Tag`. 
`Algne` is the word from the initial input text. `Asendatud` is the pseudonymised text if pseudonymisation is set to True, otherwise it is the same as the `Tag`. 
`Tag` is the assigned entity to the word. 
`anonümiseeritud_tekst` is anonymised text, where each detected entity is covered with the detected entity. `pseudonümiseeritud_tekst` is pseudonymised text, where each detected entity is replaced with random entity. 
If pseudonymisation is set to false then the `pseudonümiseeritud_tekst` contains text where detected entities are covered with entity names. 

where each found entity is masked with the entity name. 
The output of the example command would be: 

### Anonymisation endpoint inputs 
<strong> Texts (required)</strong>
The API endpoint expects `texts` as an input, which should be a list of texts. Maximum amount of texts in the list is 100. 

For example: 

`"texts":["Rahapesu on valdkond , mille osakaal Eesti-Soome vahelises kuritegevuses kasvab .", "Bristol Trust on aastaid varustanud Eesti julgeolekuasutusi ja kaitseväge vajaliku kraamiga, alates relvadest ja isikukaitsevahenditest kuni koeratoiduni."]`

When no input of `texts` is included in the API call, API outputs following error: 
`"Message": "'texts' not in request."`

When the amount of texts exceeds 100, then the API outputs following message: 
`Maximum limit of 100 texts is exceeded, current amount 101`


When the input type of `texts` is not list of texts, API outputs following error: 
`"Message": "'texts' should be a list not a <class str>`


<strong> Thresholds (optional) </strong>
`thresholds` is a required input, which should be a dictionary containing entities and their assigned thresholds. For example, when we want to increase the detection of Names, we would specify the dictionary as `{"Nimi":0.5}`. 
If we do not want to assign any thresholds then we should leave the dictionary empty. 
Setting new threshold will increase the amount of entities detected from the text. Setting the thresholds to a small number like {-1...2} will increase the possibility of finding an entity. 
Setting the threshold to something bigger {2..10} will decrease the possibility of marking a word as an entity. 




<strong> Tokenize (optional)</strong>
It is possible to turn the tokenization off when the input text is already correctly tokenized.
For that set the tokenization to false: 

`tokenize:false`

If the API call do not contain `tokenize` input then the API sets tokenization to true by default. 

For example, when the input text is `texts:["Rahapesu on valdkond, mille osakaal Eesti-Soome vahelises kuritegevuses kasvab."]`
and `tokenize:false` (all other inputs are not specified) then the output would be: 
`
[
    {
        "Mapping": [
            {
                "Algne": "Rahapesu",
                "Asendatud": "rahapesu",
                "Tag": "O",
                "end_i": 8,
                "start_i": 0
            },
            {
                "Algne": "on",
                "Asendatud": "on",
                "Tag": "O",
                "end_i": 11,
                "start_i": 9
            },
            {
                "Algne": "valdkond,",
                "Asendatud": "valdkond,",
                "Tag": "O",
                "end_i": 21,
                "start_i": 12
            },
            {
                "Algne": "mille",
                "Asendatud": "mille",
                "Tag": "O",
                "end_i": 27,
                "start_i": 22
            },
            {
                "Algne": "osakaal",
                "Asendatud": "osakaal",
                "Tag": "O",
                "end_i": 35,
                "start_i": 28
            },
            {
                "Algne": "Eesti-Soome",
                "Asendatud": "Kiviõli",
                "Tag": "GPE_1",
                "end_i": 47,
                "start_i": 36
            },
            {
                "Algne": "vahelises",
                "Asendatud": "vahelises",
                "Tag": "O",
                "end_i": 57,
                "start_i": 48
            },
            {
                "Algne": "kuritegevuses",
                "Asendatud": "kuritegevuses",
                "Tag": "O",
                "end_i": 71,
                "start_i": 58
            },
            {
                "Algne": "kasvab.",
                "Asendatud": "kasvab.",
                "Tag": "O",
                "end_i": 79,
                "start_i": 72
            }
        ],
        "anonümiseeritud_tekst": "Rahapesu on valdkond, mille osakaal [b-gpe] vahelises kuritegevuses kasvab.",
        "pseudonümiseeritud_tekst": "Rahapesu on valdkond, mille osakaal kiviõli vahelises kuritegevuses kasvab.",
        "sisendtekst": "Rahapesu on valdkond, mille osakaal Eesti-Soome vahelises kuritegevuses kasvab."
]`


<strong> Truecase (optional)</strong>
Truecasing handles the casing of the words in the input text. If the casing is already correct in the input text, set the 
truecasing to False:

`truecase:false`

If the `truecase` parameter is not included in the API call the API will automatically set the truecasing to True. 

For example, when the input text is `texts:["Rahapesu on valdkond, mille osakaal Eesti-Soome vahelises kuritegevuses kasvab."]`
and `truecase:false` (all other inputs are not specified)  then the output would be: 

`
[
    {
        "Mapping": [
            {
                "Algne": "Rahapesu",
                "Asendatud": "Rahapesu",
                "Tag": "Rahapesu_1",
                "end_i": 8,
                "start_i": 0
            },
            {
                "Algne": "on",
                "Asendatud": "on",
                "Tag": "O",
                "end_i": 11,
                "start_i": 9
            },
            {
                "Algne": "valdkond",
                "Asendatud": "valdkond",
                "Tag": "O",
                "end_i": 20,
                "start_i": 12
            },
            {
                "Algne": ",",
                "Asendatud": ",",
                "Tag": "O",
                "end_i": 21,
                "start_i": 20
            },
            {
                "Algne": "mille",
                "Asendatud": "mille",
                "Tag": "O",
                "end_i": 27,
                "start_i": 22
            },
            {
                "Algne": "osakaal",
                "Asendatud": "osakaal",
                "Tag": "O",
                "end_i": 35,
                "start_i": 28
            },
            {
                "Algne": "Eesti-Soome",
                "Asendatud": "Kiviõli",
                "Tag": "GPE_1",
                "end_i": 47,
                "start_i": 36
            },
            {
                "Algne": "vahelises",
                "Asendatud": "vahelises",
                "Tag": "O",
                "end_i": 57,
                "start_i": 48
            },
            {
                "Algne": "kuritegevuses",
                "Asendatud": "kuritegevuses",
                "Tag": "O",
                "end_i": 71,
                "start_i": 58
            },
            {
                "Algne": "kasvab",
                "Asendatud": "kasvab",
                "Tag": "O",
                "end_i": 78,
                "start_i": 72
            },
            {
                "Algne": "R",
                "Asendatud": ".",
                "Tag": "O",
                "end_i": 1,
                "start_i": 0
            }
        ],
        "anonümiseeritud_tekst": "Rahapesu on valdkond, mille osakaal [b-gpe] vahelises kuritegevuses kasvab.",
        "pseudonümiseeritud_tekst": "Rahapesu on valdkond, mille osakaal kiviõli vahelises kuritegevuses kasvab.",
        "sisendtekst": "Rahapesu on valdkond, mille osakaal Eesti-Soome vahelises kuritegevuses kasvab."
    }
]
`

<strong> Pseudonymise (optional)</strong>

Pseudonymisation will replace detected entities with new random words that belong to the same category as the initial word. This means
that when `Nimi` is detected from the input text, it will be replaced with new random name. 

If the pseudonymisation is not needed, set the `pseudonymise` to False: 

`pseudonymise:false`

If the pseudonymisation is not specified in the API call then it will be automatically set to True. 

For example, when the input text is `texts:["Rahapesu on valdkond, mille osakaal Eesti-Soome vahelises kuritegevuses kasvab."]`
and `pseudonymise:false` (all other inputs are not specified) then the output would be: 
`[
    {
        "Mapping": [
            {
                "Algne": "Rahapesu",
                "Asendatud": "Rahapesu",
                "Tag": "O",
                "end_i": 8,
                "start_i": 0
            },
            {
                "Algne": "on",
                "Asendatud": "on",
                "Tag": "O",
                "end_i": 11,
                "start_i": 9
            },
            {
                "Algne": "valdkond",
                "Asendatud": "valdkond",
                "Tag": "O",
                "end_i": 20,
                "start_i": 12
            },
            {
                "Algne": ",",
                "Asendatud": ",",
                "Tag": "O",
                "end_i": 21,
                "start_i": 20
            },
            {
                "Algne": "mille",
                "Asendatud": "mille",
                "Tag": "O",
                "end_i": 27,
                "start_i": 22
            },
            {
                "Algne": "osakaal",
                "Asendatud": "osakaal",
                "Tag": "O",
                "end_i": 35,
                "start_i": 28
            },
            {
                "Algne": "Eesti-Soome",
                "Asendatud": "GPE_1",
                "Tag": "GPE_1",
                "end_i": 47,
                "start_i": 36
            },
            {
                "Algne": "vahelises",
                "Asendatud": "vahelises",
                "Tag": "O",
                "end_i": 57,
                "start_i": 48
            },
            {
                "Algne": "kuritegevuses",
                "Asendatud": "kuritegevuses",
                "Tag": "O",
                "end_i": 71,
                "start_i": 58
            },
            {
                "Algne": "kasvab",
                "Asendatud": "kasvab",
                "Tag": "O",
                "end_i": 78,
                "start_i": 72
            },
            {
                "Algne": ".",
                "Asendatud": ".",
                "Tag": "O",
                "end_i": 78,
                "start_i": 79
            }
        ],
        "anonümiseeritud_tekst": "rahapesu on valdkond, mille osakaal [B-GPE] vahelises kuritegevuses kasvab.",
        "pseudonümiseeritud_tekst": "Rahapesu on valdkond, mille osakaal GPE_1 vahelises kuritegevuses kasvab.",
        "sisendtekst": "Rahapesu on valdkond, mille osakaal Eesti-Soome vahelises kuritegevuses kasvab ."
    }
]`


<strong> Disabled entities (optional) </strong>

When some of the entities are not needed to be detected, it is possible to turn these entities off with 
`disabled_entities` option, which takes in a list of strings. Each element in the list is a entity. 
Available entities are:<br>
<strong>Nimi</strong> <br>
<strong>GPE</strong> <br>
<strong>Aadress</strong>  <br>
<strong>Asutus</strong> <br>
<strong>Toode</strong>  <br>
<strong>Sündmus </strong>  <br>
<strong>Kuupäev </strong> <br>
<strong>Aeg </strong> <br>
<strong>Tiitel </strong> <br>
<strong>Raha </strong> <br>
<strong>Protsent </strong> <br>
<strong>Dokumendinr </strong> <br>
<strong>Kaardinr</strong>   <br>
<strong>IBAN</strong>   <br>
<strong>Isikudokumendinr</strong>  <br>
<strong>Isikukood</strong>  <br>
<strong>Email</strong>   <br>
<strong>Telefon</strong>   <br>
<strong>Parool</strong>  <br>
<strong>Autonumber</strong>   <br> 




<strong> Detokenize (optional) </strong>
Detokenization will correct the tokenization of the output sentence. When the detokenization is set to False then 
each word in the sentence will be separated by a whitespace, this also includes punctuation. 






### Training endpoint

To train a model call: 


   `$ wget -S --header="Accept-Encoding: gzip, deflate" --header='Accept-Charset: UTF-8' --header='Content-Type: application/json'   http://0.0.0.0:5001/train`

Training data should go to `/app/training/data` inside the celery worker docker container. 
Needed files: 
- EstNER_new_dev.json
- EstNER_new_test.json
- EstNER_new_train.json
- labels.txt 

Dataset files can have other named entities that are not listed in the labels.txt file. These extra entities will be filtered out when the dataset is loaded in. 
The model fill be saved in `/app/training/model` folder inside the worker container. 



## Logging 
API log is output to the folder /logs/gunicorn.log. All errors are saved there. 
Celery has its own logging, this is output into celery/logs/celery.log folder. This log contains the 
information about the training process.



