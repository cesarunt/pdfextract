import re
import unidecode
from itertools import groupby

SEARCH_WORDS_ES = ['innovacion', 'INNOVACION']

# Split the string
word_list_init = []

def pdf_search(keyword = ""):
    word_list_init = keyword.split()
    # print("Texto Inicial")
    # print(word_list_init)
    word_list_last = []
    # Verify if exists consonants 'rr', 'll'
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
    # print("Texto Final")
    # print(word_list_final)

    return word_list_final