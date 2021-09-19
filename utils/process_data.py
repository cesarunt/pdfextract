from utils.config import cfg
# from textblob import TextBlob
from langdetect import detect
# from statistics import mode
from scipy import stats as s
import re

# PATTERNS SPANISH
# general patterns
patterns_es = [ 
        cfg.LIST.BLOCK_WORDS_ES,
        cfg.LIST.BLOCK_AUTHOR_ES,
        cfg.LIST.PATTERN_ABST_ES,
        cfg.LIST.PATTERN_METHOD_ES,
        cfg.LIST.PATTERN_SUBTIT_ES,
        cfg.LIST.PATTERN_ARTI_ES,
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
        cfg.LIST.BLOCK_AUTHOR_EN,
        cfg.LIST.PATTERN_ABST_EN,
        cfg.LIST.PATTERN_METHOD_EN,
        cfg.LIST.PATTERN_SUBTIT_EN,
        cfg.LIST.PATTERN_ARTI_EN,
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

# getting for URL
def getData_ResultURL(text_page, PATTERN):
    result_res = False
    result_text = ""
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            obj = text_page[patt.start(0):].split(" ")[0]
            if len(obj)>0:
                result_res = True
                result_text = obj
                break

    return result_res, result_text

# getting for doi
def getData_ResultDOI(text_page, PATTERN):
    result_res = False
    result_text = ""
    # print(text_page)
    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            obj = text_page[patt.start(0):].split("\n")[0]
            if len(obj)>len(pattern):
                result_res = True
                result_text = obj
                break

    return result_res, result_text

# getting for resumen
def getData_TitleResumen(text_page, PATTERN, limit, intro_font) :
    resumen_title = ""
    # patt_band = False

    text_page = text_page.replace("   ", "#_")
    text_page = text_page.replace("  ", "#_")
    text_page = text_page.replace("#_", " ")
    # print(text_page)

    for pattern in PATTERN[:limit]:
        patt = re.search(rf"{pattern}", text_page, re.IGNORECASE)
        # print("... patt: " + pattern + "  - intro: "+ str(intro_font))
        if patt != None :
            # print("PATTERN: " + pattern ) 
            # patt_band = True 
            resumen_title = pattern
            break
        
    return resumen_title

# def getData_ResultResumen(text_page, PATTERN, band):
def getData_ResultResumen(pagelines_list, resumen_title, PATTERN, limit, band, pagefonts_mode):
    result_text = ""
    result_page = False
    find_title = False
    # font_title = 0
    font_title_list = []
    patt_band = False
    result_lines = []
    list_count = 0
    list_fonts = []
    list_max_key = 0        # len(key)
    list_max_font = 0       # max value
    font_title = pagefonts_mode

    max_long = 0
    max_font = 0
    for item in pagelines_list:
        if len(item[0])>max_long:
            max_long = len(item[0])
            max_font = item[1]
            # print("text "+ item[0])
    if max_long > 400 : pagefonts_mode = max_font

    # print("introduction_mode: "+ str(pagefonts_mode))
    # print("\n Result LIST")
    # for item in pagelines_list:
    #     print(item)

    if band == False : result_lines = pagelines_list
    else :
        for key,value,_ in pagelines_list:
            if find_title == False:
                patt = re.search(rf"{resumen_title}", key, re.IGNORECASE)
                # print("... Patt key: " + key + "  - value: "+ str(value))
                if patt != None: # and value==pagefonts_mode:
                    # print("*** Start: " + str(patt) + "  - key_value:" + key +"_"+ str(value))
                    find_title = True
                    font_title = value
                    # print("----font_title: "+ str(font_title))
                    result_lines.append(tuple([key, value, 0]))
                    continue
            if find_title==True:
                list_count += 1
                if list_count < 5 :
                    list_fonts.append(value)
                    if len(key)>list_max_key:
                        list_max_key = len(key)
                        list_max_font = value
                    # list_mode = mode(list_fonts)
                    list_mode = s.mode(list_fonts)[0]
                # if value==font_title:
                result_lines.append(tuple([key, value, 0]))
                    # font_title_list.append(value)
        if list_max_font == list_mode :
            font_title = list_mode
    
    # print("font_title: "+ str(font_title))
    # print("\n Result Lines")
    # for item in result_lines:
    #     print(item)

    if len(result_lines)>0 :
        for key, value, _ in result_lines:
            for pattern in PATTERN[limit:]:
                patt = re.search(rf"{pattern}", key, re.IGNORECASE)
                if patt != None :
                    # print("*** End: " + str(patt) + "  - key_value:" + key +"_"+ str(value))
                    patt_band=True; break
            if patt_band:
                result_page = True
                break
            elif value == font_title:  # ///////////////////////////////////////////////////////////
                result_text = result_text + key
            # elif value==pagefonts_mode:
            #     result_text = result_text + key
    # print("TEXT....")
    # print(result_text)

    return result_text, result_page


# getting for introduction
def getData_TitleIntroduction(text_page, PATTERN, limit, intro_font) :
    resumen_title = ""
    # patt_band = False

    for pattern in PATTERN[:limit]:
        patt = re.search(rf"{pattern}", text_page, re.IGNORECASE)
        # print("... patt: " + pattern + "  - intro: "+ str(intro_font))
        if patt != None :
            # print("PATTERN: " + pattern + " - " + key + " - " + str(value)) 
            # patt_band = True 
            resumen_title = pattern
            break
        
    return resumen_title

def getData_ResultIntroduction(pagelines_list, introduction_title):
    find_title = False
    # result_lines = []
    introduction_mode = 0

    for key,value,_ in pagelines_list:
        if find_title == False:    # author_band = True; continue
            patt = re.search(rf"{introduction_title}", key, re.IGNORECASE)
            if patt != None:
                # print("*** patt: " + str(patt) + "  - key_value:" + key +"_"+ str(value))
                find_title = True
                continue
        else:
            # result_lines.append(tuple([key, value, 0]))
            introduction_mode = value
            break
    # print("\nResult Intro")
    # for item in result_lines:
    #     print(item)

    return introduction_mode

# getting for methodology
def getData_TitleMethodology(text_page, PATTERN, limit) :
    methodology_title = ""
    # patt_band = False
    # print(text_page)

    # method_font_max = max(text_page, key=lambda x:x[1])[1]
    # for key,value in text_page:
    for pattern in PATTERN[:limit]:
        patt = re.search(rf"{pattern}", text_page)
        # print("__ PATTERN: " + str(patt) + " - pattern: " + pattern)
        if patt != None :
            # print("PATTERN: " + str(patt) ) 
            # patt_band = True 
            methodology_title = pattern
            break
    
    return methodology_title

def getData_ResultMethodology(pagelines_list, methodology_title, PATTERN, limit, band, intro_font, introduction_mode):
    result_text = ""
    result_page = False
    find_title = False
    patt_band = False
    result_lines = []
    font_title = introduction_mode

    # print("\n Result LIST")
    # for item in pagelines_list:
    #     print(item)
    # print('intro_font: '+ str(intro_font))
    # print("introduction_mode: "+ str(introduction_mode))

    if band == False : result_lines = pagelines_list
    else :
        for key,value,_ in pagelines_list:
            if find_title == False:
                patt = re.search(rf"{methodology_title}", key)
                # print("\n___PREV patt: " + str(patt) + "  - key_value:" + key +" _ "+ str(value))
                if (patt != None): # and value==intro_font) or (patt != None and value==introduction_mode):
                    # print("\n___Start patt: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
                    find_title = True
                    font_title = value
                    result_lines.append(tuple([key, value, 0]))
                    continue
            if find_title==True:
                if value==font_title:
                    result_lines.append(tuple([key, value, 0]))

    # print("font_title: "+ str(font_title))
    # print("\n Result Lines")
    # for item in result_lines:
    #     print(item)

    if len(result_lines)>0 :
        for key, value, _ in result_lines:
            for pattern in PATTERN[limit:]:
                patt = re.search(rf"{pattern}", key, re.IGNORECASE)
                # print("\n___POST patt: " + str(pattern) + " _ "+ str(value))
                if patt != None: # and value == intro_font) or (patt != None and value==introduction_mode):
                    # print("\n___End patt: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
                    patt_band=True; break
            if patt_band:
                result_page = True
                break
            elif value == font_title : # or value==introduction_mode:
                result_text = result_text + key

    return result_text, result_page

# getting for result
def getData_TitleResults(text_page, PATTERN, limit, intro_font):
    methodology_title = ""
    # patt_band = False

    # method_font_max = max(text_page, key=lambda x:x[1])[1]
    # for key,value in text_page:
    text_page = text_page.replace("   ", "#_")
    text_page = text_page.replace("  ", "#_")
    text_page = text_page.replace("#_", " ")
    # print("\nText Page ...")
    # print(text_page)
    for pattern in PATTERN[:limit]:
        patt = re.search(rf"{pattern}", text_page)
        # print("PATTERN: " + pattern + " ...intro:" + str(intro_font))
        if patt != None :#and value == intro_font:
            # print("\nResult OK:" + str(intro_font))
            # patt_band = True
            methodology_title = pattern
            break
    # if patt_band : break
    
    return methodology_title

def getData_ResultResults(text_page, methodology_title, PATTERN, limit, band, pagefonts_mode):
    result_page = False
    result_text = ""
    result_band = False

    text_page = text_page.replace("   ", "#_")
    text_page = text_page.replace("  ", "#_")
    text_page = text_page.replace("#_", " ")

    if band == False : result_text = text_page
    else :
        patt = re.search(rf"\b{methodology_title}\b", text_page)
        if patt != None :
            result_text = text_page[patt.end(0):]
    
    if result_band == False :
        for pattern in PATTERN[limit:] :
            patt = re.search(rf"\b{pattern}\b", result_text)
            if patt != None :
                result_text = result_text[:patt.start(0)]
                result_page = True
                break

    return result_text, result_page

# getting for article
def getData_ResultArticle(text_page, PATTERN):
    result_res = False
    result_text = ""

    text_page = text_page.replace("   ", "#_")
    text_page = text_page.replace("  ", "#_")
    text_page = text_page.replace("#_", " ")

    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            obj = text_page[patt.start(0):].split("\n")[0]
            if len(obj)>0:
                result_res = True
                result_text = obj
                break

    return result_res, result_text

# getting long data
def getData_ResultText(text_page, PATTERN):
    result = False
    pos = 0
    text_page = text_page.replace("   ", "#_")
    text_page = text_page.replace("  ", "#_")
    text_page = text_page.replace("#_", " ")

    for pattern in PATTERN :
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        if patt != None :
            pos = patt.start(0)
            result = True
            break

    return result, pos

def getData_LongText(text_page, PATTERN, limit_start, limit_end):
    text = ""
    text_page = text_page.replace("   ", "#_")
    text_page = text_page.replace("  ", "#_")
    text_page = text_page.replace("#_", " ")

    for pattern in PATTERN :
        obj = ""
        patt = re.search(rf"\b{pattern}\b", text_page, re.IGNORECASE)
        # print("\nLong pattern: "+pattern+" found:"+str(patt))
        if patt != None :
            # print("\nLong pattern: "+pattern+" found:"+str(patt))
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
    text = ""
    text_page = text_page.replace("   ", "#_")
    text_page = text_page.replace("  ", "#_")
    text_page = text_page.replace("#_", " ")

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
    language = ""
    # language = TextBlob(text_page).detect_language()
    language = detect(text_page)
    return language

def lang_loadPatterns(language):
    lib_spacy = ""
    patterns = []
    patterns_level = []
    patterns_approach = []
    # load patterns for language
    if language == "es" :
        patterns = patterns_es
        patterns_level = patterns_level_es
        patterns_approach = patterns_approach_es
        lib_spacy = "es_core_news_sm"; #from spacy.lang.es.stop_words import STOP_WORDS
    else :
        patterns = patterns_en
        patterns_level = patterns_level_en
        patterns_approach = patterns_approach_en
        lib_spacy = "xx_ent_wiki_sm"; #from spacy.lang.en.stop_words import STOP_WORDS

    # NLP = spacy.load(lib_spacy)
# --------------------=-=-=-=-=-====-=-=-=-=
    return lib_spacy, patterns, patterns_level, patterns_approach

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