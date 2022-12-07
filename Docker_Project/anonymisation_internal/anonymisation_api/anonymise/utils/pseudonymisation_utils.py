import random
from copy import deepcopy
import exrex
import random
import time
import re
from utils import read_file, read_streets, read_names, read_companies
from estnltk import Text
from estnltk.taggers import WhiteSpaceTokensTagger, VabamorfTagger
from estnltk.vabamorf.morf import synthesize
from collections import defaultdict
from flask import Flask
import logging

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

"""
OLEMID: 
Nimi + 
GPE - riigid, linnad 
Aadress + 
Asutus +
Toode - 
Sündmus - ?
Kuupäev - muuda numbrid ära, kuud ära
Aeg - muuda numbrid ära 
Tiitel  - ? 
Raha  - muuda numbrid ära 
Protsent - muuda numbrid ära 
Dokumendinr - regexiga
Kaardinr  - regexiga
IBAN  - regexiga
Isikudocumendinr - regexiga
Isikukood +
Email  +
Telefon  +
Parool +
Autonumber + 
"""

COUNTRIES = read_file('../gazetteers/countries.txt')
COUNTIES = read_file('../gazetteers/counties.txt')
MUNICIPALITIES = read_file('../gazetteers/municipalities.txt')
TOWN_PARTS = read_file('../gazetteers/town_parts.txt')
TOWNS = read_file('../gazetteers/towns.txt')
BOROUGHS = read_file('../gazetteers/borough.txt')
STREETS = read_streets()
VILLAGES = read_file('../gazetteers/villages.txt')

NAMES = read_names('../gazetteers/names.txt')
LASTNAMES = read_names('../gazetteers/lastnames.txt')
COMPANIES = read_companies()
EVENTS = read_file('../gazetteers/events.txt')
TITLES = read_file('../gazetteers/titles.txt')
PRODUCTS = read_file('../gazetteers/products.txt')


def generate_address(entity):
    entity = ' ' + entity + ' '
    uncovered_words = ' ' + deepcopy(entity) + ' '
    already_covered = set()

    text = Text(entity)
    text.tag_layer('addresses')
    if len(text.addresses) != 0:
        street = text.addresses['TÄNAV'][0][0]
        house = text.addresses['MAJA'][0][0]
        town = text.addresses['ASULA'][0][0]
        borough = text.addresses['MAAKOND'][0][0]
        if street != '':
            new_street = random.choice(random.choice(list(STREETS.values()))).capitalize()
            uncovered_words = uncovered_words.replace(street, new_street)
            entity = entity.replace(street, new_street)
            already_covered.add(new_street)
        if house != '':
            new_house = re.sub(r'[1-9]', r'[0-9]', house)
            uncovered_words = uncovered_words.replace(house, new_house)
            entity = entity.replace(house, new_house)
        if town != '':
            new_town = random.choice(TOWNS).capitalize()
            uncovered_words = uncovered_words.replace(town, new_town)
            entity = entity.replace(town, new_town)
            already_covered.add(new_town)
        if borough != '':
            new_borough = random.choice(BOROUGHS).capitalize()
            uncovered_words = uncovered_words.replace(borough, new_borough)
            entity = entity.replace(borough, new_borough)
            already_covered.add(new_borough)
    random_county = None

    for ent in COUNTRIES:
        if ' ' + ent.lower() + ' ' in entity.lower() and ent not in already_covered:
            detected_ent = ent
            already_covered.add(detected_ent)
            random_ent = random.choice(COUNTRIES).capitalize()
            already_covered.add(random_ent)
            entity = entity.replace(detected_ent, random_ent).strip()
            uncovered_words = uncovered_words.replace(entity, '')
            uncovered_words = uncovered_words.replace(' riik ', '')
            uncovered_words = uncovered_words.replace(' riigis ', '')

            break
    for county in COUNTIES:
        if ' ' + county + ' ' in entity and county not in already_covered:
            detected_county = county
            already_covered.add(detected_county)
            random_county = random.choice(COUNTIES).capitalize()
            already_covered.add(random_county)
            entity = entity.replace(detected_county, random_county).strip()

            uncovered_words = uncovered_words.replace(detected_county, '')
            uncovered_words = uncovered_words.replace(' maakonnas ', '')
            uncovered_words = uncovered_words.replace(' maakond ', '')

            break
    for ent in MUNICIPALITIES:
        if ' ' + ent + ' ' in entity and ent not in already_covered:
            detected_ent = ent
            already_covered.add(detected_ent)
            random_ent = random.choice(MUNICIPALITIES).capitalize()
            already_covered.add(random_ent)
            entity = entity.replace(detected_ent, random_ent).strip()
            uncovered_words = uncovered_words.replace(detected_ent, '')
            uncovered_words = uncovered_words.replace(' vald ', '')
            uncovered_words = uncovered_words.replace(' vallas ', '')

            break
    for ent in TOWN_PARTS:
        if ' ' + ent + ' ' in entity and ent not in already_covered:
            detected_ent = ent
            already_covered.add(detected_ent)
            random_ent = random.choice(TOWN_PARTS).capitalize()
            already_covered.add(random_ent)
            entity = entity.replace(detected_ent, random_ent).strip()
            uncovered_words = uncovered_words.replace(detected_ent, '')
            uncovered_words = uncovered_words.replace(' linnaosa ', '')
            uncovered_words = uncovered_words.replace(' linnaosas ', '')

            break
    for ent in BOROUGHS:
        if ' ' + ent + ' ' in entity and ent not in already_covered:
            detected_ent = ent
            already_covered.add(detected_ent)
            random_ent = random.choice(BOROUGHS).capitalize()
            already_covered.add(random_ent)
            entity = entity.replace(detected_ent, random_ent).strip()
            uncovered_words = uncovered_words.replace(detected_ent, '')
            uncovered_words = uncovered_words.replace(' asulas ', '')
            uncovered_words = uncovered_words.replace(' asula ', '')

            break
    detected_city = None
    random_city = None
    for city in TOWNS:
        if ' ' + city + ' ' in entity and city != random_county and city not in already_covered:
            detected_city = city
            random_city = random.choice(TOWNS).capitalize()
            entity = entity.replace(detected_city, random_city).strip()
            already_covered.add(random_city)
            already_covered.add(detected_city)

            uncovered_words = uncovered_words.replace(detected_city, '')

            break
    if detected_city is not None:

        if ' põik ' in entity:
            detected_city = detected_city + '_põik'
        elif ' tänav ' in entity:
            detected_city = detected_city + '_tänav'
        elif ' tee ' in entity:
            detected_city = detected_city + '_tee'
        elif ' maantee ' in entity:
            detected_city = detected_city + '_maantee'
        if len(STREETS[detected_city]) == 0:
            detected_city = detected_city.split('_')[0]
        for street in STREETS[detected_city]:

            if (' ' + street + ' ' in entity and street != random_city and street not in already_covered):
                detected_street = street
                random_street = random.choice(
                    random.choice(list(STREETS.values()))).strip().capitalize()
                entity = entity.replace(detected_street, random_street)
                already_covered.add(detected_street)
                already_covered.add(random_street)

                uncovered_words = uncovered_words.replace(detected_street, '')
                uncovered_words = uncovered_words.replace('tänaval', '')
                uncovered_words = uncovered_words.replace('tänav', '')
                uncovered_words = uncovered_words.replace('maanteel', '')
                uncovered_words = uncovered_words.replace('maantee', '')
                uncovered_words = uncovered_words.replace(' mnt ', ' ')
                uncovered_words = uncovered_words.replace('põik', '')
                uncovered_words = uncovered_words.replace('puiesteel', '')
                uncovered_words = uncovered_words.replace('puiestee', '')
                uncovered_words = uncovered_words.replace(' tee ', '')

                break
    else:
        for street_list in STREETS.values():
            for street in street_list:
                if (
                        ' ' + street + ' ' in entity and street != random_city and street != random_county and street not in already_covered):
                    detected_street = street
                    already_covered.add(detected_street)
                    random_street = random.choice(
                        random.choice(list(STREETS.values()))).capitalize()
                    already_covered.add(random_street)
                    uncovered_words = uncovered_words.replace(detected_street, '')
                    entity = entity.replace(detected_street, random_street)
                    uncovered_words = uncovered_words.replace('tänaval', '')
                    uncovered_words = uncovered_words.replace('tänav', '')
                    uncovered_words = uncovered_words.replace('maanteel', '')
                    uncovered_words = uncovered_words.replace('maantee', '')
                    uncovered_words = uncovered_words.replace(' mnt ', '')
                    uncovered_words = uncovered_words.replace('põik', '')
                    uncovered_words = uncovered_words.replace('puiesteel', '')
                    uncovered_words = uncovered_words.replace('puiestee', '')
                    uncovered_words = uncovered_words.replace(' tee', '')

                    break

    for village in VILLAGES:
        if ' ' + village + ' ' in entity and village not in already_covered:
            detected_village = village
            already_covered.add(detected_village)
            random_village = random.choice(VILLAGES).capitalize()
            entity = entity.replace(detected_village, random_village)
            already_covered.add(random_village)

            uncovered_words = uncovered_words.replace(detected_village, '')
            uncovered_words = uncovered_words.replace('külas', '')
            uncovered_words = uncovered_words.replace('küla', '')

            break

    length = len(re.sub("[^0-9]", "", entity))
    uncovered_words = re.sub(r'[0-9]', '', uncovered_words)
    uncovered_words = re.sub(r'[.,:!?\'\"]', '', uncovered_words)
    pattern = r'[0-9]'
    new_ent = deepcopy(entity)
    entity1 = ""
    for i in range(length):

        random_number = str(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        new_ent = re.sub(pattern, random_number, new_ent, 1)
        if i == 0:
            entity1 = new_ent[:new_ent.index(random_number) + 1]
            new_ent = new_ent[new_ent.index(random_number) + 1:]
        else:
            if new_ent.index(random_number) != 0:
                entity1 = entity1 + new_ent[: new_ent.index(random_number)]
            part = new_ent[new_ent.index(random_number):new_ent.index(random_number) + 1]
            new_ent = new_ent[new_ent.index(random_number) + 1:]
            entity1 = entity1 + part

    if entity1 != "":
        entity = entity1
    if uncovered_words.strip() != "":
        splitted = uncovered_words.split()
        for split in splitted:
            if ' ' + split + ' ' in entity:
                entity = entity.replace(split, '')

    entity = ' '.join(entity.split())
    if entity.strip() == '' or entity is None:
        entity = random.choice(TOWNS)
    return entity.strip()


TEL_REG = r"""5[0-9]{7}"""
CAR_NR_REG = r"""[0-9]{3}[A-Z]{3}"""
PW_REG = r"""[a-zA-Z]{4,8}[0-9]{1,2}[!\.,\)\(/&%¤?+]{1,2}"""
IBAN_REG = r"""EE9099[0-9]{14}"""
CARD_NR_REG = r"""(5018|5020|5038|5612|5893|6304|6759|6761|6762|6763|0604|6390|6759)[0-9]{4}[0-9]{4}[0-9]{4}"""
DOC_NR_REG = r"""(AA|AB|AC|EA|EB|EC|N|NA|N|UA|PB|PC|BD|BE|FB|FC|FD|FE|KD|KE|KF|VD|VE|VF|MD|ME|MF|SD|SE|SF|RD|RE|RF|CD|CF)[0-9]{7}"""
DOC_NR_O_REG = r"""[A-Z]{2}[0-9]{3,7}"""

regex_dictionary = {'[Telefoninr]': TEL_REG, '[Autonumber]': CAR_NR_REG, '[Parool]': PW_REG, '[IBAN]': IBAN_REG,
                    '[Kaardinr]': CARD_NR_REG, '[Isikudokumendinr]': DOC_NR_REG, '[Dokumendinr]': DOC_NR_O_REG}


def generate(ent):
    if 'Email' in ent:
        email_regex_1 = r"""\.{0,1}"""
        ending_selection = ['gmail.com', 'gmail.com', 'gmail.com', 'gmail.com', 'gmail.com',
                            'gmail.com', 'gmail.com', 'mail.ee', 'hotmail.com', 'hot.ee']
        new_ent = ''.join([random.choice(NAMES).lower(),
                           exrex.getone(email_regex_1),
                           random.choice(LASTNAMES).lower(),
                           '@',
                           random.choice(ending_selection)
                           ])
    elif 'Isikukood' in ent:
        id_reg_34 = r"""[3-4][4-9][0-9](01|02|03|04|05|06|07|08|09|10|11|12)"""
        id_reg_56 = r"""[5-6][0-1][0-9](01|02|03|04|05|06|07|08|09|10|11|12)"""

        id_reg_cent = random.choice([exrex.getone(id_reg_34), exrex.getone(id_reg_56)])
        if id_reg_cent[-2:] == '02':
            id_reg_date = r"""(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28)[0-9]{3}[0-9]"""
        elif id_reg_cent[-2:] in ['01', '03', '05', '07', '08', '10', '12']:
            id_reg_date = r"""(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30|31)[0-9]{3}[0-9]"""
        else:
            id_reg_date = r"""(01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24|25|26|27|28|29|30)[0-9]{3}[0-9]"""

        new_ent = id_reg_cent + exrex.getone(id_reg_date)
    elif 'Muu' in ent:
        new_ent = '[eemaldatud]'
    else:
        new_ent = exrex.getone(regex_dictionary.get(ent))
    return new_ent


def str_time_prop(start, end, time_format, prop):
    stime = time.mktime(time.strptime(start, time_format))
    etime = time.mktime(time.strptime(end, time_format))
    ptime = stime + prop * (etime - stime)

    return time.strftime(time_format, time.localtime(ptime))


def random_date(entity):
    length = len(re.sub("[^0-9]", "", entity))
    if length == 0:
        if length == 0:
            return random.choice(["õhtu","päev", "jaanuar", "veebruar", "märts", "aprill", "juuni", "juuli", "august","september", "oktoober", "november", "detsember", "õhtu", "eile", "täna", "üleeile"])

    return str_time_prop("1/1/2000 1:00 AM", "12/12/2022 1:00 AM", '%m/%d/%Y %I:%M %p', random.random())


def generate_number(entity):
    length = len(re.sub("[^0-9]", "", entity))
    pattern = r'[0-9]'
    new_ent = deepcopy(entity)
    entity1 = ""
    for i in range(length):

        random_number = str(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9]))
        new_ent = re.sub(pattern, random_number, new_ent, 1)
        if i == 0:
            entity1 = new_ent[:new_ent.index(random_number) + 1]
            new_ent = new_ent[new_ent.index(random_number) + 1:]
        else:
            if new_ent.index(random_number) != 0:
                entity1 = entity1 + new_ent[: new_ent.index(random_number)]
            part = new_ent[new_ent.index(random_number):new_ent.index(random_number) + 1]
            new_ent = new_ent[new_ent.index(random_number) + 1:]
            entity1 = entity1 + part

    entity1 = entity1 + new_ent

    return entity1


def pseudonymization(text, entities):
    tokenizer = WhiteSpaceTokensTagger()
    vabamorf_tagger = VabamorfTagger(input_words_layer='tokens')
    t = Text(text)
    tokenizer.tag(t)
    t.tag_layer('paragraphs')
    vabamorf_tagger.tag(t)
    new_text = []
    previous = 'O'
    entity_mapping = {}
    counts = defaultdict(lambda: 1)

    i = 0
    tagged_text = []
    mappings = []
    previous_name = ""
    for span, ent in zip(t.morph_analysis, entities):
        form = span.form[0]
        span_lemma = span.lemma[0]
        span_form = span.text
        pos = span.partofspeech[0]
        new_ent = ""
        if ent in ('[Telefoninr]', '[Autonumber]', '[IBAN]', '[Email]', '[Parool]', '[Isikukood]', '[Kaardinr]',
                   '[Isikudokumendinr]', '[Muu]', '[Dokumendinr]'):
            if previous != ent:
                ent_formatted = ent[1:-1]
                if counts.get(ent_formatted) is None:
                    counts[ent_formatted] = 1
                if form in entity_mapping.keys():
                    new_ent = entity_mapping.get(form)
                    count = counts.get(form)

                else:
                    new_ent = generate(ent)
                    entity_mapping[form] = new_ent
                    count = counts.get(ent_formatted)
                    counts[ent_formatted] += 1
                    counts[form] = count
                tagged_text.append(ent_formatted + '_' + str(count))
                mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                                 'Tag': ent_formatted + '_' + str(count)})


        elif 'Nimi' in ent:
            if span_lemma in entity_mapping.keys():
                random_name = entity_mapping[span_lemma]
            elif span_form in entity_mapping.keys():
                random_name = entity_mapping.get(span_form)
            elif 'Nimi' in previous and ent == '[I-Nimi]':
                if i + 1 < len(entities):  # check if we are trying to access out of list element
                    if entities[i + 1] == '[I-Nimi]':
                        random_name = random.choice(NAMES)
                    else:
                        random_name = random.choice(LASTNAMES)
                else:
                    random_name = random.choice(LASTNAMES)

                entity_mapping[span_lemma] = random_name
                entity_mapping[span_form] = random_name

            else:  # ent == B-Nimi
                random_name = random.choice(NAMES)
                entity_mapping[span_lemma[0]] = random_name
                entity_mapping[span_lemma[0] + '.'] = random_name
                entity_mapping[span_lemma] = random_name
                entity_mapping[span_form] = random_name

            new_ent = synthesize(random_name, form, partofspeech=pos)
            new_ent = random_name.capitalize() if new_ent == [] else new_ent[0].capitalize()
            if counts.get('Nimi') is None:
                counts['Nimi'] = 1
            count = str(counts.get('Nimi'))
            if random_name in counts.keys():
                count = str(counts.get(random_name))
            elif ent == '[I-Nimi]':
                count = str(counts.get(previous_name))
            else:
                counts['Nimi'] += 1
            mappings.append({'Algne': span.text,
                             'Asendatud': new_ent.capitalize(),
                             'Tag': 'Nimi_' + count})
            if random_name not in counts.keys():
                counts[random_name] = int(count)

            tagged_text.append('Nimi_' + count)
            previous_name = random_name

        elif 'Asutus' in ent:
            if ent == '[I-Asutus]':
                new_ent = ''
            else:
                last_span = span
                count, j = 1, 1
                collected_words = [span.lemma[0]]
                collected_forms = [span.text]
                while True:
                    if i + j >= len(entities):
                        break
                    next_ent = entities[i + j]
                    if next_ent == '[I-Asutus]':
                        last_span = t.morph_analysis[i + j]
                        collected_words.append(last_span.lemma[0])
                        collected_forms.append(last_span.text)
                        count += 1
                        j += 1
                    else:
                        break
                form = last_span.form[0]
                pos = last_span.partofspeech[0]
                collected_words_word = ' '.join(collected_words)
                if collected_words_word in entity_mapping.keys():
                    random_company = entity_mapping.get(collected_words_word)
                elif len(COMPANIES.get(count)) != 0:
                    random_company = random.choice(COMPANIES.get(count))
                else:
                    random_company = random.choice(COMPANIES.get(2))

                entity_mapping[collected_words_word] = random_company
                splitted = random_company.split(' ')
                beginning_words = ' '.join(splitted[:-1])
                new_ent = synthesize(splitted[-1], form, partofspeech=pos)
                if not new_ent:
                    new_ent = random_company.strip()
                else:
                    if beginning_words is not None:
                        new_ent = beginning_words + ' ' + new_ent[0].strip()
                    else:
                        new_ent = new_ent[0].strip()
                new_ent = new_ent.capitalize()
                if counts.get('Asutus') is None:
                    counts['Asutus'] = 1
                count = str(counts.get(random_company)) if random_company in counts.keys() else str(
                    counts.get('Asutus'))
                mappings.append({'Algne': ' '.join(collected_forms), 'Asendatud': new_ent.capitalize(),
                                 'Tag': 'Asutus_' + count})
                tagged_text.append('Asutus_' + count)
                if random_company not in counts.keys():
                    counts[random_company] = int(count)
                    counts['Asutus'] += 1


        elif 'Aadress' in ent:

            if ent != '[B-Aadress]':
                new_ent = ''
            else:
                last_span = span
                j = 1
                collected_words = [span.text]
                collected_lemmas = [span.lemma[0]]
                while True:
                    if i + j >= len(entities):
                        break
                    next_ent = entities[i + j]
                    if next_ent == '[I-Aadress]':
                        last_span = t.morph_analysis[i + j]
                        collected_words.append(last_span.text)
                        collected_lemmas.append(last_span.lemma[0])
                        j += 1
                    else:
                        break

                form = last_span.form[0]
                pos = last_span.partofspeech[0]
                if ' '.join(collected_words) in entity_mapping.keys():
                    random_address = entity_mapping.get(' '.join(collected_words))
                else:
                    random_address = generate_address(' '.join(collected_words)).strip()

                entity_mapping[' '.join(collected_words)] = random_address
                splitted = random_address.split(' ')
                word = splitted[-1] if len(splitted) > 1 else random_address
                new_ent = synthesize(word, form, partofspeech=pos)

                if not new_ent:
                    new_ent = random_address.capitalize()
                else:
                    new_ent = ' '.join(splitted[:-1]).capitalize() + ' ' + new_ent[0] if len(splitted) > 1 else new_ent[
                        0].capitalize()
                if counts.get('Aadress') is None:
                    counts['Aadress'] = 1
                count = str(counts.get(random_address)) if random_address in counts.keys() else str(
                    counts.get('Aadress'))
                mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent.capitalize(),
                                 'Tag': 'Aadress_' + count})
                tagged_text.append('Aadress_' + count)
                if random_address not in counts.keys():
                    counts[random_address] = int(count)
                    counts['Aadress'] += 1




        elif 'Sündmus' in ent:
            if ent != '[B-Sündmus]':
                new_ent = ''
            else:
                last_span = span
                j = 1
                collected_words = [span.text]
                while True:
                    if i + j >= len(entities):
                        break
                    next_ent = entities[i + j]
                    if next_ent == '[I-Sündmus]':
                        last_span = t.morph_analysis[i + j]
                        collected_words.append(last_span.text)
                        j += 1
                    else:
                        break

                form = last_span.form[0]
                pos = last_span.partofspeech[0]

                if ' '.join(collected_words) in entity_mapping.keys():
                    random_event = entity_mapping.get(' '.join(collected_words))
                else:
                    random_event = random.choice(EVENTS)

                entity_mapping[' '.join(collected_words)] = random_event
                splitted = random_event.split(' ')
                word = splitted[-1] if len(splitted) > 1 else random_event
                new_ent = synthesize(word, form, partofspeech=pos)

                if not new_ent:
                    new_ent = random_event.capitalize()
                else:
                    new_ent = ' '.join(splitted[:-1]).capitalize() + ' ' + new_ent[0] if len(splitted) > 1 else new_ent[
                        0].capitalize()
                if counts.get('Sündmus') is None:
                    counts['Sündmus'] = 1
                count = str(counts.get(random_event)) if random_event in counts.keys() else str(counts.get('Sündmus'))
                mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent,
                                 'Tag': 'Sündmus_' + count})
                tagged_text.append('Sündmus_' + count)

                if random_event not in counts.keys():
                    counts[random_event] = counts.get('Sündmus')
                    counts['Sündmus'] += 1

        elif 'GPE' in ent:
            if ent != '[B-GPE]':
                new_ent = ''
            else:
                last_span = span
                j = 1
                collected_words = [span.text]
                collected_lemmas = [span.lemma[0]]
                while True:
                    if i + j >= len(entities):
                        break
                    next_ent = entities[i + j]
                    if next_ent == '[I-GPE]':
                        last_span = t.morph_analysis[i + j]
                        collected_words.append(last_span.text)
                        collected_lemmas.append(last_span.lemma[0])
                        j += 1
                    else:
                        break

                form = last_span.form[0]
                pos = last_span.partofspeech[0]

                if ' '.join(collected_lemmas) in entity_mapping.keys():
                    random_gpe = entity_mapping.get(' '.join(collected_lemmas))
                else:
                    random_gpe = generate_address(' '.join(collected_lemmas)).strip()

                entity_mapping[' '.join(collected_lemmas)] = random_gpe
                splitted = random_gpe.split(' ')
                word = splitted[-1] if len(splitted) > 1 else random_gpe
                new_ent = synthesize(word, form, partofspeech=pos)

                if not new_ent:
                    new_ent = random_gpe.capitalize()
                else:
                    new_ent = ' '.join(splitted[:-1]).capitalize() + ' ' + new_ent[0] if len(splitted) > 1 else new_ent[
                        0].capitalize()
                if counts.get('GPE') is None:
                    counts['GPE'] = 1
                count = str(counts.get(random_gpe)) if random_gpe in counts.keys() else str(counts.get('GPE'))
                mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent.capitalize(),
                                 'Tag': 'GPE_' + count})
                tagged_text.append('GPE_' + count)
                if random_gpe not in counts.keys():
                    counts[random_gpe] = int(count)
                    counts['GPE'] += 1


        elif 'Protsent' in ent or 'Aeg' in ent or 'Raha' in ent or 'Kuupäev' in ent:
            if ent.startswith('[I-'):
                new_ent = ''
            else:
                cleaned_entity = ent.replace('[B-', '').replace(']', '')
                j = 1
                collected_words = [span.text]
                last_span = t.morph_analysis[i]
                while True:
                    if i + j >= len(entities):
                        break
                    next_ent = entities[i + j]
                    if next_ent == ent.replace('B-', 'I-'):
                        last_span = t.morph_analysis[i + j]
                        collected_words.append(last_span.text)
                        j += 1
                    else:
                        break
                if 'Kuupäev' in ent:
                    new_ent = random_date(' '.join(collected_words)).split(" ")[0].replace('/', '.')
                    if len(re.sub("[^0-9]", "", ' '.join(collected_words))) == 0:
                        form = last_span.form[0]
                        temp = synthesize(new_ent, form, partofspeech=pos)
                        if temp:
                            new_ent = temp[0]


                elif 'Aeg' in ent:
                    plus = random.choice([0, 12])
                    new_ent = random_date(' '.join(collected_words))
                    length = len(re.sub("[^0-9]", "", ' '.join(collected_words)))
                    if length != 0:
                        new_ent = new_ent.split(" ")[1].split(':')
                        new_ent = str(int(new_ent[0]) + plus) + ':' + new_ent[1]
                    else:
                        form = last_span.form[0]
                        temp = synthesize(new_ent, form, partofspeech=pos)
                        if  temp:
                            new_ent = temp[0]
                else:
                    new_ent = generate_number(' '.join(collected_words))
                if counts.get(cleaned_entity) is None:
                    counts[cleaned_entity] = 1
                count = str(counts.get(cleaned_entity))
                mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent,
                                 'Tag': cleaned_entity + '_' + count})
                tagged_text.append(cleaned_entity + '_' + count)

        elif 'Toode' in ent:
            if  ent.startswith('[I-'):
                new_ent = ''
            else:

                j = 1
                collected_words = [span.text]
                while True:
                    if i + j >= len(entities):
                        break
                    next_ent = entities[i + j]
                    if next_ent == ent.replace('B-', 'I-'):
                        last_span = t.morph_analysis[i + j]
                        collected_words.append(last_span.text)
                        j += 1
                    else:
                        break
                if ' '.join(collected_words) in entity_mapping.keys():
                    random_prod = entity_mapping.get(' '.join(collected_words))
                else:
                    random_prod = random.choice(PRODUCTS)
                entity_mapping[' '.join(collected_words)] = random_prod
                splitted = random_prod.split(' ')
                word = splitted[-1] if len(splitted) > 1 else random_prod
                new_ent = synthesize(word, form, partofspeech=pos)

                if not new_ent:
                    new_ent = random_prod.capitalize()
                else:
                    new_ent = ' '.join(splitted[:-1]).capitalize() + ' ' + new_ent[0] if len(splitted) > 1 else new_ent[
                        0].capitalize()
                if counts.get('Toode') is None:
                    counts['Toode'] = 1
                count = str(counts.get(random_prod)) if random_prod in counts.keys() else str(counts.get('Toode'))
                mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent,
                                 'Tag': 'Toode_' + count})
                tagged_text.append('Toode_' + count)
                if random_prod not in counts.keys():
                    counts[random_prod] = int(count)
                    counts['Toode'] += 1



        elif 'Tiitel' in ent:
            if ent != '[B-Tiitel]':
                new_ent = ''
            else:
                last_span = span
                j = 1
                collected_words = [span.text]
                while True:
                    if i + j >= len(entities):
                        break
                    next_ent = entities[i + j]
                    if next_ent == '[I-Tiitel]':
                        last_span = t.morph_analysis[i + j]
                        collected_words.append(last_span.text)
                        j += 1
                    else:
                        break

                form = last_span.form[0]
                pos = last_span.partofspeech[0]

                if ' '.join(collected_words) in entity_mapping.keys():
                    random_title = entity_mapping[' '.join(collected_words)]
                else:
                    random_title = random.choice(TITLES)

                entity_mapping[' '.join(collected_words)] = random_title
                splitted = random_title.split(' ')
                word = splitted[-1] if len(splitted) > 1 else random_title
                new_ent = synthesize(word, form, partofspeech=pos)

                if not new_ent:
                    new_ent = random_title.capitalize()
                else:
                    new_ent = ' '.join(splitted[:-1]).capitalize() + ' ' + new_ent[0] if len(splitted) > 1 else new_ent[
                        0].capitalize()
                if counts.get('Tiitel') is None:
                    counts['Tiitel'] = 1
                count = str(counts.get(random_title)) if random_title in counts.keys() else str(counts.get('Tiitel'))
                mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent,
                                 'Tag': 'Tiitel_' + count})
                tagged_text.append('Tiitel_' + count)
                if random_title not in counts.keys():
                    counts[random_title] = int(count)
                    counts['Tiitel'] += 1




        else:
            new_ent = ent
            mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                             'Tag': 'O'})
            tagged_text.append(span.text)
        if new_ent != '':
            new_text.append(new_ent.strip())
            previous = ent if ent.startswith('[') and ent.endswith(']') else 'O'
        i += 1

    return ' '.join(new_text).capitalize().split(), tagged_text, mappings
