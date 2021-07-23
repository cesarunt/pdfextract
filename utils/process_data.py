from utils.config import cfg
from textblob import TextBlob
# import spacy
import re

# PATTERNS SPANISH
# general patterns
patterns_es = [ 
        cfg.LIST.BLOCK_WORDS_ES,
        cfg.LIST.PATTERN_OBJE_ES,
        cfg.LIST.PATTERN_METH_ES,
        # cfg.LIST.PATTERN_TYPE_ES,
        cfg.LIST.PATTERN_DESI_ES,
        cfg.LIST.PATTERN_APPR_ES,
        cfg.LIST.PATTERN_LEVE_ES,
        cfg.LIST.PATTERN_SAMP_ES
        # cfg.LIST.PATTERN_TOOL_ES
    ]
# level pattern
patterns_level_es = [
        cfg.LIST.PATTERN_LEVE_APPL_ES,
        cfg.LIST.PATTERN_LEVE_PRED_ES,
        cfg.LIST.PATTERN_LEVE_EXPI_ES,
        cfg.LIST.PATTERN_LEVE_RELA_ES,
        cfg.LIST.PATTERN_LEVE_DESC_ES,
        cfg.LIST.PATTERN_LEVE_EXPO_ES
    ]
# approach pattern
patterns_approach_es = [
        cfg.LIST.PATTERN_APPR_QUAN_ES,
        cfg.LIST.PATTERN_APPR_QUAL_ES
    ]

# PATTERNS ENCGLISH
# general patterns
patterns_en = [ 
        cfg.LIST.BLOCK_WORDS_EN,
        cfg.LIST.PATTERN_OBJE_EN,
        cfg.LIST.PATTERN_METH_EN,
        # cfg.LIST.PATTERN_TYPE_EN,
        cfg.LIST.PATTERN_DESI_EN,
        cfg.LIST.PATTERN_APPR_EN,
        cfg.LIST.PATTERN_LEVE_EN,
        cfg.LIST.PATTERN_SAMP_EN
        # cfg.LIST.PATTERN_TOOL_EN
    ]
# level pattern
patterns_level_en = [
        cfg.LIST.PATTERN_LEVE_APPL_EN,
        cfg.LIST.PATTERN_LEVE_PRED_EN,
        cfg.LIST.PATTERN_LEVE_EXPI_EN,
        cfg.LIST.PATTERN_LEVE_RELA_EN,
        cfg.LIST.PATTERN_LEVE_DESC_EN,
        cfg.LIST.PATTERN_LEVE_EXPO_EN
]
# approach pattern
patterns_approach_en = [
        cfg.LIST.PATTERN_APPR_QUAN_EN,
        cfg.LIST.PATTERN_APPR_QUAL_EN
    ]


# GETTING DATA FROM PATTERN (patt)
def patt_getData_Long(text_page, PATTERN):
    # find the text from patterns
    text = ""
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        print("pattern: "+str(patt))
        if patt != None :
            obj = text_page[patt.end(0)+1:-1].split('.')[0]
            # print(obj)
            # if obj_0 and len(obj_0)<300 : obj = obj_0
            # else : obj = text_page[patt.end(0)+1:-1].split('.   ')[0]
            # # re.split(r';|,|\.', str)
            # obj = re.split('.',text_page[patt.end(0)+1:-1)[0]
            text = obj.replace("\n", "")
            if len(text)>0 :
                break
    return text

def patt_getLevel_Short(text_page, PATTERN):
    # find the text from patterns
    result = False
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            # print("pattern: "+str(pattern)+ " ..."+str(patt))
            result = True
            break
    return result

# GETTING THE LANGUAGE (lang)
def lang_getLanguage(text_page):
    language = TextBlob(text_page).detect_language()
    return language

def lang_loadPatterns(language):
    lib_spacy = ""
    patterns = []
    patterns_level = []
    patterns_approach = []
    # load patterns for language
    if language == "en" :
        patterns = patterns_en
        patterns_level = patterns_level_en
        patterns_approach = patterns_approach_en
        lib_spacy = "xx_ent_wiki_sm"; from spacy.lang.en.stop_words import STOP_WORDS
    else :
        patterns = patterns_es
        patterns_level = patterns_level_es
        patterns_approach = patterns_approach_es
        lib_spacy = "es_core_news_sm"; from spacy.lang.es.stop_words import STOP_WORDS
    # NLP = spacy.load(lib_spacy)
# --------------------=-=-=-=-=-====-=-=-=-=
    return lib_spacy, STOP_WORDS, patterns, patterns_level, patterns_approach

# PROCESS DATA AND TEXT
def clear_text_save():
   open("output/reporte.html", "w").close()

def writelines(self, lines):
    self._checkClosed()
    for line in lines:
       self.write(line)

def find_word_in_title(word, title):
    result = 0
    if word[-1]==" ": word = word[:-1]
    if word in title: result = 1
    return result

def find_number_in_word(word):
    result = False
    if word[-1] in cfg.LIST.BLOCK_NUMBERS: 
        result = True
    return result

def find_words_allowed(word_full):
    result = False
    new_word = ""
    # separate word by empty space
    word_parts = word_full.split()
    # print(word_parts)
    for word in word_parts :
        # if find_number_in_word(word)==True :
        #     word = ""
        if word.lower() in cfg.LIST.ALLOW_WORDS :
            result = True
            # new_word = word_full
            break
        # new_word = new_word + word + " "
    return result

def clear_word(word_full, list_words):
    new_word = ""
    # validate each word
    for word in list_words :
        if word in word_full :
            new_word = word_full.split(word)[1]
            break
        else:
            new_word = word_full
    return new_word

def format_word_dash(word_full):
    word_formated = ""
    # separate word by empty space
    word_parts = word_full.split()
    # validate each word
    for word in word_parts :
        if len(word.split("-")) == 1:
            word_formated = word_formated + word + " "
        if len(word.split("-")) == 2:
            word_formated = word_formated + word.split("-")[0] + " " + word.split("-")[1] + " "
    return word_formated