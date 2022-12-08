import re
import stanza
stanza.download('et')
nlp = stanza.Pipeline('et', processors='tokenize,pos,lemma', use_gpu=False)  # , download_method=None,
    # dir='/app/stanza_resources/')  # change to True, if using gpu

def tokenize_pos_text(text):
    doc = nlp(text)
    sentences = []
    lemmatized = []
    for sent in doc.sentences:
        words_in_sent = ' '.join([token.text for token in sent.tokens])
        lemmas_in_sent = ' '.join([token.lemma.replace('_', '') for token in sent.words])
        sentences.append(words_in_sent)
        lemmatized.append(lemmas_in_sent)

    return sentences, lemmatized


def detokenize(text):
    # kellaajad 18:18 JA 18.18 ehk siis kõik nr-te vahelised asjad
    text = re.sub(r'\s(?=[.,:!?\'\"])', '', text)
    text = re.sub(r'(?<=[0-9][.:-])\s(?=[0-9])', '', text)
    return text
