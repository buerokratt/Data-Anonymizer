import nltk
from flask import Flask

import traceback
from utils.pseudonymisation_utils import *
from utils.tokenization_utils import *
from utils.utils import *
import logging
logging.basicConfig(level=logging.DEBUG)
nltk.data.path.append('/app/nltk_data/')
app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

def predict_ne(text: str, tokenize: bool, truecase: bool, do_pseudonymisation: bool, thresholds: dict,
            disabled_entities: list, do_detokenize: bool):
    from utils.model_utils import do_truecase, find_ne
    url_dic, text = find_url(text)
    ner_tagged = []
    confs = []
    if tokenize:
        sentences, lemmatized_sentences = tokenize_pos_text(text)
        for sent in sentences:
            if truecase:
                sent = do_truecase(sent.lower().split())

            tagged, temp_confs = find_ne(sent, thresholds)
            ner_tagged.extend(
                tagged)
            confs.extend(temp_confs)
        text = ' '.join(sentences)
        text_lemmatized = ' '.join(lemmatized_sentences)
    else:
        if truecase:
            text = do_truecase(text.lower().split())
        tagged, temp_confs = find_ne(text, thresholds)

        ner_tagged.extend(tagged)
        confs.extend(temp_confs)
        text_lemmatized = text
    try:
        #app.logger.debug(confs)
        regex_entities = find_regex_entities(text, text_lemmatized, confs)
    except Exception as e:
        regex_entities = {}
        app.logger.debug("Error occurred while matching entities with regex, error: {} and input: {]".format(e, text))
        app.logger.debug(traceback.format_exc())
    try:
        anonymised_text = connect_tags(ner_tagged, disabled_entities, regex_entities, url_dic)
    except Exception as e:
        anonymised_text = text.split()
        app.logger.debug("Error occurred while matching model and regex entities, error: {} and input: {]".format(e, text))
        app.logger.debug(traceback.format_exc())

    mapping = []


    if do_pseudonymisation:
        try:
            pseudo_text, replaced_tags, mapping = pseudonymization(text, anonymised_text)
        except Exception as e:
            app.logger.debug(
                "Error occurred in pseudonymisation, error: {} and input: {}".format(e, text))
            app.logger.debug(traceback.format_exc())
            pseudo_text = text.split()
    else:
        try:
            _, pseudo_text, mapping1 = pseudonymization(text, anonymised_text)
        except Exception as e:
            app.logger.debug(
                "Error occurred in pseudnonymisation, error: {} and input: {]".format(e, text))
            app.logger.debug(traceback.format_exc())
            mapping1 = {}
            pseudo_text = text.split()
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
