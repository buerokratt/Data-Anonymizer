import  torch
from transformers import BertTokenizer, BertForTokenClassification


CONVERSIONS = {'B-ORG': 'B-Asutus', 'I-ORG': 'I-Asutus', 'B-LOC': 'B-Aadress', 'I-LOC': 'I-Aadress',
                            'B-PER': 'B-Nimi', 'I-PER': 'I-Nimi', 'B-TIME': 'B-Aeg', 'I-TIME': 'I-Aeg',
                            'B-DATE': 'B-Aeg',
                            'I-Date': 'I-Aeg'}
ALL_LABELS = {0: 'B-Nimi',
                                    1: 'I-Nimi',
                                    2: 'B-Asutus',
                                    3: 'I-Asutus',
                                    4: 'B-Aadress',
                                    5: 'I-Aadress',
                                    6: 'O'}

OLD_LABELS = {0: 'O',
                                1: 'B-PER',
                                2: 'I-PER',
                                3: 'B-ORG',
                                4: 'I-ORG',
                                5: 'B-LOC',
                                6: 'I-LOC'}

NEW_LABELS = {0: 'B-PROD',
                                1: 'I-PROD',
                                2: 'B-DATE',
                                3: 'I-DATE',
                                4: 'B-TIME',
                                5: 'I-TIME',
                                6: 'B-EVENT',
                                7: 'I-EVENT',
                                8: 'B-MONEY',
                                9: 'I-MONEY',
                                10: 'B-PERCENT',
                                11: 'I-PERCENT',
                                12: 'O',
                                13: 'B-PER',
                                14: 'I-PER',
                                15: 'B-ORG',
                                16: 'I-ORG',
                                17: 'B-LOC',
                                18: 'I-LOC',
                                19: 'B-TITLE',
                                20: 'I-TITLE',
                                21: 'B-GPE',
                                22: 'I-GPE',
                                23: ''}

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




def predict_all(sentence: list, bert_tokenizer, bertner, labelmap, thresholds: dict, device:str) -> list:
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

    for token, prediction_group, prediction_group_second, values, first_value in zip(sentence, aligned_predictions,
                                                                                         aligned_predictions_second,
                                                                                         values_predictions_second,
                                                                                         values_predictions_first):
        try:
            label = prediction_group[0]
            if label in CONVERSIONS.keys():
                label = CONVERSIONS.get(label)
            else:
                label = 'O'
            threshold = thresholds.get(label.split('-')[-1])
            if threshold is not None:
                if first_value[0] < threshold:
                    label = 'O'
            label_alt = prediction_group_second[0]
            if label_alt in CONVERSIONS.keys():
                label_alt = CONVERSIONS.get(label_alt)
            else:
                label_alt = 'O'
            if label == 'O':
                threshold = thresholds.get(label_alt.split('-')[-1])
                if threshold is not None:
                    if values[0] >= threshold:
                        label = label_alt

            predicted_labels.append(label)
        except Exception as e:
            print(e)
            predicted_labels.append('O')

    return predicted_labels


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
            if label in CONVERSIONS.keys():
                label = CONVERSIONS.get(label)
            else:
                label = 'O'
            threshold = thresholds.get(label.split('-')[-1])
            if threshold is not None:
                if first_value[0] < threshold:
                    label = 'O'

            label_alt = prediction_group_second[0]
            if label_alt in CONVERSIONS.keys():
                label_alt = CONVERSIONS.get(label_alt)
            else:
                label_alt = 'O'
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
        except:
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
        print(sentence, "truecase", e)  # unknwon token triggers it
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
            predicted_labels.append('Lower')
    truecased = [token if label == 'Lower' else token.upper() if label == 'AUpper' else token.capitalize() for
                    label, token in
                     zip(predicted_labels, sentence)]
    return ' '.join(truecased)



def find_ne(text, thresholds):
    words = text.split()
    predicted_tags1 = predict_na(words, bert_new_tokenizer, bert_new_model, NEW_LABELS, thresholds, 'cpu')  # new
    predicted_tags2 = predict_na(words, bert_old_tokenizer, bert_old_model, OLD_LABELS, thresholds, 'cpu')  # old
    predicted_tags3 = predict_all(words, bert_all_res_tokenizer, bert_all_model_res, ALL_LABELS, thresholds, 'cpu')  # all
    new_sentence = []
    for token1, token2, token3, w in zip(predicted_tags1, predicted_tags2, predicted_tags3,
                                         words):
        tag1 = token1  # finetuned ner ?
        tag2 = token2  # vana ner ?
        tag3 = token3  # uus ner?

        if 'Asutus' in tag3:
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
    return new_sentence
