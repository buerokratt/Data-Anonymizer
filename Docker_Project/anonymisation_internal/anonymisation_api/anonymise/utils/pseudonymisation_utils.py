import random
from copy import deepcopy
import exrex
import re
from utils import read_file, read_streets, read_names, read_companies
from estnltk import Text
from estnltk.taggers import WhiteSpaceTokensTagger, VabamorfTagger
from estnltk.vabamorf.morf import synthesize
from collections import defaultdict
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

def generate_address(entity):
    entity = ' ' + entity + ' '
    uncovered_words = ' ' + deepcopy(entity) + ' '
    random_county = None

    already_covered = set()
    for ent in COUNTRIES:
        if ' ' + ent + ' ' in entity:
            detected_ent = ent
            already_covered.add(detected_ent)
            random_ent = random.choice(COUNTRIES).capitalize()
            already_covered.add(random_ent)
            entity = entity.replace(detected_ent, random_ent)
            uncovered_words = uncovered_words.replace(random_ent, '')
            uncovered_words = uncovered_words.replace(' vald ', '')
            uncovered_words = uncovered_words.replace(' vallas ', '')

            break
    for county in COUNTIES:
        if ' ' + county + ' ' in entity and county not in already_covered:
            detected_county = county
            already_covered.add(detected_county)
            random_county = random.choice(COUNTIES).capitalize()
            already_covered.add(random_county)
            entity = entity.replace(detected_county, random_county)

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
            entity = entity.replace(detected_ent, random_ent)
            uncovered_words = uncovered_words.replace(random_ent, '')
            uncovered_words = uncovered_words.replace(' vald ', '')
            uncovered_words = uncovered_words.replace(' vallas ', '')

            break

    for ent in TOWN_PARTS:
        if ' ' + ent + ' ' in entity and ent not in already_covered:
            detected_ent = ent
            already_covered.add(detected_ent)
            random_ent = random.choice(TOWN_PARTS).capitalize()
            already_covered.add(random_ent)
            entity = entity.replace(detected_ent, random_ent)
            uncovered_words = uncovered_words.replace(random_ent, '')
            uncovered_words = uncovered_words.replace(' linnaosa ', '')
            uncovered_words = uncovered_words.replace(' linnaosas ', '')

            break
    for ent in BOROUGHS:
        if ' ' + ent + ' ' in entity and ent not in already_covered:
            detected_ent = ent
            already_covered.add(detected_ent)
            random_ent = random.choice(BOROUGHS).capitalize()
            already_covered.add(random_ent)
            entity = entity.replace(detected_ent, random_ent)
            uncovered_words = uncovered_words.replace(random_ent, '')
            uncovered_words = uncovered_words.replace(' asulas ', '')
            uncovered_words = uncovered_words.replace(' asula ', '')

            break

    detected_city = None
    random_city = None
    for city in TOWNS:
        if ' ' + city + ' ' in entity and city != random_county and city not in already_covered:
            detected_city = city
            random_city = random.choice(TOWNS).capitalize()
            entity = entity.replace(detected_city, random_city)
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
                random_street = random.choice(random.choice(list(STREETS.values()))).replace('tänav',
                                                                                                  '').replace(
                    'põik', '').replace('maantee', '').replace('tee', '').replace('puiestee', 'pst').capitalize()
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
                    random_street = random.choice(random.choice(list(STREETS.values()))).replace(' tänav',
                                                                                                      '').replace(
                        ' põik', '').replace(' maantee', '').replace(' tee', '').replace(' puiestee', '').replace(
                        ' pst ', '').capitalize()
                    already_covered.add(random_street)
                    uncovered_words = uncovered_words.replace(detected_street, '')
                    entity = entity.replace(detected_street, random_street)
                    uncovered_words = uncovered_words.replace('tänaval', '')
                    uncovered_words = uncovered_words.replace('tänav', '')
                    uncovered_words = uncovered_words.replace('maanteel', '')
                    uncovered_words = uncovered_words.replace('maantee', '')
                    uncovered_words = uncovered_words.replace(' mnt ', ' ')
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

    entity = entity.replace('  ', ' ')
    if entity.strip() == '':
        entity = random.choice(TOWNS)
    return entity.strip()

def pseudonymization(text, entities):
    tokenizer = WhiteSpaceTokensTagger()
    vabamorf_tagger = VabamorfTagger(input_words_layer='tokens')
    t = Text(text)

    tokenizer.tag(t)

    all_ents = ["[Telefoninr]", "[Parool]", "[Email]", "[B-Nimi]", "[I-Nimi]", "[B-Asutus]", "[I-Asutus]", "[Muu]",
                "[B-Aadress]", "[I-Aadress]", "[Isikukood]", "[Autonumber]"]
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
        if ent in all_ents:
            if ent == '[Telefoninr]':
                if previous == '[Telefoninr]':
                    new_ent = ''
                else:
                    form = span.form[0]
                    if form in entity_mapping.keys():
                        new_ent = entity_mapping.get(form)
                    else:
                        tel_regex = r"""5[0-9]{7}"""
                        new_ent = exrex.getone(tel_regex)
                        entity_mapping[form] = new_ent
                    if counts.get('Telefoninr') is None:
                        counts['Telefoninr'] = 1
                    tagged_text.append('Telefoninr_' + str(counts.get('Telefoninr')))
                    mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                                     'Tag': 'Telefoninr_' + str(counts.get('Telefoninr'))})
                    counts['Telefoninr'] += 1
            elif ent == '[Autonumber]':
                form = span.form[0]
                if form in entity_mapping.keys():
                    new_ent = entity_mapping.get(form)
                else:
                    car_regex = r"""[0-9]{3}[A-Z]{3}"""
                    new_ent = exrex.getone(car_regex)
                    entity_mapping[form] = new_ent
                if counts.get('Autonumber') is None:
                    counts['Autonumber'] = 1
                mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                                 'Tag': 'Autonumber_' + str(counts.get('Autonumber'))})
                tagged_text.append('Autonumber_' + str(counts.get('Autonumber')))
                counts['Autonumber'] += 1
            elif ent == '[Parool]':
                form = span.form[0]
                if form in entity_mapping.keys():
                    new_ent = entity_mapping.get(form)
                else:
                    par_regex = r"""[a-zA-Z0-9\d]{4,8}"""
                    new_ent = exrex.getone(par_regex)
                    entity_mapping[form] = new_ent
                if counts.get('Parool') is None:
                    counts['Parool'] = 1
                mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                                 'Tag': 'Parool_' + str(counts.get('Parool'))})
                tagged_text.append('Parool_' + str(counts.get('Parool')))
                counts['Parool'] += 1
            elif ent == '[Email]':
                if previous == '[Email]':
                    new_ent = ''
                else:
                    form = span.form[0]
                    if form in entity_mapping.keys():
                        new_ent = entity_mapping.get(form)
                    else:
                        email_regex_1 = r"""\.{0,1}"""
                        ending_selection = ['gmail.com', 'gmail.com', 'gmail.com', 'gmail.com', 'gmail.com',
                                        'gmail.com', 'gmail.com', 'mail.ee', 'hotmail.com', 'hot.ee']
                        new_ent = ''.join([random.choice(NAMES).lower(),
                                       exrex.getone(email_regex_1),
                                       random.choice(LASTNAMES).lower(),
                                       '@',
                                       random.choice(ending_selection)
                                       ])
                        entity_mapping[form] = new_ent
                    if counts.get('Email') is None:
                        counts['Email'] = 1
                    mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                                     'Tag': 'Email_' + str(counts.get('Email'))})
                    tagged_text.append('Email_' + str(counts.get('Email')))
                    counts['Email'] += 1
            elif '-Nimi' in ent:
                if previous == '[B-Nimi]' or previous == '[I-Nimi]':
                    form = span.form[0]
                    name_lemma = span.lemma[0]
                    name_form = span.text
                    if name_lemma in entity_mapping.keys():
                        random_name = entity_mapping[name_lemma]
                    elif name_form in entity_mapping.keys():
                        random_name = entity_mapping[name_form]
                    else:
                        ## TODO should check if is actually the lastname
                        if entities[i+1] == 'I-Nimi':
                            random_name = random.choice(NAMES)
                        else:
                            random_name = random.choice(LASTNAMES)
                        entity_mapping[name_lemma] = random_name
                        entity_mapping[name_form] = random_name
                    pos = span.partofspeech[0]
                    new_ent = synthesize(random_name, form, partofspeech=pos)
                    if counts.get('Nimi') is None:
                        counts['Nimi'] = 1
                    if random_name in counts.keys():
                        if new_ent == []:
                            mappings.append({'Algne': span.text, 'Asendatud': random_name.capitalize(),
                                             'Tag': 'Nimi_' + str(counts.get(random_name))})
                        else:
                            mappings.append({'Algne': span.text, 'Asendatud': new_ent[0],
                                             'Tag': 'Nimi_' + str(counts.get(random_name))})
                        # tagged_text.append('Nimi_' + str(counts.get(random_name)))
                    else:
                        mappings.append({'Algne': span.text,
                                         'Asendatud': new_ent[0] if new_ent != [] else random_name.capitalize(),
                                         'Tag': 'Nimi_' + str(counts.get(previous_name))})
                        # tagged_text.append('Nimi_' + str(counts.get('Nimi')))

                        counts[random_name] = counts.get(previous_name)
                        # counts['Nimi'] += 1
                else:
                    form = span.form[0]
                    name_lemma = span.lemma[0]
                    name_form = span.text
                    if name_lemma in entity_mapping.keys():
                        random_name = entity_mapping[name_lemma]
                    elif name_form in entity_mapping.keys():
                        random_name = entity_mapping[name_form]
                    else:

                        random_name = random.choice(NAMES)
                        if previous != 'B-Nimi' and previous != 'I-Nimi':
                            entity_mapping[name_lemma[0]] = random_name
                            entity_mapping[name_lemma[0] + '.'] = random_name
                        entity_mapping[name_lemma] = random_name
                        entity_mapping[name_form] = random_name
                    pos = span.partofspeech[0]
                    new_ent = synthesize(random_name, form, partofspeech=pos)

                    if random_name in counts.keys():
                        mappings.append({'Algne': span.text,
                                         'Asendatud': new_ent[0] if new_ent != [] else random_name.capitalize(),
                                         'Tag': 'Nimi_' + str(counts.get(random_name))})
                        tagged_text.append('Nimi_' + str(counts.get(random_name)))
                    else:
                        if counts.get('Nimi') is None:
                            counts['Nimi'] = 1
                        if 'B-Nimi' in ent:
                            tagged_text.append('Nimi_' + str(counts.get('Nimi')))

                            mappings.append({'Algne': span.text,
                                             'Asendatud': new_ent[0] if new_ent != [] else random_name.capitalize(),
                                             'Tag': 'Nimi_' + str(counts.get('Nimi'))})
                            counts[random_name] = counts.get('Nimi')
                            counts['Nimi'] += 1
                        else:
                            mappings.append({'Algne': span.text,
                                             'Asendatud': new_ent[0] if new_ent != [] else random_name.capitalize(),
                                             'Tag': 'Nimi_' + str(counts.get(previous_name))})
                            counts[random_name] = counts.get(previous_name)
                            counts[random_name[0]] = counts.get(previous_name)

                if not new_ent:
                    new_ent = random_name.capitalize()
                else:
                    new_ent = new_ent[0].capitalize()
                previous_name = random_name
            elif '-Asutus' in ent:
                if previous == '[B-Asutus]':
                    new_ent = ''

                else:
                    last_span = span
                    j = 1
                    count = 1
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
                        entity_mapping[collected_words_word] = random_company
                    else:
                        random_company = random.choice(COMPANIES.get(2))
                        entity_mapping[collected_words_word] = random_company

                    splitted = random_company.split(' ')
                    beginning_words = None
                    if len(splitted) > 1:
                        beginning_words = ' '.join(splitted[:-1])
                        last_word = splitted[-1]
                        new_ent = synthesize(last_word, form, partofspeech=pos)
                    else:
                        new_ent = synthesize(random_company, form, partofspeech=pos)
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
                    if random_company in counts.keys():
                        mappings.append({'Algne': ' '.join(collected_forms), 'Asendatud': new_ent,
                                         'Tag': 'Asutus_' + str(counts.get(random_company))})
                        tagged_text.append('Asutus_' + str(counts.get(random_company)))
                    else:
                        mappings.append({'Algne': ' '.join(collected_forms), 'Asendatud': new_ent,
                                         'Tag': 'Asutus_' + str(counts.get('Asutus'))})

                        counts[random_company] = counts.get('Asutus')
                        tagged_text.append('Asutus_' + str(counts.get('Asutus')))
                        counts['Asutus'] += 1

            elif ent == '[Muu]':
                new_ent = '[eemaldatud]'
                if counts.get('Muu') is None:
                    counts['Muu'] = 1
                mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                                 'Tag': 'Muu_' + str(counts.get('Muu'))})
                tagged_text.append('Muu_' + str(counts.get('Muu')))
                counts['Muu'] += 1
            elif '-Aadress' in ent:

                if ent != '[B-Aadress]':
                    new_ent = ''
                else:
                    last_span = span
                    j = 1
                    collected_words = [span.text]
                    while True:
                        if i + j >= len(entities):
                            break
                        next_ent = entities[i + j]
                        if next_ent == '[I-Aadress]':
                            last_span = t.morph_analysis[i + j]
                            collected_words.append(last_span.text)

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
                    if len(splitted) > 1:

                        last_word = splitted[-1]
                        new_ent = synthesize(last_word, form, partofspeech=pos)
                    else:
                        new_ent = synthesize(random_address, form, partofspeech=pos)
                    if not new_ent:
                        new_ent = random_address
                    else:
                        if len(splitted) > 1:
                            new_ent = ' '.join(splitted[:-1]) + ' ' + new_ent[0]

                        else:
                            new_ent = new_ent[0]
                    new_ent = new_ent.capitalize()
                    if counts.get('Aadress') is None:
                        counts['Aadress'] = 1
                    if random_address in counts.keys():
                        mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent,
                                         'Tag': 'Aadress_' + str(counts.get(random_address))})
                        tagged_text.append('Aadress_' + str(counts.get(random_address)))
                    else:
                        mappings.append({'Algne': ' '.join(collected_words), 'Asendatud': new_ent,
                                         'Tag': 'Aadress_' + str(counts.get('Aadress'))})

                        counts[random_address] = counts.get('Aadress')
                        tagged_text.append('Aadress_' + str(counts.get('Aadress')))
                        counts['Aadress'] += 1

            elif ent == '[Isikukood]':
                if previous == '[Isikukood]':
                    new_ent = ''
                else:
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
                    if counts.get('Isikukood') is None:
                        counts['Isikukood'] = 1
                    mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                                     'Tag': 'Isikukood_' + str(counts.get('Isikukood'))})
                    tagged_text.append('Isikukood_' + str(counts.get('Isikukood')))
                    counts['Isikukood'] += 1
            new_text.append(new_ent.strip())
            previous = ent
        else:
            new_ent = ent
            new_text.append(ent)
            mappings.append({'Algne': span.text, 'Asendatud': new_ent,
                             'Tag': 'O'})
            tagged_text.append(span.text)
            previous = 'O'
        i += 1
    return new_text, tagged_text, mappings
