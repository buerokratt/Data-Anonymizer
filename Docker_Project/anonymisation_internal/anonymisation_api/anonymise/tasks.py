import json

from worker import celery
from training.run_ner import main
from celery.utils.log import get_task_logger
from anonymise import predict_ne
from random import choice
from string import ascii_uppercase
import requests

logger = get_task_logger(__name__)

def predict(request_obj):
    """
    :return: {"input_text": text, "Mapping": dict , "anonymised_text": text, "pseudonymised_text":text}
    """
    if "texts" not in request_obj.keys():
        return {"Message": "'texts' not in request."}

    texts = request_obj.get("texts")
    if type(texts) != list:
        if type(texts) == str:
            texts = [texts]
        else:
            return ({"Message": "'texts' should be a list not a {}".format(type(texts))})

    if "thresholds" not in request_obj.keys():
        thresholds = {}
    else:
        thresholds = request_obj.get("thresholds")
    if type(thresholds) != dict:
        return {"Message": "'thresholds' should be a dictionary not a {}".format(type(texts))}


    if "detokenize" not in request_obj.keys():
        detokenize = True
    else:
        detokenize = request_obj.get("detokenize")

    if "disabled_entities" not in request_obj.keys():
        disabled_entities = []
    else:
        disabled_entities = request_obj.get("disabled_entities")
        disabled_entities = ['B-' + ent for ent in disabled_entities] + ['I-' + ent for ent in disabled_entities]

    # if len(texts) > 100:
    #     return jsonify(
    #         {"Message": "Maximum limit of 100 texts is exceeded, current amount {}.".format(len(texts))}), 400
    if "pseudonymise" not in request_obj.keys():
        pseudonymise = True
    else:
        pseudonymise = request_obj.get("pseudonymise")

    if "tokenize" not in request_obj.keys():
        tokenize = True
    else:
        tokenize = request_obj.get("tokenize")
    if "truecase" not in request_obj.keys():
        truecase = True
    else:
        truecase = request_obj.get("truecase")

    # app.logger.debug(
    #     "Anonymisation started with following parameters\ntokenize: {}, do_pseudonymisation: {}, thresholds: {}, disabled_entities: {}, do_detokenize: {}".format(
    #          tokenize, pseudonymise, thresholds, disabled_entities, detokenize))
    outputs = []

    for text in texts:
        anonymised_text, pseudonymised_text, mapping, tokenized_text = predict_ne(
        orig_text=text,
        tokenize=tokenize, truecase=truecase, do_pseudonymisation=pseudonymise, thresholds=thresholds,
        disabled_entities=disabled_entities, do_detokenize=detokenize)
        outputs.append({"input_text": text, "Mapping": mapping, "anonymised_text": anonymised_text,
                    "pseudonymised_text": pseudonymised_text})
    # app.logger.debug("Anonymisation ended.")

    return outputs

@celery.task(bind=True)
def annotate_corpora_task(self):
    try:
        logger.info("Annotating Corpora")
        r = requests.post(url = 'http://resql:8082/get_latest_corpora')
        orig_texts = r.json()
        texts = [x['rawText'] for x in orig_texts]
        logger.info("Got Models")
        outputs = predict({
            "pseudonymise": True,
            "texts": texts,
            "thresholds": {},
            "tokenize": True,
            "truecase": True
        })
        logger.info("Prediction Done")
        result = []
        for index, output in enumerate(outputs):
            res = {"sentences_annotations": [], "annotate_existing_task": False, "id": orig_texts[index]["id"], "corpora_id": orig_texts[index]["corporaId"] }
            # curr_index = 0
            logger.info(output)
            for i, word in enumerate(output["Mapping"]):
                len_word = len(word['Algne'])
                if word['Tag'] != 'O' or word.get('regex_entity_tag'):
                    res['sentences_annotations'].append({
                        "id": ''.join(choice(ascii_uppercase) for x in range(10)),
                        "from_name": "label",
                        "origin": "manual",
                        "is_prelabelled": True,
                        "to_name": "text",
                        "type": "labels",
                        "value": {
                            "start": word['start_i'],
                            "end": word['end_i'],
                            "labels": [word.get('regex_entity_tag')] if word.get('regex_entity_tag') else [word['Tag'].split("_")[0]],
                            "text": word['Algne']
                        }
                    })
                # next_curr_index = len_word + 1
                # try:
                #     curr_index+=(next_curr_index if output["input_text"][curr_index + next_curr_index] == output["Mapping"][i+1]['Algne'][0] else len_word)
                # except Exception as e:
                #     curr_index+=len_word
            res['sentences_annotations'] = json.dumps(res['sentences_annotations'])
            result.append(res)
        logger.info("Posting Result")
        requests.post(url = 'http://resql:8082/upsert_corpora_task/batch', json={"queries": result})
    except Exception as e:
        logger.info('error')
        logger.info(e)

@celery.task(bind=True)
def train(id):
    logger.info("started training")
    try:
        main()
    except Exception as e:
        print(e)
        logger.error(e)
    logger.info("training ended")
    return json.dumps({'Message':'Started training', 'code':'SUCCESS'})

