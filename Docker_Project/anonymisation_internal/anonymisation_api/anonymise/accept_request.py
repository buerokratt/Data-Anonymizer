from anonymise import predict_ne
from flask import Flask, request, jsonify, make_response
from tasks import train, annotate_corpora_task
import logging
import traceback
from worker import celery
from celery.result import AsyncResult
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

@app.route("/predict", methods=["POST"])
def predict(data=None):
    """
    :return: {"sisendtekst": text, "Mapping": dict , "anonümiseeritud tekst": text, "pseudonümiseeritud tekst":text}
    """
    request_obj = data if data else request.get_json()
    if "texts" not in request_obj.keys():
        return jsonify({"Message": "'texts' not in request."}), 400

    texts = request_obj.get("texts")
    if type(texts) != list:
        if type(texts) == str:
            texts = [texts]
        else:
            return jsonify({"Message": "'texts' should be a list not a {}".format(type(texts))}), 400

    if "thresholds" not in request_obj.keys():
        thresholds = {}
    else:
        thresholds = request_obj.get("thresholds")
    if type(thresholds) != dict:
        return jsonify({"Message": "'thresholds' should be a dictionary not a {}".format(type(texts))}), 400


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

    app.logger.debug(
        "Anonymisation started with following parameters\ntokenize: {}, do_pseudonymisation: {}, thresholds: {}, disabled_entities: {}, do_detokenize: {}".format(
             tokenize, pseudonymise, thresholds, disabled_entities, detokenize))
    outputs = []

    for text in texts:
        try:
            anonymised_text, pseudonymised_text, mapping, tokenized_text = predict_ne(
            orig_text=text,
            tokenize=tokenize, truecase=truecase, do_pseudonymisation=pseudonymise, thresholds=thresholds,
            disabled_entities=disabled_entities, do_detokenize=detokenize)
            outputs.append({"sisendtekst": text, "Mapping": mapping, "anonümiseeritud_tekst": anonymised_text,
                        "pseudonümiseeritud_tekst": pseudonymised_text})
        except Exception as e:

            app.logger.debug("Error occurred : {}, in input: {}".format(e, text) )
            app.logger.debug(traceback.format_exc())
            outputs.append({"Message":"Could not anonymise text: {}".format(text)})
    app.logger.debug("Anonymisation ended.")

    return outputs if data else make_response(jsonify(outputs), 200)

@app.route("/annotate_corpora", methods=["POST", "GET"])
def annotate_corpora():
    task = annotate_corpora_task.delay()
    return jsonify({"Message": 'Annotation started', "task_id": task.id }), 200

@app.route("/prelabelling_status", methods=["POST"])
def get_prelabelling_status():
    task_id = request.get_json().get('task_id')
    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return jsonify(result), 200

@app.route("/train", methods=["POST"])
def train_model():
    app.logger.debug("Training is starting.")
    train.delay()

    return jsonify({"Message": 'Training started'}), 200


@app.route("/health_check", methods=["GET"])
def health_check():
    return jsonify({"success": True}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
