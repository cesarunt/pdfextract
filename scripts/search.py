import re
from itertools import groupby

# Split the string
word_list_init = []

def pdf_search(keyword = ""):
    word_list_init = keyword.split()
    # print("Texto Inicial")
    # print(word_list_init)
    word_list_last = []
    # Verify if exists consonants 'rr', 'll'
    i = 0
    for word in word_list_init:
        if len(word) > 2:
            valid = []
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
                            'pos':  i,
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