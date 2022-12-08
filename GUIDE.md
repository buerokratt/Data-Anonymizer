# Kasutusõpetus
See the English version below.

## Sisukord
1. [Sissejuhatus](#intro-et)
2. [Teksti anonümiseerimine](/#anonymizer-et)
3. [Korpuse üleslaadimine](/#corpus-et)
4. [Teksti märgendamine](/#pre-labeling-et)
5. [Treeni oma mudel](/#training-et)

# User Guide
## Content
1. [Introduction](/#intro-en)
2. [How to anonymize a text](/#anonymizer-en)
3. [Upload a custom corpora](/#corpus-en)
4. [Pre-label text in corpora](/#pre-labeling-en)
5. [How to train a custom model](/#training-en)

## EST
### <a href="#intro-et"></a>1. Sissejuhatus

**Bürokrati Anonümiseerija** on [Riigi Infosüsteemi Ameti](https://www.ria.ee/) tellimusel loodud tarkvararakendus, mis võimaldab kasutajal 
anonümiseerida etteantavat eestikeelset teksti nii rakenduses kui ka rakendusliidese
(API) kaudu. 

Rakendus jaguneb ```anonümiseerimis-```, ```treenija-``` ja ```märgendamismooduliks```.

Anonümiseerijaga on võimalik tuvastada nimeolemeid (NER)
kui ka ületreenida vastavalt vajadusele uus nimeolemi tuvastamise mudel, kasutades
oma kohandatud korpust.

### 2. Teksti anonümiseerimine

Teksti anonümiseerija töötab eestikeelsete tekstidega. Selleks, et teksti
anonümiseerida, tuleb sisestada tekstiväljale ning vajutada nupule 
```Anonümiseeri tekst```. Teksti anonümiseerimise tulemusel ilmub väljundtekst
kõrvalolevasse väljundkasti. Teksti sisendkasti ilmub algse teksti asemel
tuvastatud nimeolemitega tekst.

Samm 1: Sisesta tekst ja vajuta ```Anonümiseeri tekst``` nupule.

Samm 2: Nimeolemitega märgendatud tekst ilmub algse teksti asemele ning väljundis
on kuvatud anonümiseeritud tekst.

### 3. Korpuse üleslaadimine

Korpuse üleslaadimine on esimene samm kohandatud nimeolemituvastusmudeli treenimiseks.

##### 3.1 Näidiskorpus 
Korpus on ```UTF-8``` kodeeringus tekstifail, mis sisaldab igal real lause või lauseid, mida soovitakse üles laadida,
et treenida uus kohandatud nimeolemituvastuse ```NER mudel```.

Näidiskorpuse sisu failis ```korpus.txt```:
```
Mina olen Maris Kask ning elan Pärnu-Jaagupis.
Eile ma kasutasin 35 protsenti oma nutitelefoni akut.
...
```
Korpuse üleslaadimiseks, vajutage ```Treenija``` moodulis nupule ```Vali fail```,
näidake oma kohalikul kettal asuv fail ning laadige korpus rakendusse.

Samm 1: Lae üles korpuse fail ```korpus.txt```</br>
Samm 2: Korpus on üles laetud

Korpuse laadimine annab veateateid, tulenevalt valest vormingust, 
korpuse suurusest või sisend-väljundveast. Veateade ilmub märguandena.

### 4. Teksti märgendamine

Teksti käsitsi märgendamiseks kasutab rakendus vabavaralise märgendamisrakenduse [Label Studio](https://labelstud.io/)
kohandatud versiooni. Teksti automaatne märgendamine toimub, kasutades 
olemasolevat või treenitud ```NER mudelit```.

#### 4.1 Teksti automaatne eelmärgendamine
Selleks, et märgendada nimeolemeid korpuses, tuleb kõigepealt laadida korpus üles, pärast
korpuse edukat üleslaadimist, tuleb takenduse treeningmoodulis vajutada nuppu 
```EELMÄRGENDA KORPUS```, misjärel korpus eelmärgendatakse. Kui eelmärgendamine on lõppenud, suunatakse kasutaja 
```märgendamisliidesesse```, et vajadusel tekstid käsitsi üle märgendada.

#### 4.2 Täiendav käsitsi märgendamine
Täiendavaks käsitsi märgendamiseks on vajalik korpus üles laadida, soovi korral 
automaatselt eelmärgendada (ei ole kohustuslik) ning seejärel vajutada nuppu 
```Märgenda täiendavalt käsitsi```. 

Kasutaja suunatakse märgendamisliidesesse, kus on võimalik teha tekst aktiivseks 
ning seejärel vastava olemiga märgendada. 

Samm 1: Vajuta nupule ```Märgenda täiendavalt käsitsi```</br>
Samm 2: Märgenda tekst märgendusliideses

#### 4.3 Täiendavate nimeolemite lisamine ja kustutamine
Täiendavate olemite lisamise vajadus võib tekkida, kui olemasolevad nimeolemid ei tuvasta
piisavalt teie kohandatud mudelis. Täiendavaid nimeolemeid saab lisada ja kustutada, kasutades ```Treenija```
moodulis nuppu ```Lisa uus olem``` 

Samm 1: Lisa uus olem, vajutades nupule ```Lisa uus olem```
Samm 2: Kustutamine - eemalda olem nimekirjast

#### 4.4 Täiendavate mustrite lisamine nimeolemi tuvastuseks
Täiendavate mustrite vajadus võib tekkida, kui soovite defineerida  
olemasolevatele nimeolemitele spetsiifilist mustrit, mida nimeolemina tuvastatakse. 

Täiendavate mustri lisamiseks on vajalik see defineerida ```regex```-muster, 
määrata olem, mida antud muster tuvastab ning see salvestada.

Regex kasutab POSIX notatsiooni, regexit saab kontrollida ja katsetada näiteks eelnevalt
[regex101.com](https://regex101.com/).

Samm 1: Defineeri regex muster</br>
Samm 2: Määra tuvastatav olem</br>
Samm 3: Salvesta muster

### 5. Treeni oma mudel
Mudeli ületreenimise vajadus tekib, kui soovite lisaks avalikule korpusele 
kasutada spetsiifilisi nimeolemeid ning neid hiljem tuvastada ja anonümiseerida tekstis.

Mudeli treenimise eeldused on:
1. Olete laadinud üles oma korpuse ja/või lisanud täiendavalt uusi mustreid olemasolevasse korpusse
2. Olete märgendanud üles laetud korpuse, kasutades kas automaatset, käsitsi või mõlemat viisi.

Mudeli treenimisel salvestatakse kohalikule kettale viimane treenitud mudel, mida 
saab anonümiseerimisel vastavalt kasutada.

Treenida saab korraga üks kasutaja, mitut treeningut korraga ei käivitata.

Treenimise lõpetamisel antakse kasutajale märku ning mudel salvestatakse kohalikule kettale.

Rakendus kasutab viimast treenitud mudelit, kui see on loodud. Vaikimisi
kasutab rakendus avalikus repositooriumis kasutatavat mudelit.

Samm 1: Korpus on üles laetud ja märgendatud</br>
Samm 2: Alusta treenimist</br>
Samm 3: Treenimine on lõpetatud ja mudel salvestatud kettale


## EN
### 1. Introduction
Bürokratt Anonümiseerija (Anonymizer) is a software application created by Estonian [State Information Authority](https://www.ria.ee), 
which allows the user to anonymize the given Estonian text both in the application and through 
the application programming interface (API).

The application is consists of ```Anonymization```, ```Trainer``` and ```Labeling Interface``` modules.

With the application, it is possible to perform name entity recognition (NER) task as well as overtrain a new NER model using your custom corpus.

### 2. How to anonymize a text
The text anonymizer works with Estonian texts. In order to anonymize 
the text, you have to enter it in the text field and press 
the ```Anonymize Text``` button. As a result of text anonymization, 
the output text appears in the adjacent output box. 
In the text input box, the text with the identified name 
entities appears instead of the original text.

Step 1: Enter the text and press the ```Anonymize Text``` button.</br>
Step 2: The text tagged with Name Entities will appear in place of the original text 
while the anonymized text will be displayed in the output.

### 3. Upload a custom corpora
Uploading the corpus is the first step in training a custom name entity recognition model.

#### 3.1 Making a new corpora
A corpora is a ```UTF-8``` encoded text file that contains a sentence 
or sentences on each line that you want to upload to train a new custom name entity recognition (NER) model.

Contents of sample corpora in file ```corpora.txt``` (In Estonian):
```
Mina olen Maris Kask ning elan Pärnu-Jaagupis.
Eile ma kasutasin 35 protsenti oma nutitelefoni akut.
...
```
To upload a corpora, press the ```Choose File``` button in the ```Trainer Module```, 
point to the file on your local drive, and upload the corpora 
to the application.

Step 1: Upload the corpora file ```corpora.txt```</br>
Step 2: The corpora is uploaded

Loading gives an error messages due to incorrect format, 
too big file size, or I/O error. 
The error message appears as a notification.

### 4. Pre-label text in corpora
The application uses a customized version of the open source labeling 
application [Label Studio](https://www.labelstudio.io) to manually label text. 
Automatic text labeling is done using an existing or overtrained NER model.

#### 4.1 Automatic pre-labeling of text
In order to label the name entities in the corpora, the corpora must 
first be uploaded. After successfully uploading the corpus, the 
button ```Pre-label Corpora``` must be pressed to execute pre-labeling, 
after which the corpora will be pre-labeled.
When the pre-labeling is finished, the user is redirected to the 
```Labeling Interface``` to manually re-annotate the texts if necessary.

#### 4.2 Additional manual labeling
For additional manual marking, it is necessary to upload the corpora, 
pre-label it automatically if necessary (not mandatory), and then press 
the ```Label Manually``` button.

The user is directed to the ```Labeling Interface```, 
where it is possible to make the text active and then tag with the 
corresponding entity.

Step 1: Click the button ```Label Manually```</br>
Step 2: Annotate the text in the Labeling Interface

#### 4.3 Adding and deleting Named Entities
You may need to add additional entities if the existing name entities
do not sufficiently identify with your custom model. Additional name
entities can be added and deleted using the 
```Add New Entity``` button in the ```Trainer Module```

Step 1: Add a new entity by pressing the button ```Add New Entity```</br>
Step 2: Delete - remove the entity from the list

#### 4.4 Adding additional patterns for name entity recognition
Additional patterns may be needed if you want to define
a pattern specific to existing name entities.

To add additional patterns, it is necessary to define a ```regex``` pattern, specify the entity that this pattern identifies and save it.

Regex uses ```POSIX notation```, regex can be checked and tested in advance eg [regex101.com](https://www.regex101.com).

Step 1: Define the regex pattern
Step 2: Determine the entity to be detected
Step 3: Save the pattern

### 5. How to train a model

The need to overtrain the model arises if you want to use 
specific name entities in addition to the public corpora and 
later identify and anonymize them in the text.

The prerequisites for model training are:

1. You have uploaded your corpra and/or added additional new Named Entity patterns to an existing corpora
2. You have tagged an uploaded corproa using either automatic, manual labeling or both.
3. When training a model, _the last trained model is saved_ on the local disk, which can be used accordingly for anonymization.

One user can train at the same time, several trainings cannot be started at the same time.

When the training is finished, the user is notified and the model is saved on the local disk overwriting 
the existing one.

Application uses last trained model if one exists, by default the application
uses public model.

Step 1: The corpora is uploaded and labeled </br>
Step 2: Start training  </br>
Step 3: Training is complete and the new model is saved to disk
