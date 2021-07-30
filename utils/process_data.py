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
        cfg.LIST.PATTERN_TYPE_ES,
        cfg.LIST.PATTERN_DESI_ES,
        cfg.LIST.PATTERN_APPR_ES,
        cfg.LIST.PATTERN_LEVE_ES,
        cfg.LIST.PATTERN_SAMP_ES,
        cfg.LIST.PATTERN_TOOL_ES,
        cfg.LIST.PATTERN_RESU_ES,
        cfg.LIST.PATTERN_CONC_ES
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
        cfg.LIST.PATTERN_TYPE_EN,
        cfg.LIST.PATTERN_DESI_EN,
        cfg.LIST.PATTERN_APPR_EN,
        cfg.LIST.PATTERN_LEVE_EN,
        cfg.LIST.PATTERN_SAMP_EN,
        cfg.LIST.PATTERN_TOOL_EN,
        cfg.LIST.PATTERN_RESU_EN,
        cfg.LIST.PATTERN_CONC_EN
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
# getting long data
def getData_ResultText(text_page, PATTERN):
    result = False
    pos = 0
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            # print("Result pattern: "+pattern+" found:"+str(patt))
            # print("patt text: "+str(text_page[patt.start(0):].split('. ')[0]))
            pos = patt.start(0)
            result = True
            break

    return result, pos

def getData_LongText(text_page, PATTERN, limit_start, limit_end):
    # limit_start = S or E
    # limit_end   = '. '
    text = ""
    for pattern in PATTERN :
        obj = ""
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            print("\nLong pattern: "+pattern+" found:"+str(patt))
            if limit_end == ''  : obj = text_page[patt.end(0)+1:]
            else :
                if limit_start == 'S':
                    if len(text_page[patt.start(0):].split(limit_end)[0]) < len(pattern) :
                        obj = text_page[patt.start(0):].split(".\n")[0]
                    else :
                        obj = text_page[patt.start(0):].split(limit_end)[0]
                if limit_start == 'E':
                    if len(text_page[patt.end(0)+1:].split(limit_end)[0]) < len(pattern) :
                        obj = text_page[patt.end(0)+1:].split(".\n")[0]
                    else:
                        obj = text_page[patt.end(0)+1:].split(limit_end)[0]
            # obj = text_page[limit_start:-1].split(limit_end)[0]
            obj = obj.replace("\n", "")
            if len(obj)>0:  
                text = obj
                break
    return text

def getData_LongText_Result(text_page, PATTERN, limit_start='E', limit_end='. \n'):
    # limit_start = S or E
    # limit_end   = '. '
    text = ""
    for pattern in PATTERN :
        obj = ""
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            # print("\nLong pattern: "+pattern+" found:"+str(patt))
            if limit_end == ''  : obj = text_page[patt.end(0)+1:]
            else :
                # if limit_start == 'E':
                if len(text_page[patt.end(0)+1:].split(limit_end)[0]) < len(pattern) :
                    obj = text_page[patt.end(0)+1:].split(".\n")[0]
                    obj = obj.replace("\n", "")
                else:
                    obj = text_page[patt.end(0)+1:].split(limit_end)
                    # obj = text_page[limit_start:-1].split(limit_end)[0]
                    # obj = obj.replace("\n", "")
            if len(obj)>0:  
                text = obj
                break
    return text

def getData_Long(text_page, PATTERN):
    # find the text from patterns
    text = ""
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        # print("pattern: "+str(patt))
        if patt != None :
            obj = text_page[patt.start(0):-1].split('.')[0]
            obj = obj.replace("\n", "")
            if obj[0]=='.': obj=obj[1:]
            if len(obj)>0:  
                text = obj
                break
    return text

# getting short data
def getLevel_Result(text_page, PATTERN):
    # find the text from patterns
    result = False
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            result = True
            break
    return result

def getTools_ResultCount(text_page, PATTERN):
    list = []
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            list.append(patt.group(0))
    return list

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