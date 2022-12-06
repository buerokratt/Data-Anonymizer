from anonymise import predict_ne
from flask import Flask, request, jsonify, make_response
from tasks import train
import logging
import json
import requests
from random import choice
from string import ascii_uppercase

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)


@app.route("/predict", methods=["POST"])
def predict(data=None):
    """
    :return: {"sisendtekst": text, "Mapping": dict vms, "anonümiseeritud tekst": text, "pseudonümiseeritud tekst":text}
    """
    request_obj = data if data else request.get_json()
    if "texts" not in request_obj.keys():
        return jsonify({"Message": "'texts' not in request."}), 400

    texts = request_obj.get("texts")
    if type(texts) != list:
        if type(texts) == str:
            texts = [texts]
        else:
            return jsonify({"Message":"'texts' should be a list not a {}".format(type(texts))})


    if "thresholds" not in request_obj.keys():
        return jsonify({"Message": "'thresholds' not in request"}), 400

    thresholds = request_obj.get("thresholds")

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

    app.logger.info("Anonymisation started.")
    outputs = []

    for text in texts:
        anonymised_text, pseudonymised_text, mapping, tokenized_text = predict_ne(
            text=text,
            tokenize=tokenize, truecase=truecase, do_pseudonymisation=pseudonymise, thresholds=thresholds, disabled_entities=disabled_entities, do_detokenize=detokenize)
        outputs.append({"sisendtekst":tokenized_text, "Mapping":mapping, "anonümiseeritud_tekst":anonymised_text, "pseudonümiseeritud_tekst":pseudonymised_text})
    app.logger.info("Anonymisation ended.")

    return outputs if data else make_response(jsonify(outputs), 200)

@app.route("/annotate_corpora", methods=["POST", "GET"])
def annotate_corpora():
    try:
        app.logger.info("Annotating Corpora")
        r = requests.post(url = 'http://resql:8082/get_latest_corpora')
        orig_texts = r.json()
        texts = [x['rawText'] for x in orig_texts]
        outputs = predict({
            "pseudonymise": True,
            "texts": texts,
            "thresholds": {
                "Nimi": 2
            },
            "tokenize": True,
            "truecase": True
        })
        result = []
        for index, output in enumerate(outputs):
            res = {"sentences_annotations": [], "annotate_existing_task": False, "id": orig_texts[index]["id"], "corpora_id": orig_texts[index]["corporaId"] }
            curr_index = 0
            for i, word in enumerate(output["Mapping"]):
                len_word = len(word['Algne'])
                if word['Tag'] != 'O':
                    res['sentences_annotations'].append({
                        "id": ''.join(choice(ascii_uppercase) for x in range(10)),
                        "from_name": "label",
                        "origin": "manual",
                        "to_name": "text",
                        "type": "labels",
                        "value": {
                            "start": curr_index,
                            "end": curr_index + len_word,
                            "labels": [word['Tag'].split("_")[0]],
                            "text": word['Algne']
                        }
                    })
                next_curr_index = len_word + 1
                try:
                    curr_index+=(next_curr_index if output["sisendtekst"][curr_index + next_curr_index] == output["Mapping"][i+1]['Algne'][0] else len_word)
                except Exception as e:
                    curr_index+=len_word
            res['sentences_annotations'] = json.dumps(res['sentences_annotations'])
            result.append(res)
        requests.post(url = 'http://resql:8082/upsert_corpora_task/batch', json={"queries": result})
        return make_response(jsonify({"message": "success"}), 200)
    except Exception as e:
        print('error')
        print(e)

@app.route("/train", methods=["POST"])
def train_model():
    train.delay()
    return jsonify({"Message":'Training started'}), 200

@app.route("/health_check", methods=["GET"])
def health_check():
    return jsonify({"success": True}), 200


if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5001, debug=True)
