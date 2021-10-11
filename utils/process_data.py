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
        cfg.LIST.PATTERN_RESUM_ES,
        cfg.LIST.PATTERN_INTRO_ES,
        cfg.LIST.PATTERN_ABST_ES,
        cfg.LIST.PATTERN_METHOD_ES,
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
        cfg.LIST.PATTERN_RESUM_EN,
        cfg.LIST.PATTERN_INTRO_EN,
        cfg.LIST.PATTERN_ABST_EN,
        cfg.LIST.PATTERN_METHOD_EN,
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

# get max and submax 
def getMaxSubmax(font_sizes, font_title):
    max = font_title
    submax = 0
    # print("size: "+ str(len(font_sizes)))
    if len(font_sizes)>2 :
        if font_sizes[0][1] == font_sizes[1][1] == font_sizes[2][1] :
            submax = max
        else:
            for key, value in font_sizes:
                if len(key)>1 and value > submax and value < max:
                    submax = value
            if submax < 5 :
                # Si el valor de submax es menor a 5, seleccionar el número mayor a max
                for key, value in font_sizes:
                    if len(key)>1 and value > max:
                        submax = value
                        break
    
    return max, submax

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
def getData_TitleResumen(pagelines_list, PATTERN, limit1, limit2, font_max) :
    resumen_title = ""
    resumen_pos = 0
    patt_band = False

    # print("\nTITLE Result LIST")
    # for item in pagelines_list:
    #     print(item)
    
    for key, value, line in pagelines_list:
        for pattern in PATTERN[:limit1+limit2]:
            patt = re.search(rf"\b{pattern}\b", key)
            # print("find ...: " + pattern + "... key_value: " + key +" _ "+ str(value)+" line"+ str(line))
            if patt != None and value >= font_max and '...' not in key:
                # print("START 1 __TITLE FOUND: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
                resumen_title = pattern
                resumen_pos = line
                patt_band=True; break
        if patt_band:
            break
    
    # if resumen_title == "" :
    #     for key, value, line in pagelines_list:
    #         for pattern in PATTERN[limit1:limit1+limit2]:
    #             patt = re.search(rf"\b{pattern}\b", key)
    #             if patt != None and value >= font_max:
    #                 print("START 2 __TITLE FOUND: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
    #                 resumen_title = pattern
    #                 resumen_pos = line
    #                 patt_band=True; break
    #         if patt_band:
    #             break
    
    return resumen_title, resumen_pos

def getData_TitleResumen_(pagelines_list, PATTERN, limit1, limit2, font_max) :
    resumen_title = ""
    resumen_pos = 0
    patt_band = False

    # print("\n\n___font_max: "+ str(font_max))
    # print("\n Result LIST")
    # for item in pagelines_list:
    #     print(item)
    
    for key, value, line in pagelines_list:
        if value >= font_max :
            for pattern in PATTERN[:limit1]:
                patt = re.search(rf"\b{pattern}\b", key)
                if patt != None and ('Table' not in key):
                    # print("START 1 __TITLE FOUND: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
                    resumen_title = pattern
                    resumen_pos = line
                    patt_band=True; break
            if patt_band:
                break
    
    if resumen_title == "" :
        for key, value, line in pagelines_list:
            if value >= font_max :
                for pattern in PATTERN[limit1:limit1+limit2]:
                    patt = re.search(rf"\b{pattern}\b", key)
                    # print("find: "+ pattern + "  key_value: " + key +" _ "+ str(value)+ " line: "+str(line))
                    if patt != None and ('Table' not in key):
                        # print("START 2 __TITLE FOUND: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
                        resumen_title = pattern
                        resumen_pos = line
                        patt_band=True; break
                if patt_band:
                    break
    
    return resumen_title, resumen_pos

# def getData_ResultResumen(text_page, PATTERN, band):
def getData_ResultResumen(pagelines_list, resumen_pos, PATTERN, limit1, limit2, band, font_max_, font_submax_):
    result_text = ""
    result_page = False
    find_title = False
    patt_band1, patt_band2 = False, False
    font_sizes = []
    font_max = 0
    font_submax = 0
    result_lines = []
    font_title = 0

    # print("\n Result LIST")
    # for item in pagelines_list:
    #     print(item)
    
    if band == False : 
        result_lines = pagelines_list; font_max = font_max_; font_submax = font_submax_
        # print("Font_max 1: "+ str(font_max) + " - Submax: " + str(font_submax))
    else :
        for key, value, line in pagelines_list:
            if find_title == False:
                if line == resumen_pos :
                # patt = re.search(rf"{resumen_title}", key, re.IGNORECASE)
                # if patt != None: # and value==pagefonts_mode:
                    # print("*** Start:  key_value:" + key +"_"+ str(value))
                    find_title = True
                    font_title = value
                    font_sizes.append(tuple([key, value]))
                    result_lines.append(tuple([key, value, 0]))
                    continue
            if find_title==True:
                num_SpacesByWord = key.count(' ')
                if num_SpacesByWord >= len(key)/3 :
                    # print("space ..." + str(num_SpacesByWord) + " - " + str(line) + " - " + str(len(key)/2))
                    key_spaces = key.replace(' ', '')
                    font_sizes.append(tuple([key_spaces, value]))
                    result_lines.append(tuple([key_spaces, value, 0]))
                else:
                    font_sizes.append(tuple([key, value]))
                    result_lines.append(tuple([key, value, 0]))
        
        font_max, font_submax = getMaxSubmax(font_sizes, font_title)
        # print("Font_max 2: "+ str(font_max) + " - Submax: " + str(font_submax))
    
    # print("\n Result Lines")
    # for item in result_lines:
    #     print(item)

    if len(result_lines)>0 :
        for key, value, _ in result_lines:
            patt = None
            # if len(key)>1 and (value == font_max or value == font_submax):
            for pattern in PATTERN[limit1:limit1+limit2]:
                patt = re.search(rf"{pattern}", key)
                if patt != None and len(result_text)>50:
                    # print("*** End1: " + str(patt) + "  - key_value:" + key +"_"+ str(value))
                    patt_band1=True; break
            if patt_band1:
                result_page = True
                break
            if patt_band1==False:
                for pattern in PATTERN[limit1+limit2:]:
                    patt = re.search(rf"{pattern}", key, re.IGNORECASE)
                    # print("pattern: "+ pattern + "  key: " + key[0:35])
                    if patt != None and len(result_text)>50:
                        # print("*** End2: " + str(patt) + "  - key_value:" + key +"_"+ str(value))
                        patt_band2=True; break
                if patt_band2:
                    result_page = True
                    break
            if patt_band1 == False and patt_band2 == False:
                if len(key)>1 and (value == font_max or value == font_submax):
                    result_text = result_text + key
                # if value > font_max and len(key)>3:
                #     break

    return result_text, result_page, font_max, font_submax


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
    # print(text_page)

    for pattern in PATTERN[:limit]:
        patt = re.search(rf"{pattern}", text_page)
        # print("__ PATTERN: " + str(patt) + " - pattern: " + pattern)
        if patt != None :
            # print("PATTERN: " + str(patt) ) 
            methodology_title = pattern
            break
    
    return methodology_title

def getData_TitleMethodology_(pagelines_list, PATTERN, limit, font_max) :
    methodology_title = ""
    methodology_pos = 0
    patt_band = False
    
    for key, value, line in pagelines_list:
        for pattern in PATTERN[:limit]:
            patt = re.search(rf"\b{pattern}\b", key)
            # print("____patt: " + str(pattern) + " - " + key[:30] + " - " + str(value))
            if patt != None and value == font_max:
                # print("__TITLE FOUND: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
                methodology_title = pattern
                methodology_pos = line
                patt_band=True; break
        if patt_band:
            # methodology_title = pattern
            break
    
    return methodology_title, methodology_pos

def getData_ResultMethodology(pagelines_list, methodology_pos, PATTERN, limit, band, font_max_, font_submax_, font_lastmax_):
    result_text = ""
    result_page = False
    find_title = False
    patt_band = False
    font_sizes = []
    font_i = 0
    font_max = 0
    font_submax = 0
    font_lastmax = 0
    result_lines = []
    font_values = []
    font_title = font_max_

    # print("\n Result LIST")
    # for item in pagelines_list:
    #     print(item)

    if band == False : 
        result_lines = pagelines_list; font_max = font_max_; font_submax = font_submax_; font_lastmax = font_lastmax_
        for key,value,_ in pagelines_list:
            font_values.append(value)
    else :
        for key,value,line in pagelines_list:
            if find_title == False:
                if line == methodology_pos :
                # patt = re.search(rf"{methodology_title}", key)
                # print("\n___PREV patt: " + str(patt) + "  - key_value:" + key +" _ "+ str(value))
                # if (patt != None): # and value==intro_font) or (patt != None and value==introduction_mode):
                    # print("\n___Start patt: Key_value: " + key +" _ "+ str(value))
                    # print("\n Key: " + key + " _ Value: " + str(value))
                    find_title = True
                    font_title = value
                    # print("Title Value: " + str(value))
                    font_sizes.append(tuple([key, value]))
                    font_values.append(value)
                    result_lines.append(tuple([key, value, font_i]))
                    font_i += 1
                    continue
            if find_title==True:
                num_SpacesByWord = key.count(' ')
                if num_SpacesByWord >= len(key)/3 :
                    # print("space ..." + str(num_SpacesByWord) + " - " + str(line) + " - " + str(len(key)/2))
                    key_spaces = key.replace(' ', '')
                    font_sizes.append(tuple([key_spaces, value]))
                    result_lines.append(tuple([key_spaces, value, 0]))
                else:
                    font_sizes.append(tuple([key, value]))
                    result_lines.append(tuple([key, value, 0]))

                font_values.append(value)
                font_i += 1
                # if value==font_title:
                #     result_lines.append(tuple([key, value, 0]))
        
        font_max, font_submax = getMaxSubmax(font_sizes, font_title)

    # print("font_max: "+ str(font_max))
    # print("font_submax: "+ str(font_submax))
    # print("font_lastmax: "+ str(font_lastmax))
    # print("\n Result Lines")
    # for item in result_lines:
    #     print(item)

    if len(result_lines)>0 :
        for key, value, fi in result_lines:
            # if len(font_sizes)>2 :
            if fi == 1 and font_lastmax == 0 and len(font_values)>2 :
                if font_values[fi-1] == font_max and font_values[fi+1] == font_submax :
                    font_lastmax = value

        for key, value, fi in result_lines:
            for pattern in PATTERN[limit:]:
                patt = re.search(rf"\b{pattern}\b", key)
                # print("\n___POST patt: " + str(pattern) + " _ "+ str(value))
                if patt != None : #and value >= font_submax and value <= font_max : # or (patt != None and value==introduction_mode):
                    # print("\n___End patt: " + str(patt) + "  ... key_value: " + key +" _ "+ str(value))
                    patt_band=True; break
            if patt_band:
                result_page = True
                break
            else:
                # if len(key)>2 and ((value == font_max or value == font_submax) or (font_lastmax>0 and value==font_lastmax) or (font_lastmax>0 and value<=font_max)):  # ///////////////////////////////////////////////////////////
                if len(key)>1 and (value<=font_max and value>font_submax*0.8):
                    result_text = result_text + key
                if value > font_max and len(key)>3:
                    break
            # elif value == font_title : # or value==introduction_mode:
            #     result_text = result_text + key

    return result_text, result_page, font_max, font_submax, font_lastmax

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
    if language == "en" :
        patterns = patterns_en
        patterns_level = patterns_level_en
        patterns_approach = patterns_approach_en
        lib_spacy = "xx_ent_wiki_sm"; #from spacy.lang.es.stop_words import STOP_WORDS
    else :
        patterns = patterns_es
        patterns_level = patterns_level_es
        patterns_approach = patterns_approach_es
        lib_spacy = "es_core_news_sm"; #from spacy.lang.en.stop_words import STOP_WORDS

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