import re, os
import unidecode
from itertools import groupby
from textblob import Word
import fasttext
import textblob.exceptions
from textblob.translate import Translator

SEARCH_WORDS_ES = ['innovacion', 'INNOVACION']

# Split the string
word_list_init = []

def pdf_search(keyword = "", global_path = ""):
    keyword_trans = ""
    word_list_final = []
    
    # detect language
    try:
        # languages = [Language.ENGLISH, Language.SPANISH]
        # detector = LanguageDetectorBuilder.from_languages(*languages).build()
        # language = str(detector.detect_language_of(keyword)).split('.')
        # lang = language[-1]
        fasttext.FastText.eprint = lambda x: None
        model = fasttext.load_model(global_path + '/lid.176.ftz')
        language = model.predict(keyword, k=1)
        lang = str(language[0][0]).split('__')[-1]
        trans = Translator()
        if lang == 'en':
            word = Word(keyword)
            keyword_list = word.spellcheck()
            keyword_result = keyword_list[0][0]
            keyword_trans = trans.translate(keyword_result, from_lang='en', to_lang='es')
            word_list_final.append(keyword_result)
        else:
            lang = 'es'
            keyword_result = keyword
            word_list_final = pdf_search_ES(keyword_result)
    except textblob.exceptions.NotTranslated:
        lang = 'es'
        word_list_final.append(keyword)

    return word_list_final, keyword_trans

def pdf_search_ES(keyword = ""):
    word_list_init = keyword.split()
    word_list_last = []
    # Verify if exists consonants 'rr', 'll', 'cc', 'nn', 'dd', 'pp', 'tt'
    for word in word_list_init:
        if len(word) > 2:
            valid = []
            word = unidecode.unidecode(word)
            if word in SEARCH_WORDS_ES:
                word_list_last.append({
                            'valid': valid,
                            'string': word
                        })
            else:
                count_l = len(re.findall("ll", word))
                if ( count_l > 0 ):
                    valid.append('l')
                count_r = len(re.findall("rr", word))
                if ( count_r > 0 ):
                    valid.append('r')
                count_r = len(re.findall("cc", word))
                if ( count_r > 0 ):
                    valid.append('c')
                count_r = len(re.findall("nn", word))
                if ( count_r > 0 ):
                    valid.append('n')
                count_r = len(re.findall("dd", word))
                if ( count_r > 0 ):
                    valid.append('d')
                count_r = len(re.findall("pp", word))
                if ( count_r > 0 ):
                    valid.append('p')
                count_r = len(re.findall("tt", word))
                if ( count_r > 0 ):
                    valid.append('t')
                # Apply remove 
                word_validate = ''.join(c for c, unused in groupby(word))
                word_es_final = ""
                word_list_last.append({
                                'valid': valid,
                                'string': word_validate
                            })

    word_list_final = []
    for word in word_list_last:
        word_es_final = ""
        for letter in word['string'] :
            value = letter
            if letter in word['valid'] and len(word['valid'])>0:
                value = str(letter+""+letter)
            word_es_final += ''.join(value)
        word_list_final.append(word_es_final)

    return word_list_final