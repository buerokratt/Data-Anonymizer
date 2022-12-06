## Anonymisation API 



### To run the API: 
1. Put the models in correct folders under `anonymise/models` folder. Models needed (use the same folder name):
   1. `bert-truecaser`
   2. `bert_new` - trained on new Estonian NER dataset
   3. `bert_old` - trained on old Estonian NER dataset
   4. `bert_restricted` - only GDPR labels included
2. Put the pretrained EstNER model in the `anonymise/training/model` that you wish to fine-tune further.
3. Execute command in the `anonymisation_api` folder: 
   
   `$ make all `


### Using the API: 

### Anonymisation endpoint 
To anonymise text, you can use following command: 

   `$ wget -S --header="Accept-Encoding: gzip, deflate" --header='Accept-Charset: UTF-8' --header='Content-Type: application/json'  --post-data '{"texts":["Tere mina- olen pille pillesalu", "Ma juhuslikult elan kastani 11-18 tänaval"], "tokenize":true, "truecase":true, "pseudonymise":true, "thresholds":{"Nimi":2}}'  http://0.0.0.0:5001/predict`

The API endpoint expects `texts` as an input, which should be a list of texts. Maximum amount of texts in the list is 100. 
`thresholds` is a required input, which should be a dictionary containing entities and their assigned thresholds. For example, when we want to increase the detection of Names, we would specify the dictionary as `{"Nimi":0.5}`. 
If we do not want to assign any thresholds then we should leave the dictionary empty. 
Other input `tokenize`, `truecase`. `disabled_entities` and  `pseudonymise` are optional. If these are not specified, then the API will automatically do both: truecasing and tokenization and add no thresholds or disable any entities. 
If you set: 

`tokenize: false` - will not execute tokenization. Will split on whitespaces. 

`truecase: false` - will not execute truecasing. All casing is left as it was inputted. 

`pseudonymise: false` - will not do pseudonymisation. 

`thresholds: {}` - Add thresholds for detecting entities (Increases recall). If empty dictionary is attached, then no thresholding will be done.

`disabled_entities: []` - will not disable any entities from detected entities.  


<strong>Threshold configuration </strong>

Setting new threshold will increase the amount of entities detected from the text. Setting the thresholds to a small number like {-1...2} will increase the possibility of finding an entity. 
Setting the threshold to something bigger {2..10} will decrease the possibility of marking a word as an entity. 


<strong> Disabling entities </strong>
It is possible to not detect certain entities. If we set the `disabled_entities`:["Nimi"] then the API will not detect and cover any names. 


Output of the API is a list of dictionaries containing keys `Mapping`, `anonümiseeritud_tekst`, `pseudonümiseeritud_tekst` and `sisendtekst`.
`Mapping` contains list of words (from the input text), each word is represented as a dictionary containing keys: `Algne`, `Asendatud` and `Tag`. 
`Algne` is the word from the initial input text. `Asendatud` is the pseudonymised text if pseudonymisation is set to True, otherwise it is the same as the `Tag`. 
`Tag` is the assigned entity to the word. 
`anonümiseeritud_tekst` is anonymised text, where each detected entity is covered with the detected entity. `pseudonümiseeritud_tekst` is pseudonymised text, where each detected entity is replaced with random entity. 
If pseudonymisation is set to false then the `pseudonümiseeritud_tekst` contains text where detected entities are covered with entity names. 

where each found entity is masked with the entity name. 
The output of the example command would be: 
`
[
    {
        "Mapping": [
            {
                "Algne": "Tere",
                "Asendatud": "tere",
                "Tag": "O"
            },
            {
                "Algne": "mina-",
                "Asendatud": "mina-",
                "Tag": "O"
            },
            {
                "Algne": "olen",
                "Asendatud": "olen",
                "Tag": "O"
            },
            {
                "Algne": "pille",
                "Asendatud": "Marek",
                "Tag": "Nimi_1"
            },
            {
                "Algne": "pillesalu",
                "Asendatud": "Mitt",
                "Tag": "Nimi_1"
            }
        ],
        "anonümiseeritud_tekst": "tere mina- olen [B-Nimi] [I-Nimi]",
        "pseudonümiseeritud_tekst": "tere mina- olen Marek Mitt",
        "sisendtekst": "Tere mina- olen pille pillesalu"
    },
    {
        "Mapping": [
            {
                "Algne": "Ma",
                "Asendatud": "ma",
                "Tag": "O"
            },
            {
                "Algne": "juhuslikult",
                "Asendatud": "juhuslikult",
                "Tag": "O"
            },
            {
                "Algne": "elan",
                "Asendatud": "elan",
                "Tag": "O"
            },
            {
                "Algne": "Kastani 11-18",
                "Asendatud": "Valeri tškalovi 77-43",
                "Tag": "Aadress_1"
            },
            {
                "Algne": "tänaval",
                "Asendatud": "tänaval",
                "Tag": "O"
            }
        ],
        "anonümiseeritud_tekst": "ma juhuslikult elan [B-Aadress] [I-Aadress] tänaval",
        "pseudonümiseeritud_tekst": "ma juhuslikult elan Valeri tškalovi 77-43  tänaval",
        "sisendtekst": "Ma juhuslikult elan Kastani 11-18 tänaval"
    }
]`

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





