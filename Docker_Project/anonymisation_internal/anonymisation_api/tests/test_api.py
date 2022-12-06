import requests
import json
import time
URL = 'http://web:5001/'

time.sleep(300)
def test_predict_simple():
    url = URL + 'predict'
    request_body = {"texts": [

        "Mu email on peeter@gmail.com ja see on kõik"

    ], "tokenize": True, "truecase": True, "pseudonymise": True, "thresholds": {}, "disabled_entities": [],
        "detokenize": True}
    r = requests.post(url=url, json=request_body)
    response = r.text
    res = json.loads(response)
    assert len(res) == 1
    assert res[0].get('sisendtekst') == "Mu email on peeter@gmail.com ja see on kõik"
    assert res[0].get('anonümiseeritud_tekst') == "mu email on [Email] ja see on kõik"
    assert 'Mapping' in res[0].keys()


def test_predict_negative_no_text():
    url = URL + 'predict'
    request_body = {}
    r = requests.post(url=url, json=request_body)
    response = r.text
    res = json.loads(response)
    assert res.get('Message') == "'texts' not in request."


def test_predict_empty_text():
    url = URL + 'predict'
    request_body = {"texts": [

    ], "tokenize": True, "truecase": True, "pseudonymise": True, "thresholds": {}, "disabled_entities": [],
        "detokenize": True}
    r = requests.post(url=url, json=request_body)
    response = r.text
    res = json.loads(response)
    assert res == []

def test_predict_negative_wrong_input_text():
    url = URL + 'predict'
    request_body = {"texts": 100, "tokenize": True, "truecase": True, "pseudonymise": True, "thresholds": {}, "disabled_entities": [],
        "detokenize": True}
    r = requests.post(url=url, json=request_body)
    response = r.text
    res = json.loads(response)
    assert res.get("Message") == "'texts' should be a list not a <class 'int'>"


def test_predict_negative_too_many_input_text():
    url = URL + 'predict'
    request_body = {"texts": ["kana"]*101, "tokenize": True, "truecase": True, "pseudonymise": True, "thresholds": {},
                    "disabled_entities": [],
                    "detokenize": True}
    r = requests.post(url=url, json=request_body)
    response = r.text
    res = json.loads(response)
    assert res.get("Message") == "Maximum limit of 100 texts is exceeded, current amount 101."

def test_train():
    url = URL + 'train'
    request_body = {}
    r = requests.post(url = url, json=request_body)
    response = r.text
    res = json.loads(response)
    assert res.get("Message") == "Training started"





