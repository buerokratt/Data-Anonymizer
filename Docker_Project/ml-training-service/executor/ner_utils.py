from itertools import combinations
import ast
import logging
import stanza
stanza.download('et')
nlp = stanza.Pipeline('et', processors='tokenize', use_gpu=False)

# TODO: Add data checks for useful error messages
def convert_to_iob(annotations: list, pos_dict: dict) -> None:
    for annot in annotations:
        annot_text = annot['text'].split(' ')
        if len(annot_text) == 1:
            if f"{annot['start']}_{annot['end']}" in pos_dict:
                pos_dict[f"{annot['start']}_{annot['end']}"].update({'ner_1': f"B-{annot['labels'][0]}"})
            else:
                for k in list(pos_dict.keys()):
                    start, end = map(int, k.split('_'))
                    if (annot['end'] > start >= annot['start']) or (annot['end'] >= end > annot['start']):
                        pos_dict.pop(k)
                pos_dict[f"{annot['start']}_{annot['end']}"] = {'ner_1': f"B-{annot['labels'][0]}",
                                                                'word': annot['text']}
        else:
            start_idx = annot['start']
            for i, word in enumerate(annot_text):
                end_idx = start_idx + len(word)
                if f"{start_idx}_{end_idx}" in pos_dict:
                    if i == 0:
                        pos_dict[f"{start_idx}_{end_idx}"].update({'ner_1': f"B-{annot['labels'][0]}"})
                    else:
                        pos_dict[f"{start_idx}_{end_idx}"].update({'ner_1': f"I-{annot['labels'][0]}"})
                else: # Key doesn't match perfectly
                    if i == 0:
                        pos_dict[f"{start_idx}_{end_idx}"] = {'ner_1': f"B-{annot['labels'][0]}",
                                                              'word': word}
                    else:
                        pos_dict[f"{start_idx}_{end_idx}"] = {'ner_1': f"I-{annot['labels'][0]}",
                                                              'word': word}

                start_idx = end_idx + 1


def prepare_annotation(element: dict) -> list:
    sentence_text = element.get('rawText', '')
    annotations = element.get('predictions', '')
    try:
        annotations = ast.literal_eval(annotations)
    except ValueError as e:
        logging.warning(f'Malformed prediction data. Discarding element with id {element["id"]}')
        return []
    annotations = [x['value'] for x in annotations]
    annotations = clear_overlaps(annotations)
    pos_dict = {}
    doc = nlp(sentence_text)
    for sent in doc.sentences:
        [pos_dict.update({f"{token.start_char}_{token.end_char}": {'word': token.text, 'ner_1': 'O'}}) for token in sent.tokens]

    convert_to_iob(annotations, pos_dict)
    return list(pos_dict.values())

def find_intersection(a: dict, b: dict) -> bool:
    a_range = range(a['start'], a['end'])
    b_range = range(b['start'], b['end'])
    overlap = set(a_range).intersection(set(b_range))
    if overlap:
        return True
    else:
        return False
    

def clear_overlaps(annotations: list) -> list:
    for a,b in combinations(annotations, 2):
        overlap = find_intersection(a,b)
        if overlap and a in annotations and b in annotations:
            if a['end'] - a['start'] > b['end'] - b['start']:
                annotations.remove(b)
            else:
                annotations.remove(a)
    return annotations
