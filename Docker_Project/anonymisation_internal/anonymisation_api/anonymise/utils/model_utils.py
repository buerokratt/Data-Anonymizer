import  torch
from transformers import BertTokenizer, BertForTokenClassification
from collections import defaultdict
import logging
from flask import Flask
app = Flask(__name__)
gunicorn_logger = logging.getLogger('gunicorn.error')
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)

ALL_LABELS = {0: 'O',
                                    1: 'B-Nimi',
                                    2: 'I-Nimi',
                                    3: 'B-Asutus',
                                    4: 'I-Asutus',
                                    5: 'B-Aadress',
                                    6: 'I-Aadress',
                                    7: 'B-GPE',
                                    8: 'I-GPE',
                                    9: 'B-Toode',
                                    10: 'I-Toode',
                                    11: 'B-Tiitel',
                                    12: 'I-Tiitel',
                                    13: 'B-Sündmus',
                                    14: 'I-Sündmus',
                                    15: 'B-Kuupäev',
                                    16: 'I-Kuupäev',
                                    17: 'B-Aeg',
                                    18: 'I-Aeg',
                                    19: 'B-Raha',
                                    20: 'I-Raha',
                                    21: 'B-Protsent',
                                    22: 'I-Protsent'}

OLD_LABELS = {0: 'O',
                                1: 'B-Nimi',
                                2: 'I-Nimi',
                                3: 'B-Asutus',
                                4: 'I-Asutus',
                                5: 'B-Aadress',
                                6: 'I-Aadress'}

NEW_LABELS = {0: "B-Toode",
1: "I-Toode",
2: "B-Tiitel",
3: "I-Tiitel",
4: "I-Asutus",
5: "B-Protsent",
6: "I-Kuupäev",
7: "B-Sündmus",
8: "B-Kuupäev",
9: "B-GPE",
10: "I-Aeg",
11: "B-Raha",
12: "B-Aeg",
13: "I-Protsent",
14: "I-Sündmus",
15: "I-Aadress",
16: "O",
17: "B-Aadress",
18: "I-Nimi",
19: "B-Nimi",
20: "I-Raha",
21: "B-Asutus",
22: "I-GPE"}

TC_LABELS = {0: 'Upper', 1: 'Lower'}

    # nltk.data.path.append('/app/nltk_data/')
model_path = '../models/'
device = 'cpu'


bert_new_model = BertForTokenClassification.from_pretrained(model_path + 'bert_new',
                                                                return_dict=True).to(device)
bert_new_tokenizer = BertTokenizer.from_pretrained(model_path + 'bert_new')

bert_old_model = BertForTokenClassification.from_pretrained(model_path + 'bert_old',
                                                                return_dict=True).to(
        device)
bert_old_tokenizer = BertTokenizer.from_pretrained(model_path + 'bert_old')

bert_truecase_model = BertForTokenClassification.from_pretrained(model_path + 'bert-truecaser',
                                                                     return_dict=True).to(
        device)
bert_truecase_tokenizer = BertTokenizer.from_pretrained(model_path + 'bert-truecaser')

bert_all_model_res = BertForTokenClassification.from_pretrained(model_path + 'gdpr_model',
                                                                    return_dict=True).to(device)
bert_all_res_tokenizer = BertTokenizer.from_pretrained(model_path + 'gdpr_model')




def predict_all(sentence: list, bert_tokenizer, bertner, labelmap, thresholds: dict, device:str) -> (list, list):
    grouped_inputs = [torch.LongTensor([bert_tokenizer.cls_token_id])]
    subtokens_per_token = []
    for token in sentence:
        tokens = bert_tokenizer.encode(
                token,
                return_tensors="pt",
                add_special_tokens=False,
            ).squeeze(axis=0)
        grouped_inputs.append(tokens)
        subtokens_per_token.append(len(tokens))

    grouped_inputs.append(torch.LongTensor([bert_tokenizer.sep_token_id]))

    flattened_inputs = torch.cat(grouped_inputs)
    flattened_inputs = torch.unsqueeze(flattened_inputs, 0).long().to(device)
    try:
        bertner.eval()
        with torch.no_grad():
            predictions_tensor = bertner(flattened_inputs)[0]
    except Exception as e:
        app.logger.debug("Unknown token in input, sentence: {}, error: {}".format(sentence, e))
        print(sentence, e)  # unknwon token triggers it
        return ['O' for _ in sentence]
    predictions_tensor = predictions_tensor.to('cpu')

    pred_values, pred_indices = predictions_tensor.topk(2, axis=2)
    first_values = pred_values[0][:, 0][1:-1]
    pred_values, pred_indices = pred_values[0][:, 1][1:-1], pred_indices[0][:, 1][1:-1]
    predictions_tensor = torch.argmax(predictions_tensor, dim=2)[0]

    preds = predictions_tensor[1:-1]
    predictions = [labelmap.get(int(pred)) for pred in preds]
    second_predictions = [labelmap.get(int(pred)) for pred in pred_indices]

    aligned_predictions = []
    aligned_predictions_second = []
    values_predictions_second = []
    values_predictions_first = []
    ptr = 0
    for size in subtokens_per_token:
        group = predictions[ptr:ptr + size]
        aligned_predictions.append(group)
        aligned_predictions_second.append(second_predictions[ptr:ptr + size])
        values_predictions_second.append(pred_values[ptr:ptr + size])
        values_predictions_first.append(first_values[ptr:ptr + size])
        ptr += size
    predicted_labels = []
    confs = []
    for token, prediction_group, prediction_group_second, values, first_value in zip(sentence, aligned_predictions,
                                                                                         aligned_predictions_second,
                                                                                         values_predictions_second,
                                                                                         values_predictions_first):
        try:
            en_values_dic = defaultdict(list)

            label = prediction_group[0]
            en_values_dic[label] = first_value[0]
            threshold = thresholds.get(label.split('-')[-1])
            if threshold is not None:
                if first_value[0] < threshold:
                    label = 'O'
            label_alt = prediction_group_second[0]
            en_values_dic[label_alt] = values[0]
            if label == 'O':
                threshold = thresholds.get(label_alt.split('-')[-1])
                if threshold is not None:
                    if values[0] >= threshold:
                        label = label_alt

            predicted_labels.append(label)
            confs.append((token, en_values_dic))
        except Exception as e:
            app.logger.debug("Exception in predict_all, error: {}, token: {}, assigning entity O.".format(e, token))
            predicted_labels.append('O')
    #app.logger.debug(confs)
    return predicted_labels, confs


def predict_na(sentence: list, bert_tokenizer, bertner, labelmap: dict, thresholds: dict, device:str) -> list:
    grouped_inputs = [torch.LongTensor([bert_tokenizer.cls_token_id])]
    subtokens_per_token = []
    for token in sentence:
        tokens = bert_tokenizer.encode(
                token,
                return_tensors="pt",
                add_special_tokens=False,
        ).squeeze(axis=0)
        grouped_inputs.append(tokens)
        subtokens_per_token.append(len(tokens))

    grouped_inputs.append(torch.LongTensor([bert_tokenizer.sep_token_id]))

    flattened_inputs = torch.cat(grouped_inputs)
    flattened_inputs = torch.unsqueeze(flattened_inputs, 0).long().to(device)
    try:
        bertner.eval()
        with torch.no_grad():
            predictions_tensor = bertner(flattened_inputs)[0]
    except Exception as e:
        app.logger.debug("Unknown token in input, sentence: {}, error: {}".format(sentence, e))
        return ['O' for _ in sentence]
    predictions_tensor = predictions_tensor.to('cpu')
    pred_values, pred_indices = predictions_tensor.topk(2, axis=2)
    first_values = pred_values[0][:, 0][1:-1]
    pred_values, pred_indices = pred_values[0][:, 1][1:-1], pred_indices[0][:, 1][1:-1]

    predictions_tensor = torch.argmax(predictions_tensor, dim=2)[0]

    preds = predictions_tensor[1:-1]
    predictions = [labelmap.get(int(pred)) for pred in preds]
    second_predictions = [labelmap.get(int(pred)) for pred in pred_indices]

    aligned_predictions = []
    aligned_predictions_second = []
    values_predictions_second = []
    values_predictions_first = []
    ptr = 0
    for size in subtokens_per_token:
        group = predictions[ptr:ptr + size]
        aligned_predictions.append(group)
        aligned_predictions_second.append(second_predictions[ptr:ptr + size])
        values_predictions_second.append(pred_values[ptr:ptr + size])
        values_predictions_first.append(first_values[ptr:ptr + size])
        ptr += size
    aligned_predictions = []
    ptr = 0
    for size in subtokens_per_token:
        group = predictions[ptr:ptr + size]
        aligned_predictions.append(group)
        ptr += size
    predicted_labels = []
    previous = 'O'
    for token, prediction_group, prediction_group_second, values, first_value in zip(sentence, aligned_predictions,
                                                                                         aligned_predictions_second,
                                                                                         values_predictions_second,
                                                                                         values_predictions_first):
        try:
            label = prediction_group[0]

            threshold = thresholds.get(label.split('-')[-1])
            if threshold is not None:
                if first_value[0] < threshold:
                    label = 'O'

            label_alt = prediction_group_second[0]

            if label == 'O':
                threshold = thresholds.get(label_alt.split('-')[-1])
                if threshold is not None:
                    if values[0] >= threshold:
                        label = label_alt

            base = label.split('-')[-1]
            if previous == 'O' and label.startswith('I'):
                label = 'B-' + base
            previous = label
            predicted_labels.append(label)
        except Exception as e:
            app.logger.debug("Exception in predict_all, error: {}, token: {}, assigning entity O.".format(e, token))
            predicted_labels.append('O')
    return predicted_labels

def do_truecase(sentence: list) -> str:
    grouped_inputs = [torch.LongTensor([bert_truecase_tokenizer.cls_token_id])]
    subtokens_per_token = []
    for token in sentence:
        tokens = bert_truecase_tokenizer.encode(
                token,
                return_tensors="pt",
                add_special_tokens=False,
        ).squeeze(axis=0)
        grouped_inputs.append(tokens)
        subtokens_per_token.append(len(tokens))

    grouped_inputs.append(torch.LongTensor([bert_truecase_tokenizer.sep_token_id]))

    flattened_inputs = torch.cat(grouped_inputs)
    flattened_inputs = torch.unsqueeze(flattened_inputs, 0).long().to(device)
    try:
        bert_truecase_model.eval()
        with torch.no_grad():
            predictions_tensor = bert_truecase_model(flattened_inputs)[0]
    except Exception as e:
        app.logger.debug("Unknown token in input, sentence: {}, error: {}".format(sentence, e))
        return ' '.join(sentence)
    predictions_tensor = predictions_tensor.to('cpu')
    predictions_tensor = torch.argmax(predictions_tensor, dim=2)[0]
    preds = predictions_tensor[1:-1]
    labelmap = {0: 'Upper', 1: 'Lower', 2: 'AUpper'}
    predictions = [labelmap.get(int(pred)) for pred in preds]

    aligned_predictions = []
    ptr = 0
    for size in subtokens_per_token:
        group = predictions[ptr:ptr + size]
        aligned_predictions.append(group)
        ptr += size
    predicted_labels = []

    for token, prediction_group in zip(sentence, aligned_predictions):
        try:
            label = prediction_group[0]

            predicted_labels.append(label)
        except Exception as e:
            app.logger.debug("Exception in assigning truecasing label, token: {}, label: {}, error: {}".format(token,prediction_group, e))
            predicted_labels.append('Lower')
    truecased = [token if label == 'Lower' else token.upper() if label == 'AUpper' else token.capitalize() for
                    label, token in
                     zip(predicted_labels, sentence)]
    return ' '.join(truecased)



def find_ne(text, thresholds):
    words = text.split()
    predicted_tags1 = predict_na(words, bert_new_tokenizer, bert_new_model, NEW_LABELS, thresholds, 'cpu')  # new
    predicted_tags2 = predict_na(words, bert_old_tokenizer, bert_old_model, OLD_LABELS, thresholds, 'cpu')  # old
    predicted_tags3, confs = predict_all(words, bert_all_res_tokenizer, bert_all_model_res, ALL_LABELS, thresholds, 'cpu')  # all
    new_sentence = []
    for token1, token2, token3, w in zip(predicted_tags1, predicted_tags2, predicted_tags3,
                                         words):
        tag1 = token1  # finetuned ner ?
        tag2 = token2  # vana ner ?
        tag3 = token3  # uus ner?

        if len(set([tag1, tag2, tag3])) == 2:
            #assign tag to the set element that appears two times
            if [tag1, tag2, tag3].count(tag1) == 2:
                tag = tag1
            elif [tag1, tag2, tag3].count(tag2) == 2:
                tag = tag2
            else:
                tag = tag3
        elif 'Asutus' in tag3:
            tag = tag3
        elif tag3 != 'O':
            tag = tag3
        elif tag1 != 'O' or tag2 != 'O':
            if tag1 != tag2:
                if tag1 == 'O':
                    tag = tag2
                elif tag2 == 'O':
                    tag = tag1
                else:
                    tag = tag1
            else:
                tag = tag1
        else:
            tag = tag1

        new_sentence.append((w.strip(), tag))
    return new_sentence, confs
