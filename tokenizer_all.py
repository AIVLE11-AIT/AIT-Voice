from kiwipiepy import Kiwi
import spacy
import string

nlp = spacy.load("en_core_web_trf")

def interjection_ko(input):
    kiwi = Kiwi()
    result = kiwi.tokenize(input)
    intj_cnt_ko = 0
    for i in result:
        if 'IC' in i:
            intj_cnt_ko += 1

    return intj_cnt_ko

def interjection_en(input):
    doc = nlp(input)
    intj_cnt_en = 0
    for token in doc:
        if token.pos_ == "INTJ":
            intj_cnt_en += 1
    return intj_cnt_en

def tokenizer_ko(input):
    text = input.translate(str.maketrans('', '', string.punctuation))
    temp = text.replace(' ', '')
    syllable_count = len(temp)
    return syllable_count

def tokenizer_en(input):
    doc = nlp(input)
    # word_count = len([token for token in doc if not token.is_punct and not token.is_space])
    word_count = sum(1 for token in doc if not token.is_punct and not token.is_space)
    return word_count
