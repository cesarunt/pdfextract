import os, re
import datetime
import spacy
from bs4 import BeautifulSoup
# from textblob import TextBlob
from utils.config import cfg
from utils.process_pdf import *
from utils.process_data import *

# GLOBAL VARIABLES
# -----------------
page = 0
font_max = 30
font_current = 10
language = ""
band_title = False   # variable to stop data searching
BLOCK_WORDS = []

text_page = ""                  # 0. PDF INFORMATION
title_text = ""                 # 1. FIND DE TITLE TEXT
authors_name  = []              # 2. FIND THE AUTHOR NAME
year = ""                       # 3. FIND THE PUBLISHING YEAR
objective = ""                  # 4. FIND THE PATTERN OBJECTIVE
band_method = False
method = ""                     # 5-8. FIND THE METHODOLOGY 
# type = ""                     # 5. FIND THE PATTERN TYPE 
design = ""                     # 6. FIND THE PATTERN DESIGN
approach = ""                   # 7. FIND THE PATTERN APPROACH
approach_quan = False; approach_qual = False
level = ""                      # 8. FIND THE PATTERN LEVEL
level_appl = False; level_pred = False; level_expi = False; level_rela = False; level_desc = False; level_expo = False
sample = ""                     # 9. FIND THE PATTERN SAMPLE
# tools = ""                      # 10. FIND THE PATTERN TOOLS

if __name__ == "__main__":
    clear_text_save()
    fname = os.listdir('split/') #fname : List contain pdf documents names.
    #fname: must be sorted.
    fname.sort(key=lambda f: int(re.sub('\D', '', f)))
    length = len(fname)
    print("\n------------------ START PROCESS ------------------")
    print("Num docs: ", length)

for page in range(length): #Repeat each operation for each document.
    print("Page 0"+str(int(page+1)) +": "+fname[page])

    # 1. FIND THE TITLE TEXT
    # ============================================================================================
    # - Extract text with functions PDFminer
    text_page = convert_pdf_to_text(('split/{}').format(fname[page])) #Extract text with PDF_to_text Function call
    text_html = convert_pdf_to_html(('split/{}').format(fname[page])) #Extract text with PDF_to_text Function call
    # text_output = text_html.decode("utf-8")     #Decode result from bytes to text
    # print(text_page)

    if text_page != "" and band_title == False:
        # - Using BeautifulSoup to parse the text
        soup = BeautifulSoup(text_html, 'html.parser')
        patt = re.compile("font-size:(\d+)")
        text_parser = [(tag.text.strip(), int(patt.search(tag["style"]).group(1))) for tag in soup.select("[style*=font-size]")] 
        # - Getting the max value of the font
        title_font  = max(text_parser, key=lambda x:x[1])[1]
        title_list_text = []
        if (title_font==55) : title_font=15
        title_list_text = [key for key, value in text_parser if value == title_font]
        title_text =(''.join(title_list_text))
        # - Validate the font and text from the title
        if title_font > font_current and title_font < font_max and len(title_text) > 0:
            title_text =(' '.join(title_list_text)).split("___")[0]
            if "Resumen" in title_text :
                title_text =(' '.join(title_list_text)).split("Resumen")[0]
            band_title = True
     # - RESULT: "title_text"
     # ============================================================================================
     # 2. FIND THE AUTHOR NAME
     # ============================================================================================
        # - Getting the language of text
        if language == "" :
            # get the text's language and patterns for NLP
            language = lang_getLanguage(text_page)
            lib_spacy, STOP_WORDS, patterns, patterns_level, patterns_approach = lang_loadPatterns(language)
            BLOCK_WORDS, PATTERN_OBJE, PATTERN_METH, PATTERN_DESI, PATTERN_APPR, PATTERN_LEVE, PATTERN_SAMP = patterns
            PATTERN_LEVE_APPL, PATTERN_LEVE_PRED, PATTERN_LEVE_EXPI, PATTERN_LEVE_RELA, PATTERN_LEVE_DESC, PATTERN_LEVE_EXPO = patterns_level
            PATTERN_APPR_QUAN, PATTERN_APPR_QUAL = patterns_approach
                    
        NLP = spacy.load(lib_spacy)
        text_nlp = NLP(text_page)
        person_label = []
        person_tot = 0
        title_inc = 0
        title_tot = 0
        w = 0
        
        print("List Original NLP items : " + str(len(text_nlp.ents)))
        for word in text_nlp.ents:
            word_ = word.text.lower().split(" ")[0]
            if  word_ not in STOP_WORDS:
                word_formated  = format_word_dash(word.text)
                size_word = len(word_formated.split())
                # print(str(w)+" .-. "+str(size_word)+" .-. "+word_formated+"- "+word.label_)
                if len(word_formated) > 0 :
                    title_inc = find_word_in_title(word_formated, title_text)
                    # print(str(title_tot)+" .-. "+str(title_inc)+" .-. "+word_formated+"- "+word.label_) ##############
                    result = find_words_allowed(word_formated)
                    if result == True :
                        word_formated = clear_word(word_formated, BLOCK_WORDS)
                        authors_name.append(tuple([w, 0, word.label_, word_formated]))
                    else :
                        if title_inc == 1 :
                            title_tot += 1
                        if title_tot > 0 and title_inc==0 :
                            # if (word.label_ != "PER" and person_tot>0) or (word.label_ == "PER" and word_ in BLOCK_WORDS) :
                            if word_ in BLOCK_WORDS:
                                break
                            if (word.label_ == "PER" and size_word > 1) :
                                person_tot += 1
                                word_formated = clear_word(word_formated, BLOCK_WORDS)
                                authors_name.append(tuple([w, title_inc, word.label_, word_formated]))
                        if title_tot == 0 and title_inc == 0:
                            if (word.label_ != "PER" and person_tot>0) or (word.label_ == "PER" and word_ in BLOCK_WORDS):
                                # print("continue")
                                w += 1
                                continue
                            if (word.label_ == "PER" and size_word > 1 and len(word_)>2 and word_[0:4]!="http") :
                                # print("..............")
                                person_tot += 1
                                word_formated = clear_word(word_formated, BLOCK_WORDS)
                                authors_name.append(tuple([w, title_inc, word.label_, word_formated]))
                w += 1
     # - RESULT: "authors_name"
     # ============================================================================================
     # 3. FIND THE DOCUMENT PUBLISHING YEAR 
     # ============================================================================================
    # if text_page != "" :
        # - Getting the max year of PDF 1st page
        if band_title == True :
            list_year = re.findall("(\d{4})",text_page)
            year_max = 0
            date = datetime.date.today()
            for year in list_year :
                year = int(year)
                if year>year_max and year<=date.year :
                    year_max = year
            year = year_max
     # - RESULT: "year"
    # ============================================================================================    
    # FIND TEXT FROM PATTERNS
    # ============================================================================================
    # 4. FIND THE OBJECTIVE OR STUDY PURPOSE
    # ======================================
    # - Getting the objective
    if objective == "" :            objective = patt_getData_Long(text_page, PATTERN_OBJE)
    # 5-8 METHODOLOGY (type, design, approach, level)
    # - Getting the method
    if method == "" :               method    = patt_getData_Long(text_page, PATTERN_METH)
    # - Getting the method
    if patt_getData_Long(text_page, PATTERN_METH) != "" :
        band_method = True
    if band_method == True :
        # - Getting the type
        # if type == "" :             type      = patt_getData(text_page, PATTERN_TYPE)
        # - Getting the design
        if design == "" :           design        = patt_getData_Long(text_page, PATTERN_DESI)
        # - Getting the approach
        if approach == "" :         approach      = patt_getData_Long(text_page, PATTERN_APPR)
        if approach_quan == False : approach_quan = patt_getLevel_Short(text_page, PATTERN_APPR_QUAN)
        if approach_qual == False : approach_qual = patt_getLevel_Short(text_page, PATTERN_APPR_QUAL)
        # - getting 5 levels
        if level_appl == False :    level_appl = patt_getLevel_Short(text_page, PATTERN_LEVE_APPL)
        if level_pred == False :    level_pred = patt_getLevel_Short(text_page, PATTERN_LEVE_PRED)
        if level_expi == False :    level_expi = patt_getLevel_Short(text_page, PATTERN_LEVE_EXPI)
        if level_rela == False :    level_rela = patt_getLevel_Short(text_page, PATTERN_LEVE_RELA)
        if level_desc == False :    level_desc = patt_getLevel_Short(text_page, PATTERN_LEVE_DESC)
        if level_expo == False :    level_expo = patt_getLevel_Short(text_page, PATTERN_LEVE_EXPO)
    
        # - Getting the smaple
        if sample == "" :           sample    = patt_getData_Long(text_page, PATTERN_SAMP)

    # ============================================================================================
    if band_title == True and len(authors_name)>0 and year!="" and page == length-1 :
        print("------------------- END PROCESS -------------------")
        print("\n1._ TITLE TEXT (" + str(title_font)+"px):\n" + title_text)
        print("\n2._ AUTHOR NAME (" + str(len(authors_name))+ "):")
        for item in authors_name: print(item)
        print("\n3._ PUBLISHING YEAR: " + str(year))
        print("\n4._ OBJECTIVE :\n" + objective)
        print("\n5._ METHODOLOGY :\n" + method)
        # print("5._ TYPE :" + type)
        print("\n ._ DESIGN :" + design)
        print("\n 6_ APPROACH :", end=" ")
        if approach_quan : print("Quantitive", end=", ")
        if approach_qual : print("Qualitative")
        # if approach : print(approach)
        print("\n 7_ LEVEL : ", end="")
        if level_appl : print("Applied", end=", ")
        if level_pred : print("Predictivo", end=", ")
        if level_expi : print("Explicativo", end=", ")
        if level_rela : print("Relacional", end=", ")
        if level_desc : print("Descriptivo", end=", ")
        if level_expo : print("Exploratorio")
        print("\n8._ SAMPLE :\n" + sample)
        print("\n")
        # break
    
    # input("................... press enter ........................")