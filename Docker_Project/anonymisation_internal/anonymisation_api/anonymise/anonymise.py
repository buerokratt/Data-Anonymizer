import nltk
from flask import Flask


from utils.pseudonymisation_utils import *
from utils.tokenization_utils import *
from utils.utils import *

nltk.data.path.append('/app/nltk_data/')
app = Flask(__name__)


def predict_ne(text: str, tokenize: bool, truecase: bool, do_pseudonymisation: bool, thresholds: dict,
            disabled_entities: list, do_detokenize: bool):
    from utils.model_utils import do_truecase, find_ne
    url_dic, text = find_url(text)
    ner_tagged = []
    if tokenize:
        sentences, lemmatized_sentences = tokenize_pos_text(text)
        for sent in sentences:
            if truecase:
                sent = do_truecase(sent.lower().split())

            ner_tagged.extend(
                find_ne(sent, thresholds))
        text = ' '.join(sentences)
        text_lemmatized = ' '.join(lemmatized_sentences)
    else:
        if truecase:
            text = do_truecase(text.lower().split())

        ner_tagged.extend(find_ne(text, thresholds))
        text_lemmatized = text

    regex_entities = find_regex_entities(text, text_lemmatized)

    anonymised_text = connect_tags(ner_tagged, disabled_entities, regex_entities, url_dic)

    mapping = []

    if do_pseudonymisation:
        pseudo_text, replaced_tags, mapping = pseudonymization(text, anonymised_text)

    else:
        _, pseudo_text, mapping1 = pseudonymization(text, anonymised_text)

        for map in mapping1:
            algne = map["Algne"]
            if map["Tag"] == 'O':
                asendatud = algne
            else:
                asendatud = map["Tag"]
            tag = map["Tag"]
            mapping.append({"Algne": algne, "Asendatud": asendatud, "Tag": tag})

    if do_detokenize:
        return detokenize(' '.join(anonymised_text)), detokenize(
            ' '.join(pseudo_text)), mapping, detokenize(text)
    return ' '.join(anonymised_text), ' '.join(pseudo_text), mapping, text
