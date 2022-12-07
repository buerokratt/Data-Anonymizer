import re
from collections import defaultdict
from flask import Flask
import logging
app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
"""
OLEMID: 
Nimi - M
GPE  - M 
Aadress - M 
Asutus - M + R
Toode - M
Sündmus - M
Kuupäev - M 
Aeg - M 
Tiitel  - M
Raha  - M 
Protsent - M
Dokumendinr - R -
Kaardinr - R 
IBAN - R 
Isikudocumendinr -R 
Isikukood - R
Email  - R
Telefon - R
Parool  - R 
Autonumber  - R 
"""
def read_companies_ner():
    replacements = {'Osaühing': 'OÜ', 'OÜ': 'Osaühing', 'MTÜ': 'Mittetulundusühing',
                    'FIE': 'Füüsilisest isikust ettevõtja', 'Füüsilisest isikust ettevõtja': 'FIE',
                    'Usaldusühing': 'UÜ', 'UÜ': 'Usaldusühing', 'Tulundusühistu': 'TÜ', 'AS': 'Aktsiaselts',
                    'Aktsiaselts': 'AS'}
    # kohaliku omavalitsuse asutus
    companies = []

    with open('../gazetteers/ariregister.txt', 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            line = line.replace('+', '\+')
            line = line.replace('*', '\*')
            line = line.replace('\\', '\\\\')
            line = line.replace('?', '\?')
            line = line.replace('.', '\.')
            line = line.replace('!', '\!')
            line = line.replace('(', '\(').replace(')', '\)')
            companies.append(line)
            companies.append(line.lower())
            for key, value in replacements.items():
                if key in line:
                    companies.append(line.replace(key, value).strip())
                    companies.append(line.replace(key, '').strip())

            if 'Eesti' in line:
                companies.append(line.replace('Eesti', '').strip())
            if 'Erakond' in line:
                companies.append(line.replace('Erakond', '').strip())

    return companies


def read_file(file):
    ents = []

    with open(file, 'r', encoding='utf-8') as f:
        for line in f:
            ents.append(line.strip())
    return ents


def read_companies():
    companies = defaultdict(list)
    with open('../gazetteers/orgs.txt', 'r', encoding='utf-8') as f:
        for line in f:
            companies[len(line.strip().split(' '))].append(line.strip())
    return companies


def read_names(filename):
    names = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.split('\t')
            name = line[1].strip()
            names.append(name)
    return names


def read_streets():
    streets = defaultdict(list)
    with open('../gazetteers/streets.txt', 'r', encoding='utf-8') as f:
        for line in f:
            if line != '\n':
                if line.startswith('!!'):
                    city = line.replace('!! ', '').strip()
                else:
                    streets[city].append(line.strip())
                    if 'tänav' in line:
                        streets[city + '_tänav'].append(line.replace('tänav', '').strip())
                    elif 'maantee' in line:
                        streets[city + '_maantee'].append(line.replace('maantee', '').strip())
                    elif 'puiestee' in line:
                        streets[city + '_puiestee'].append(line.replace('puiestee', '').strip())
                    elif 'tee' in line:
                        streets[city + '_tee'].append(line.replace('tee', '').strip())
                    elif 'põik' in line:
                        streets[city + '_põik'].append(line.replace('põik', '').strip())
                    elif 'väljak' in line:
                        streets[city + '_väljak'].append(line.replace('väljak', '').strip())
                    elif 'park' in line:
                        streets[city + '_park'].append(line.replace('park', '').strip())
                    elif 'plats' in line:
                        streets[city + '_plats'].append(line.replace('plats', '').strip())

    return streets


### regex


def find_nr(text):
    dic = {}
    expression = r"(?:^|(?<=[±|.|,|;|:|\s|!|?|\W)|(]))((\+?\s?359|\+?\s?372|\+?\s?79|\+?\s?49|\+?\s?46|\+?\s?358|\+?\s?44|\+?\s?52)\s|\+?\s?372|\+?\s?79|\+?\s?49|\+?\s?358|\+?\s?44|\+?\s?52|\+?\s?46)?[5|6|7|4|8|1|0][0-9\s-]{4,13}[0-9](?=[.|,|;|:|\s|!|?|)|(]|$)"
    for match in re.finditer(expression, text):
        start, end = match.span()
        found = text[start:end]
        if len(found.split()) > 1:
            no_numbers = sum(c.isdigit() for c in found)
            if no_numbers >= 5:
                for part in found.split():
                    dic[start] = ('Telefoninr', start + len(part), part)
                    start += len(part) + 1
        else:
            if text[start - 1] != ' ' and start != 0:
                i = 1
                while True:
                    if start - i == 0:
                        dic[0] = ('O', end, text[0:start])
                        break
                    if text[start - i] == ' ':
                        dic[start - i + 1] = ('O', end, text[start - i + 1:start])
                        break
                    i += 1

            no_numbers = sum(c.isdigit() for c in found)
            if no_numbers >= 5:
                dic[start] = ('Telefoninr', end, found)
    return dic


BN_REGEX = r"""(?:^|(?<=[.|,|;|:|\s|!|?]))[A-Za-z]{2}[0-9]{18,}(?=[.|,|;|:|\s|!|?]|$)"""
BN_ENT = 'IBAN'

CAR_NR_REGEX = r"""(?:^|(?<=[±|.|,|;|:|\s|!|?|\W)|(]))([0-9]{2,3}\s{0,1}[a-zA-Z]{3}?)(?=[.|,|;|:|\s|!|?]|$)"""
CAR_NR_ENT = 'Autonumber'

ID_REGEX = r"""(?:^|(?<=[.|,|;|:|\s|!|?]))[1-6][0-9]{2}(01|02|03|04|05|06|07|08|09|10|11|12)(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)[0-9]{3}[0-9](?=[.|,|;|:|\s|!|?]|$)"""
ID_ENT = 'Isikukood'

CARD_MAESTRO_NR_REGEX = r"""(?:^|(?<=[.|,|;|:|\s|!|?]))(5018|5020|5038|5612|5893|6304|6759|6761|6762|6763|0604|6390|6759)\s?[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}(?=[.|,|;|:|\s|!|?]|$)"""
CARD_OTHER_NR_REGEX = r"""(?:^|(?<=[.|,|;|:|\s|!|?]))[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}\s?[0-9]{4}(?=[.|,|;|:|\s|!|?]|$)"""
CARD_ENT = "Kaardinr"

ID_DOC_NR_REGEX = r"""(?:^|(?<=[.|,|;|:|\s|!|?]))(AA|AB|AC|EA|EB|EC|N|NA|N|UA|PB|PC|BD|BE|FB|FC|FD|FE|KD|KE|KF|VD|VE|VF|MD|ME|MF|SD|SE|SF|RD|RE|RF|CD|CF)[0-9]{7}(?=[.|,|;|:|\s|!|?]|$)"""
ID_DOC_NR_ENT = "Isikudokumendinr"

DOC_NR_REGEX = r"""(?:^|(?<=[.|,|;|:|\s|!|?]))[A-Za-z-_]{2,}\s?[0-9]{3,}(?=[.|,|;|:|\s|!|?]|$)"""
DOC_NR_ENT = "Dokumendinr"
def find_match(text, regex, ent):
    dic = {}
    for match in re.finditer(regex, text):
        start, end = match.span()
        found = text[start:end]
        dic[start] = (ent, end, found)
    return dic


NUMERIC_REGEX = r"(?:^|(?<=[.|,|;|:|\s|!|?|\W]))([a-zA-Z]{2}(\s?-\s?)?)?[0-9]{5,}(?=[.|,|;|:|\s|!|?]|$)"
NUMERIC_ENT = 'Muu'

PI_REGEX = r"(?:^|(?<=[.|,|;|:|\s|!|?]))[1-9][0-9]{4}(?=[.|,|;|:|\s|!|?]|$)"
PI_ENT = 'Muu'

OTHER_REGEX = r"""(?:^|(?<=[.|,|;|:|\s|!|?]))([A-Za-z]{2})?[0-9]{6,}(?=[.|,|;|:|\s|!|?]|$)"""
OTHER_ENT = 'Muu'

EMAIL_REGEX = r"""(?:[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")\s?@\s?(?:(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[A-Za-z0-9-]*[A-Za-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])"""
EMAIL_ENT = 'Email'


def find_match_split(text, regex, ent):
    dic = {}
    for match in re.finditer(regex, text):
        start, end = match.span()
        found = text[start:end]
        if len(found.split()) > 1:

            for part in found.split():
                dic[start] = (ent, start + len(part), part)
                start += len(part) + 1
        else:
            dic[start] = (ent, end, found)
    return dic


def get_expression_company(companies):
    string = '(?:^|(?<=[.|,|;|:|\s|!|?]))('
    for s in companies:
        string += str(s) + '|'
    string = string[:-1]
    string += ')(?=[.|,|;|:|\s|!|?]|$)'
    return string


def find_companies(lemma_text, text, confs):
    dic = {}
    lemma_to_form = defaultdict()
    for lemma, word, conf_dic in zip(lemma_text.split(), text.split(), confs):
        lemma_to_form[lemma] = (word, conf_dic)
    for match in re.finditer(get_expression_company(read_companies()), lemma_text):
        start, end = match.span()
        found = lemma_text[start:end]
        if len(found.split()) > 1:
            bi = 'B'
            for part in found.split():
                temp = lemma_to_form.get(part)
                if temp is None:
                    conf_dic = {}
                else:
                    part, conf_dic = temp[0], temp[1][1]
                if 'B-Asutus' in conf_dic.keys() or 'I-Asutus' in conf_dic.keys():
                    if part is not None:
                        start = text.index(part)
                        dic[start] = (bi + '-Asutus', start + len(part), part)
                        start += len(part) + 1
                        bi = 'I'
        else:
            temp = lemma_to_form.get(found)
            if temp is None:
                conf_dic = {}
            else:
                part, conf_dic = temp[0], temp[1][1]
            if found is not None:
                if 'B-Asutus' in conf_dic.keys() or 'I-Asutus' in conf_dic.keys():
                    start = text.index(found)
                    end = start + len(found)
                    dic[start] = ('B-Asutus', end, found)
    return dic


def get_expression_streets(streets):
    string = '(?:^|(?<=[.|,|;|:|\s|!|?]))('
    for s in streets:
        string += s + '|'
    string = string[:-1]
    string += ')((\s*(tänav|tee|rada|põik|maantee|tn|mnt|pst|puiestee)\s*[1-9]([0-9]{1,2}[a-z]?)?(\s*-\s*[0-9]{1,3})?)|(\s(tänav|tee|põik|maantee|tn|mnt|pst|puiestee|rada))|(\s[1-9]([0-9]{1,2}[a-z]?)?(\s*-\s*[0-9]{1,3})?))(?=[.|,|;|:|\s|!|?]|$)'
    return string


def find_ad(text, confs):
    dic = {}
    form_to_dic = {}
    for word, conf_dic in zip(text.split(), confs):
        form_to_dic[word] = conf_dic
    for match in re.finditer(get_expression_streets(read_streets()), text):
        start, end = match.span()
        found = text[start:end]

        if len(found.split()) > 1:
            bi = 'B'
            for part in found.split():
                conf_dic = form_to_dic.get(found)
                if conf_dic is None:
                    conf_dic = {}
                else:
                    conf_dic = conf_dic[1]

                if 'B-Aadress' in conf_dic.keys() or 'I-Aadress' in conf_dic.keys():
                    dic[start] = (bi + '-Aadress', start + len(part), part)
                    start += len(part) + 1
                    bi = 'I'
        else:
            conf_dic = form_to_dic.get(found)[1]
            if conf_dic is None:
                conf_dic = {}
            if 'B-Aadress' in conf_dic.keys() or 'I-Aadress' in conf_dic.keys():
                dic[start] = ('B-Aadress', end, found)
    return dic


def find_regex_entities(text, text_lemmatized, confs):
    regex_entities = {}
    regex_entities.update(find_match(text, DOC_NR_REGEX, DOC_NR_ENT))
    regex_entities.update(find_match_split(text, NUMERIC_REGEX, NUMERIC_ENT))
    regex_entities.update(find_match_split(text, OTHER_REGEX, OTHER_ENT))
    regex_entities.update(find_match_split(text, PI_REGEX, PI_ENT))
    regex_entities.update(find_nr(text))
    regex_entities.update(find_companies(text_lemmatized, text, confs))
    regex_entities.update(find_match(text, CARD_MAESTRO_NR_REGEX, CARD_ENT))
    regex_entities.update(find_match(text, CARD_OTHER_NR_REGEX, CARD_ENT))
    regex_entities.update(find_match(text, ID_REGEX, ID_ENT))
    regex_entities.update(find_match(text, BN_REGEX, BN_ENT))
    regex_entities.update(find_match_split(text, EMAIL_REGEX, EMAIL_ENT))
    regex_entities.update(find_match(text, CAR_NR_REGEX, CAR_NR_ENT))
    regex_entities.update(find_ad(text, confs))
    return regex_entities


def find_url(text):
    dic = {}
    i = 0
    expression = r"(http|ftp|https):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])"
    new_text = text
    for match in re.finditer(expression, text):
        start, end = match.span()
        found = text[start:end]
        new_text = new_text.replace(found, 'url_' + str(i))
        dic['url_' + str(i)] = found
        i += 1
    return dic, new_text


def connect_tags(ner_tagged, disabled_entities, regex_entities, url_dic):
    word_start = 0
    new_text = []
    important_regex = False
    for word, tag in ner_tagged:
        if word_start in regex_entities.keys():
            tag_temp, word_end, token = regex_entities.get(word_start)
            if tag_temp in ['Email', 'Telefoninr', 'Autonumber']:
                important_regex = True

        if 'Nimi' in tag and not important_regex:  # name cannot start with number
            if not word[0].isdigit():  # and word_start not in regex_entities.keys():
                if tag not in disabled_entities:
                    new_text.append('[' + tag + ']')
                    word_start += len(word) + 1
                    continue
                else:
                    new_text.append(word)
                    word_start += len(word) + 1
                    continue

        elif tag != 'O' and not important_regex:
            if tag not in disabled_entities:
                new_text.append('[' + tag + ']')
                word_start += len(word) + 1
                continue
            else:
                new_text.append(word)
                word_start += len(word) + 1
                continue
        elif word.lower() in url_dic.keys():
            word = url_dic.get(word.lower())
            new_text.append(word)
            word_start += len(word) + 1
            continue

        word_end_true = word_start + len(word)

        if word_start in regex_entities.keys():
            tag_temp, word_end, token = regex_entities.get(word_start)
            if word_end == word_end_true and token == word:
                if tag_temp not in disabled_entities:
                    new_text.append('[' + tag_temp + ']')
                else:
                    new_text.append(word)
                word_start += len(word) + 1

            else:
                added = False
                for key, vals in regex_entities.items():  # in case the tokenization is incorrect
                    temp_tag, temp_end, temp_token = vals
                    if added:
                        break
                    if key >= word_start and temp_end <= word_end_true:
                        added = True
                        temp_token = temp_token.replace('+', '\+').replace('?', '\?').replace('*', '\*')
                        splitted = re.split(rf"(?={temp_token})|(?<={temp_token})", word)
                        for split in splitted:
                            if split != '':
                                if split == temp_token:

                                    tag_from_dict = regex_entities.get(key)[0]
                                    if tag_from_dict not in disabled_entities:
                                        new_text.append('[' + regex_entities.get(key)[0] + ']')
                                    else:
                                        new_text.append(split)
                                    word_start += len(split)
                                else:
                                    if word_start in regex_entities.keys():
                                        tag_from_dict = regex_entities.get(word_start)[0]
                                        if tag_from_dict not in disabled_entities:
                                            new_text.append('[' + regex_entities.get(word_start)[0] + ']')
                                        else:
                                            new_text.append(split)
                                        word_start += len(split)
                                    else:
                                        new_text.append(split)
                                        word_start += len(split)
                        word_start += 1

                if not added:
                    new_text.append(word)
                    word_start += len(word) + 1

        else:
            new_text.append(word)
            word_start += len(word) + 1

    return new_text
