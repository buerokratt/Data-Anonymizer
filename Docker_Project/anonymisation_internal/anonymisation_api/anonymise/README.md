# Anonymisation pipeline 
Anonymisation pipeline contains four separate parts: tokenization, truecasing, named entity recognition (NER) and pseudonymisation. 

Anonymisation pipeline can identify and pseudonymise following entities: 

<strong>Nimi</strong> - nt Mari Maasikas, Mart Mardikas<br>
<strong>GPE</strong>  - nt Tartu, Eesti, Euroopa<br>
<strong>Aadress</strong>  - nt Tartu, Rüütli 7, Harjumaa <br>
<strong>Asutus</strong>  - nt <br>
<strong>Toode</strong>  <br>
<strong>Sündmus </strong> - <br>
<strong>Kuupäev </strong> - nt täna, homme, 13.01.2022 <br>
<strong>Aeg </strong> - nt 14:15, 17:56<br>
<strong>Tiitel </strong> - nt president, kirjanik <br>
<strong>Raha </strong> - nt 100 eurot, 1200EUR<br>
<strong>Protsent </strong> - 12%, 19%<br>
<strong>Dokumendinr </strong> <br>
<strong>Kaardinr</strong>   <br>
<strong>IBAN</strong>   <br>
<strong>Isikudokumendinr</strong>  <br>
<strong>Isikukood</strong>  - nt 49905022723<br>
<strong>Email</strong>  - nt mari.maasikas@gmail.com, mart_mardikas@hotmail.ee <br>
<strong>Telefon</strong>  - nt 57840387, +372 58923420 <br>
<strong>Parool</strong>  - nt parool123, qwerty111<br>
<strong>Autonumber</strong>  - nt 633MGI, 234MMG <br> 

Pipeline uses the inside-outside-beginning (IOB) format. This means that when entity starts with B- it indicaets 
that the tag is the beginning of a chunk, I-prefix before the entity indicates that this part is inside a chunk. 
For example `Tartu maakond` would be tagged as `B-Aadress I-Aadress`. O tag indicates that the word is not belonging to any chunk. 

## Tokenization 
Tokenization is done by using <a href="https://stanfordnlp.github.io/stanza/available_models.html">Stanza Estonian pipeline </a>,
which is trained on the Universal Dependencies Estonian Dependency Treebank. 

## Truecasing 
This part of the pipeline handles casing the input text. Often the input text might not be 
cased properly. Poorly cased input text might negatively impact the next step of the pipeline called named entity recognition (NER).
Truecasing is done by using fine-tuned EstBERT model,  more specifically the EstBERT model fine-tuned on the Universal Dependencies Estonian Dependency Treebank (v2.11). 

## NER  
Named entity recognition has three separate methods for different entities: regex, matching entities from gazetteer and pretrained models. 

<strong>Regex matches following entities: </strong><br>
Dokumendinr <br>
Kaardinr <br>
IBAN <br>
Isikudokumendinr <br>
Isikukood <br>
Email <br>
Telefon <br>
Parool <br>
Autonumber <br>

<strong>Following entities are matched using gazetteers: </strong><br>
Asutus <br>
Aadress <br>

Gazetteers are known collection of entities. 

<strong>Models match these entities: </strong><br>
Asutus <br>
Aadress <br>
Nimi<br>
GPE <br>
Toode <br>
Sündmus <br>
Kuupäev <br>
Aeg <br>
Tiitel <br>
Raha <br>

There are three pre-trained BERT models that are trained on different datasets. 

The pipeline prefers the prediction of model and then regex and gazetteer. The prediction scores of the models are also used when matching entities with regex. This means
that when the model's confidence about the particular word being that entity is too low, the pipeline will not recognize the matched entity. 


## Pseudonymisation 
Pseudonymisation is done by using gazetteers and regex patterns. All the entities that are matched with regex are also pseudonymised by using the same regex pattern to create new entity. 
Other entities matched by models are pseudonymised by using gazetteers and changing the form of the new random entity. 
Form is changed by using EstNLTK library. 

# Training 
