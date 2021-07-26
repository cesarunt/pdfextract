import os, re
import datetime
import spacy
from bs4 import BeautifulSoup
from utils.config import PATTERN_TYPE_EN, cfg
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
authors_name = []               # 2. FIND THE AUTHOR NAME
year = ""                       # 3. FIND THE PUBLISHING YEAR
band_objective = False
objective = ""                  # 4. FIND THE PATTERN OBJECTIVE
band_method = False
method = ""                     # 5-8. FIND THE METHODOLOGY 
type = ""                     # 5. FIND THE PATTERN TYPE 
design = ""                     # 6. FIND THE PATTERN DESIGN
approach = ""                   # 7. FIND THE PATTERN APPROACH
approach_quan = False; 
approach_qual = False
level = "Aplicado"                      # 8. FIND THE PATTERN LEVEL
level_appl = False; level_pred = False; level_expi = False; level_rela = False; level_desc = False; level_expo = False
samples = ""                    # 9. FIND THE PATTERN SAMPLES
tools = ""                      # 10. FIND THE PATTERN TOOLS
listQuan = []
listQual = []
band_result = False
results = ""                    # 11. FIND THE PATTERN RESULTS
conclusions = ""                # 12. FIND THE PATTERN CONCLUSIONS

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
    text_html = convert_pdf_to_html(('split/{}').format(fname[page])) #Extract text with PDF_to_html Function call
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
        title_text = (''.join(title_list_text)).replace("\n", "")
        if title_font > font_current and title_font < font_max and len(title_text) > 1:
            title_text = title_text.split("___")[0]
            # if "Resumen" in title_text :
                # title_text =(' '.join(title_list_text)).split("Resumen")[0]
            band_title = True
         # - RESULT: "title_text"
         # ============================================================================================
         # 2. FIND THE AUTHOR NAME
         # ============================================================================================
        if band_title == True :
            # - Getting the language of text
            if language == "" :
                # get the text's language and patterns for NLP
                language = lang_getLanguage(text_page)
                lib_spacy, STOP_WORDS, patterns, patterns_level, patterns_approach = lang_loadPatterns(language)
                BLOCK_WORDS, PATTERN_OBJE, PATTERN_METH, PATTERN_TYPE, PATTERN_DESI, PATTERN_APPR, PATTERN_LEVE, PATTERN_SAMP, PATTERN_TOOL, PATTERN_RESU, PATTERN_CONC = patterns
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
            # if band_title == True :
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
    
            if objective == "": objective = getData_LongText(text_page, PATTERN_OBJE, 'E', '. ')
            
    text_method = ""
    if text_page != "" and language!="" and band_method == False:
        method_res, method_pos       = getData_ResultText(text_page, PATTERN_METH)
        if method_res :
            band_method = True
            method_page = page + 1
            # print(text_page[method_pos:])
    
    result_res = False
    if text_page != "" and language!="" and band_method == True : 
        result_res, result_pos       = getData_ResultText(text_page, PATTERN_RESU)
        # print(result_res)
        if result_res == False :
            # text_method = text_page[method_pos:-1].replace("\n", " ")
            text_method = text_page[method_pos:-1]
        if result_res == True:
            result_page = page + 1
            band_result = True
            if method_page < result_page :
                # text_method = text_page[0:result_pos].replace("\n", "")
                text_method = text_page[0:result_pos]
            else :
                # text_method = text_page[method_pos:result_pos].replace("\n", " ")
                text_method = text_page[method_pos:result_pos]
            text_result = text_page[result_pos:]
            # print(text_result)
            
            # print(text_result)
        # print(text_method)
        # - Getting the methodology (method, design, approach, level)
        if method == "" :       method   = getData_LongText(text_method, PATTERN_METH, 'E', '.\n')
        if type == "" :         type     = getData_LongText(text_method, PATTERN_TYPE, 'S', ', ')
        if design == "" :       design   = getData_LongText(text_method, PATTERN_DESI, 'S', ', ')
        if approach == "" :     approach = getData_LongText(text_method, PATTERN_APPR, 'S', '. ')
        # - getting 2 approach
        # if approach_quan == False : approach_quan = getTools_ResultCount(text_method, PATTERN_APPR_QUAN)
        listQn = getTools_ResultCount(text_method, PATTERN_APPR_QUAN)
        if len(listQn) > 0 :  listQuan = listQuan + listQn
        listQl = getTools_ResultCount(text_method, PATTERN_APPR_QUAL)
        if len(listQl) > 0 :  listQual = listQual + listQl
        # if approach_qual == False : listQual = getTools_ResultCount(text_method, PATTERN_APPR_QUAL)
        # - getting 5 levels
        if level_appl == False :    level_appl = getLevel_Result(text_method, PATTERN_LEVE_APPL)
        if level_pred == False :    level_pred = getLevel_Result(text_method, PATTERN_LEVE_PRED)
        if level_expi == False :    level_expi = getLevel_Result(text_method, PATTERN_LEVE_EXPI)
        if level_rela == False :    level_rela = getLevel_Result(text_method, PATTERN_LEVE_RELA)
        if level_desc == False :    level_desc = getLevel_Result(text_method, PATTERN_LEVE_DESC)
        if level_expo == False :    level_expo = getLevel_Result(text_method, PATTERN_LEVE_EXPO)
        
        if text_page != "" and language!="" and tools == "":
            # - Getting the tools
            tools      = getData_Long(text_method, PATTERN_TOOL)

     ## LOS RESULTADOS SE DEBEN OBTENER DE LA MISMA FORMA QUE LA METODOLOGIA
        if text_page != "" and language!="" and band_result == True :
            result_res, result_pos       = getData_ResultText(text_result, PATTERN_RESU)
            # print(text_page[result_pos:])
            # - Getting the results
            if results == "" :
                results    = getData_LongText(text_result, PATTERN_RESU, 'E', '.\n')
                band_result = False

    if text_page != "" and language!="" and samples == "":
        # - Getting the samples
        samples    = getData_Long(text_page, PATTERN_SAMP)
    if text_page != "" and language!="" and conclusions == "":
        # - Getting the samples
        conclusions    = getData_LongText(text_page, PATTERN_CONC, 'E', '.\n')

    # ============================================================================================
    if band_title == True and len(authors_name)>0 and year!="" and page == length-1 :
        print("------------------- END PROCESS -------------------")
        print("\n01._ TITLE TEXT (" + str(title_font)+"px):\n" + title_text)
        print("\n02._ AUTHOR NAME (" + str(len(authors_name))+ "):")
        for item in authors_name: print(item)
        print("\n03._ PUBLISHING YEAR: " + str(year))
        print("\n04._ OBJECTIVE :\n" + objective)
        print("\n05._ METHODOLOGY :\n" + method, end="")
        method_list = {'type':'tipo', 'design':'diseño', 'approach':'enfoque'}
        mi = 1
        for key, value in method_list.items() : 
            if value in method or value.capitalize() in method  : print("\n   5."+str(mi)+"._ "+key.capitalize()+" : " + vars()[key]); mi += 1
            # vars()[item]
        # print("5._ TYPE :" + type) # LEVEL
        # print("\n 06._ DESIGN : " + design)
        print("\n06._ APPROACH DETAILS : ", end="")
        listQuan = list(dict.fromkeys(listQuan))
        if len(listQuan) > 0 : print("Cuantitativo", end=", ")
        listQual = list(dict.fromkeys(listQual))
        if listQual : print("Cualitativo", end="")
        # if approach : print(approach)
        print("\n\n07._ LEVEL DETAILS: ", end="")
        if level_appl : print("Aplicado", end=", ")
        if level_pred : print("Predictivo", end=", ")
        if level_expi : print("Explicativo", end=", ")
        if level_rela : print("Relacional", end=", ")
        if level_desc : print("Descriptivo", end=", ")
        if level_expo : print("Exploratorio", end="")
        print("\n\n08._ SAMPLES :\n" + samples)
        print("\n09._ TOOLS : Técnica(s) de recolección de datos empleada(s): ")
        if len(listQuan) > 0 : print("  " + str(listQuan))
        if len(listQual) > 0 : print("  " + str(listQual))
        print("\n10._ RESULTS :\n" + results)
        print("\n11._ CONCLUSIONS :\n" + conclusions)
        # break
    # input("................... press enter ........................")