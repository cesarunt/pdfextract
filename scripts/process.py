import os, re
import datetime
import numpy as np
import spacy
from scipy import stats as s
from bs4 import BeautifulSoup as soup
from sqlalchemy import true
from utils.process_pdf import *
from utils.process_data import *
from utils.sqlite_tools import *
from utils.config import PATTERN_METHOD_EN, cfg

def clear_report(files_output):
    open(files_output+"/background.txt", "w").close()

def addText_background(type, line):
    if line != "":
        text_pdf.append(tuple([type, line]))

def addText_view(line, att_id, page):
    try:    
        _ = put_newPDFdetail(pdf_id, att_id, line, page)
    except:
        print("Error en registro del PDF details")

def removeAuthorsDuplicates(lst):
    return [t for t in (set(tuple(i) for i in lst))]

def pdf_process(files_split, files_output, pdf_info_id, pdfs):
    # clear_report(files_output)
    fname = os.listdir(files_split+"/")
    fname.sort(key=lambda f: int(re.sub('\D', '', f)))
    length = len(fname)

    global text_pdf
    global pdf_id
    global attributes

    attributes = []
    pdf_id = pdf_info_id
    text_pdf = []
    is_article = True

    page = 0
    language = "es"
    language_band = False
    text_page = ""

    # Title
    title_font = 7
    title_font_last = 10
    title_font_max = 33
    title_text = ""
    title_ctrl = False
    title_band = False

    # Authors
    authors_list = []
    authors_name = []
    authors_text = ""
    authors_band = False
    # Resumen
    resumen_font = 0
    resumen_title = ""
    resumen_text = ""
    resumen_res = False
    resumen_band = False

    font_max = 0

    # Introduction
    intro_font = 0

    # Methodology
    methodology_text = ""
    methodology_title = ""
    methodology_band = False
    
    # Article
    article_band = False
    doi_band = False
    URL_band = False
    year = 0                # 03. FIND THE PUBLISHING YEAR
    year_band = False
    objective = ""          # 04. FIND THE PATTERN OBJECTIVE
    objective_band = False
    design = ""             #  -. FIND THE PATTERN DESIGN
    design_band = False
    approach = ""           #  -. FIND THE PATTERN APPROACH
    approach_band = False
    samples = ""            # 06. FIND THE PATTERN SAMPLES
    samples_band = False
    tools_text = ""
    tools_band = False
    result_text = ""
    result_band = False
    result_title = ""

    # Conslusion
    conclusion_text = ""
    conclusion_band = False
    conclusion_title = ""

    result_res = False
    listQuan = []
    listQual = []
    pagelines_list = []

    # PATTERN_OBJE = []
    level_appl = False; level_pred = False; level_expi = False; level_rela = False; level_desc = False; level_expo = False

    if length > 50 :
        is_article = False
    else:
        if len(pdfs)>0:
            list_pages = pdfs[str(pdf_id)]
            length = len(list_pages)
        else:
            list_pages = range(length)

        # print(list_pages)
        np = 0
        for page in list_pages: #Repeat each operation for each document.
            print("\n\nPage 0"+str(int(page+1)) +": "+fname[page])

            # 1. EXTRACT ALL TEXT PAGE
            # ============================================================================================
            # - Extract text with functions PDFminer
            text_page = convert_pdf_to_text((files_split+'/{}').format(fname[page])) #Extract text with PDF_to_text Function call
            text_html = convert_pdf_to_html((files_split+'/{}').format(fname[page])) #Extract text with PDF_to_html Function call
            # text_html_out = text_html.decode("utf-8")     #Decode result from bytes to text
            # print(text_html)
            # 2. GET THE LANGUAGE
            # ============================================================================================

            if language_band == False:
                if page == 0:
                    language = lang_getLanguage(text_page)
                    print("Language ...", language)
                    language_band = True

                lib_spacy, patterns, patterns_level, patterns_approach = lang_loadPatterns(language)
                BLOCK_WORDS, BLOCK_AUTHOR, PATTERN_RESUM, PATTERN_INTRO, PATTERN_ABST, PATTERN_METHOD, PATTERN_ARTI, PATTERN_OBJE, PATTERN_METH, PATTERN_TYPE, PATTERN_DESI, PATTERN_APPR, PATTERN_LEVE, PATTERN_SAMP, PATTERN_TOOL, PATTERN_RESU, PATTERN_CONC = patterns
                PATTERN_LEVE_APPL, PATTERN_LEVE_PRED, PATTERN_LEVE_EXPI, PATTERN_LEVE_RELA, PATTERN_LEVE_DESC, PATTERN_LEVE_EXPO = patterns_level
                PATTERN_APPR_QUAN, PATTERN_APPR_QUAL = patterns_approach      
                NLP = spacy.load(lib_spacy)

            # 3. FIND THE TITLE TEXT
            # ============================================================================================
            if text_page != ""  and page == 0:
                # - Using BeautifulSoup to parse the text
                page_soup = soup(text_html, 'html.parser')
                patt = re.compile("font-size:(\d+)")
                text_parser = [(tag.text.strip(), int(patt.search(tag["style"]).group(1))) for tag in page_soup.select("[style*=font-size]")]

                # title_font_max  = max(text_parser, key=lambda x:x[1] )[1] 
                title_font_max = title_font
                patt_band = False
                patt_num = 0
                band_autor = False
                title_text_line = []
                pagelong_item = []      # longitud del item para obtener el texto resumen mas exacto
                pagefonts_list = []
                pageresum_list = []
                authors_list = []
                last_value = 0
                last_key = " "
                line = 0
                text_key = ""
                key_on = ""
                
                for key,value in text_parser :
                    num_SpacesByWord = key.count(' ')
                    if num_SpacesByWord >= len(key)/3 :
                        key_on = key.replace(' ', '')
                    else:
                        key_on = key
                    
                    if resumen_font == 0 : 
                        for item in PATTERN_RESUM :
                            patt = re.search(rf"\b{item}\b", key_on)
                            if patt != None :
                                resumen_font = value
                                # print("Resumen font: " + str(resumen_font))
                                break
                    if intro_font == 0 : 
                        for item in PATTERN_INTRO :
                            patt = re.search(rf"\b{item}\b", key_on)
                            if patt != None :
                                intro_font = value
                                # print("\nIntroducción font: " + str(intro_font))
                                break
                    if value > 0 :
                        pageresum_list.append(value)
                        if last_value > 0 :
                            pagelines_list.append(tuple([last_key, last_value, line]))
                            line = line + 1
                            pagefonts_list.append(value)
                            pagelong_item.append(len(last_key))
                            if last_value > title_font_max and len(last_key.split(" "))>5 :
                                title_font_max = last_value
                            text_key = ""
                        text_key = text_key + key_on
                    if value == 0 :
                        text_key = text_key + " "
                    last_value = value
                    last_key = text_key

                if last_key!="" and last_value>0:
                    pagelines_list.append(tuple([last_key, last_value, line]))
                    line += 1
                    pagefonts_list.append(last_value)

                if title_font_max > title_font and title_font_max <= 40:
                    title_font = title_font_max
                    title_text_list = []
                    title_text_list = [key for key, value in text_parser if value == title_font]
                    title_text_line = [line for key, value, line in pagelines_list if value == title_font]
                    title_text = (' '.join(title_text_list))
                    title_ctrl = True
                if len(title_text_line)==0: title_text_line=[1]

                if (authors_text == "" and language != "" and title_ctrl == True) or (authors_text!="" and title_font>title_font_last) :
                    title_font_last = title_font
                    
                    patt_band = False
                    patt_i = 0
                    for key,value,line in pagelines_list :
                        if band_autor == False:
                            for pattern in ['Autor', 'Autores']:
                                patt = re.search(rf"\b{pattern}", key, re.IGNORECASE)
                                if patt != None :
                                    patt_band = True
                                    break    
                            if patt_band :
                                band_autor = True
                                if str(patt.group(0)) == 'AUTOR':   patt_num = 1
                                else:   patt_num = 2
                                continue
                        
                        if band_autor and len(key)>1:
                            patt_i += 1
                            authors_list.append(tuple([key, value]))
                            if patt_i >= patt_num :
                                authors_name.append(key)
                                authors_text += key + ", "
                                break
                    
                    patt_band = False
                    if len(authors_list) == 0 :
                        for key,value,line in pagelines_list :
                            # get MAX value for title font
                            if line > title_text_line[0]:
                                for word_block in BLOCK_WORDS :
                                    wordl_patt = re.search(rf"{word_block}", key, re.IGNORECASE)
                                    if wordl_patt != None : patt_band=True; break
                                if patt_band : break
                                else: authors_list.append(tuple([key, value]))

                        if len(authors_list) > 0 and title_text != "":
                            # 1er recorrido authors_list, para actualizar lista con "\n"
                            for key, value in authors_list :
                                if len(key)>1 :
                                    key_name = key.split("\n")
                                    if len(key_name) > 1 :
                                        authors_list.remove(tuple([key, value]))
                                        for key_split in key_name:
                                            # Validar si ya existe
                                            authors_list.insert(len(authors_list)-1, tuple([key_split, value]))
                            # 2do recorrido authors_list, para actualizar lista con ", "
                            for key, value in authors_list :
                                if len(key)>1 :
                                    key_name = key.split(",")
                                    if len(key_name)>1:
                                        authors_list.remove(tuple([key, value]))
                                        for key_split in key_name:
                                            # Validar si ya existe
                                            authors_list.insert(len(authors_list)-1, tuple([key_split, value]))

                            # 3er recorrido authors_list, para obtener la lista final de __authors_name
                            for key, value in authors_list :
                                if len(key)>1 :
                                    # print("\nKey: " + key + " - Value: " + str(value))
                                    for auth_block in BLOCK_AUTHOR :
                                        auth_patt = re.search(rf"{auth_block}", key, re.IGNORECASE)
                                        if auth_patt != None : patt_band=True; break
                                    if patt_band or len(key)<=1 : patt_band=False; continue
                                    text_nlp = NLP(key)
                                    for word in text_nlp.ents:
                                        if word.label_ == "PER" :
                                            authors_name.append(key)
                                            authors_text += key + ", "

                # AUTORES (ANTECEDENTES) ............
                if objective == "":     objective = getData_LongText(resumen_text, PATTERN_OBJE, 'E', '. ')
                if objective == "":     objective = getData_LongText(text_page, PATTERN_OBJE, 'E', '. ')
                # -----------

                # Getting Article
                if article_band == False:  article_band, article_text = getData_ResultArticle(text_page, PATTERN_ARTI)

                # Getting DOI
                if doi_band == False:      doi_band, doi_text = getData_ResultDOI(text_page, cfg.LIST.PATTERN_DOI_XX)
                if doi_band == False and URL_band == False: URL_band, URL_text = getData_ResultURL(text_page, ['http'])

                # GETTING YEAR IS OK +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
                if year == 0 or year < 1000:
                    list_year = re.findall("(\d{4})",text_page)
                    year_max = 0
                    date = datetime.date.today()
                    for year in list_year :
                        year = int(year)
                        if year>year_max and year<=date.year :
                            year_max = year
                    year = year_max
            
            # 4. GET THE RESUME TEXT
            # ============================================================================================
            if resumen_title=="" and len(pagelines_list)>0:
                resumen_title, resumen_pos = getData_TitleResumen(pagelines_list, PATTERN_ABST, 6, 3, resumen_font)
                # print("\nResumen Title: \n" + resumen_title)
            if resumen_title != "" :
                if resumen_text == "" :
                    resumen_text, resumen_res, font_max, font_submax = getData_ResultResumen(pagelines_list, resumen_pos, PATTERN_ABST, 9, 5, True, 0, 0)
                    # print("RES Resumen "+ str(resumen_res))
                elif resumen_res == False :
                    resumen_text_, resumen_res, _, _ = getData_ResultResumen(pagelines_list, resumen_pos, PATTERN_ABST, 9, 5, resumen_res, font_max, font_submax)
                    if resumen_text_ != "" :
                        resumen_text = resumen_text + resumen_text_
                if resumen_res :
                    resumen_text_list = resumen_text.split("\n")
                    for item in resumen_text_list:
                        if item.isdigit() or len(item)<=1: resumen_text_list.remove(item)
                    resumen_text = str(' '.join(resumen_text_list))
                    resumen_text = resumen_text.replace("\n", " ")
            
            # print("TITLE TEXT")
            # print(title_text)
            if (title_text!="" or resumen_text != "" or authors_text!= "") and page > 0:
                print("... enter title_text")
                # 5. GET THE METHODOLOGY TEXT
                # ============================================================================================
                # finding the title of methodology using PATTERN_METHOD
                # print("\nMetodo Title : " + methodology_title)
                if methodology_title=="":
                    methodology_title, methodology_pos = getData_TitleResumen_(pagelines_list, PATTERN_METHOD, 10, 10, intro_font)
                    # print("\nMethodology Title: " + methodology_title + "  _ Mode: " + str(pagefonts_mode))
                if methodology_title != "":
                    # Desde este punto (pagina) comienza el texto para la sección de methodología
                    if methodology_text == "" :
                        methodology_text, methodology_res, font_max, font_submax, font_lastmax = getData_ResultMethodology(pagelines_list, methodology_pos, PATTERN_METHOD, 20, True, 0, 0, 0)
                        # print("\nmethodology_res .... " + str(methodology_res))
                    elif methodology_res == False :
                        methodology_text_, methodology_res, _, _, _ = getData_ResultMethodology(pagelines_list, methodology_pos, PATTERN_METHOD, 20, methodology_res, font_max, font_submax, font_lastmax)
                        if methodology_text_ != "" :
                            methodology_text = methodology_text + methodology_text_
                        # else :
                        #     methodology_text = ""
                    if methodology_res :
                        methodology_text_list = methodology_text.split("\n")
                        for item in methodology_text_list:
                            if item.isdigit() or len(item)<=1: methodology_text_list.remove(item)
                        methodology_text = str(''.join(methodology_text_list))
                        methodology_text = methodology_text.replace("\n", " ")

                    # if type_level == "" :   type_level  = getData_LongText(methodology_text, PATTERN_TYPE, 'S', ', ')
                    if design == "" :       design     = getData_LongText(methodology_text, PATTERN_DESI, 'S', ', ')
                    if approach == "" :     approach  = getData_LongText(methodology_text, PATTERN_APPR, 'S', '. ')
                    # - getting 2 approach
                    # if approach_quan == False : approach_quan = getTools_ResultCount(text_method, PATTERN_APPR_QUAN)
                    listQn = getTools_ResultCount(methodology_text, PATTERN_APPR_QUAN)
                    if len(listQn) > 0 :  listQuan = listQuan + listQn
                    listQl = getTools_ResultCount(methodology_text, PATTERN_APPR_QUAL)
                    if len(listQl) > 0 :  listQual = listQual + listQl
                    if len(listQuan) > 0 :
                        tools_text = tools_text + "Cuantitativos: " + str(listQuan)
                    if len(listQual) > 0 : 
                        tools_text = tools_text + ", Cualitativos: " + str(listQual)
                    # - getting 5 levels
                    # if level_appl == False :    level_appl = getLevel_Result(methodology_text, PATTERN_LEVE_APPL)
                    # if level_pred == False :    level_pred = getLevel_Result(methodology_text, PATTERN_LEVE_PRED)
                    # if level_expi == False :    level_expi = getLevel_Result(methodology_text, PATTERN_LEVE_EXPI)
                    # if level_rela == False :    level_rela = getLevel_Result(methodology_text, PATTERN_LEVE_RELA)
                    # if level_desc == False :    level_desc = getLevel_Result(methodology_text, PATTERN_LEVE_DESC)
                    # if level_expo == False :    level_expo = getLevel_Result(methodology_text, PATTERN_LEVE_EXPO)

                    if samples == "":     samples = getData_LongText(methodology_text, PATTERN_SAMP, 'E', '. ')
                    if samples == "":     samples = getData_LongText(resumen_text, PATTERN_SAMP, 'E', '. ')
               
                # 6. GET THE RESULT TEXT
                # ============================================================================================
                # finding the title of methodology using PATTERN_RESU
                if result_title=="":
                    # print("\nIntro: " + str(intro_font))
                    result_title, result_pos = getData_TitleResumen_(pagelines_list, PATTERN_RESU, 4, 4, intro_font)
                    # print("\nResult Title:" + result_title + " mode:" + str(pagefonts_mode))
                if result_title != "":
                    # Desde este punto (pagina) comienza el texto para la sección de resultados
                    if result_text == "" :
                        result_text, result_res, font_max, font_submax, font_lastmax = getData_ResultMethodology(pagelines_list, result_pos, PATTERN_RESU, 8, True, 0, 0, 0)
                    elif result_res == False :
                        result_text_, result_res, _, _, _ = getData_ResultMethodology(pagelines_list, result_pos, PATTERN_RESU, 8, result_res, font_max, font_submax, font_lastmax)
                        if result_text_!= "" :
                            result_text = result_text + result_text_
                        # else :
                        #     result_text = ""
                    if result_res :
                        result_text = result_text.replace(".\n\n", "._")
                        result_text_list = result_text.split("\n\n")
                        for item in result_text_list:
                            if item.isdigit() or len(item)<=1: result_text_list.remove(item)
                        result_text = str(' '.join(result_text_list))
                        result_text = result_text.replace("\n", "")
                        result_text = result_text.replace("._", ".\n\n")
                    
                # 7. GET THE CONCLUSION TEXT
                # ============================================================================================
                # finding the title of methodology using PATTERN_METHOD
                if conclusion_title=="":
                    conclusion_title, conclusion_pos = getData_TitleResumen_(pagelines_list, PATTERN_CONC, 9, 9, intro_font)
                    # print("\nConclusions Title:" + conclusion_title)
                if conclusion_title != "":
                    # Desde este punto (pagina) comienza el texto para la sección de conclusiones
                    if conclusion_text == "" :
                        conclusion_text, conclusion_res, font_max, font_submax, font_lastmax  = getData_ResultMethodology(pagelines_list, conclusion_pos, PATTERN_CONC, 18, True, 0, 0, 0)
                    elif conclusion_res == False :
                        conclusion_text_, conclusion_res, _, _, _ = getData_ResultMethodology(pagelines_list, conclusion_pos, PATTERN_CONC, 18, conclusion_res, font_max, font_submax, font_lastmax)
                        if conclusion_text_!= "" :
                            conclusion_text = conclusion_text + conclusion_text_
                        # else :
                            # conclusion_text = ""
                    if conclusion_res :                  
                        conclusion_text = conclusion_text.replace(".\n\n", "._")
                        conclusion_text_list = conclusion_text.split("\n\n")
                        for item in conclusion_text_list:
                            if item.isdigit() or len(item)<=1: conclusion_text_list.remove(item)
                        conclusion_text = str(' '.join(conclusion_text_list))
                        conclusion_text = conclusion_text.replace("\n", "")
                        conclusion_text = conclusion_text.replace("._", ".\n\n")

            if authors_text and authors_band == False:
                addText_view(authors_text, 1, page+1)
                authors_band = True
            if title_text and title_band == False:
                addText_view(title_text, 2, page+1)
                title_band = True
            if year and year_band == False:
                addText_view(year, 3, page+1)
                year_band = True
            if objective and objective_band == False:
                addText_view(objective, 4, page+1)
                objective_band = True
            if resumen_text and resumen_band == False:
                addText_view(resumen_text, 5, page+1)
                resumen_band = True
            if len(methodology_text)>0 and methodology_band == False:
                addText_view(methodology_text, 6, page+1)
                methodology_band = True
            if approach and approach_band == False:
                addText_view(approach, 7, page+1)
                approach_band = True
            if design and design_band == False:
                addText_view(design, 8, page+1)
                design_band = True
            if len(samples)>0 and samples_band == False:
                addText_view(samples, 9, page+1)
                samples_band = True
            if tools_text and tools_band == False:
                addText_view(tools_text, 10, page+1)
                tools_band = True
            if len(result_text)>0 and result_band == False:
                addText_view(result_text, 11, page+1)
                result_band = True
            if len(conclusion_text)>0 and conclusion_band == False:
                addText_view(conclusion_text, 12, page+1)
                conclusion_band = True

            if title_ctrl == True and title_text!="" and np == length-1 :
                if authors_band == False:
                    addText_view(authors_text, 1, 1)
                if title_band == False:
                    addText_view(title_text, 2, 1)
                if year_band == False:
                    addText_view(year, 3, 1)
                if objective_band == False:
                    addText_view(objective, 4, 1)
                if resumen_band == False:
                    addText_view(resumen_text, 5, 1)
                if methodology_band == False:
                    addText_view(methodology_text, 6, 1)
                if approach_band == False:
                    addText_view(approach, 7, 1)
                if design_band == False:
                    addText_view(design, 8, 1)
                if samples_band == False:
                    addText_view(samples, 9, 1)
                if tools_band == False:
                    addText_view(tools_text, 10, 1)
                if result_band == False:
                    addText_view(result_text, 11, page-1)
                if conclusion_band == False:
                    addText_view(conclusion_text, 12, page)
                
                # RESUMEN ...........
                resumen_text_list = resumen_text.split("\n")
                for item in resumen_text_list :
                    if 'ISSN' in item or 'http' in item : resumen_text_list.remove(item)
                resumen_text_list = [x for x in resumen_text_list if x]

                # print("\nRESUMEN")
                # print(resumen_text_list)
                resumen_text = (' '.join(resumen_text_list))

                addText_background("B", "\nRESUMEN")
                resumen_text = resumen_text.replace("\n\n", "#")
                resumen_text = resumen_text.replace("\n", " ")
                resumen_text = resumen_text.replace("#", "\n\n")
                addText_background("N", resumen_text)
                
                # print("AUTORES ...")
                # print(type(authors_text))
                # print("\n01._ AUTHORs NAME \n" + authors_text)
                # print("\n02._ PUBLISHING YEAR: " + str(year))
                # print("\n03._ TITLE TEXT (" + str(title_font)+"px):\n" + title_text)
                article_print = ""
                if article_band : article_print = "Revista"
                # print("\n04._ ARTICLE TEXT: " + article_text)
                addText_background("B", "\nANTECEDENTES") 
                addText_background("N", authors_text  + ' ('+str(year)+') en su estudio titulado "' + title_text.replace('\n', ' ') + '". (Articulo cientifico - '+ article_print +'). Objetivo:' + objective)

                # METODOLOGIA ................
                addText_background("B", "\nMETODOLOGIA")

                if methodology_text=="":
                    addText_background("N", "No existe información específica sobre Metodología o Métodos.")
                else:
                    addText_background("N", methodology_text)
                    
                    # Metodologia detalles
                    methodology_det = ""
                    # print("\n  6.1._ APPROACH DETAILS : ", end="")
                    listQuan = list(dict.fromkeys(listQuan))
                    if len(listQuan) > 0 :
                        methodology_det = methodology_det + "Cuantitativo, "
                        # print("Cuantitativo", end=", ")
                    listQual = list(dict.fromkeys(listQual))
                    if listQual : 
                        methodology_det = methodology_det + "Cualitativo, "
                        # print("Cualitativo", end="")
                    # print("\n\n  6.1_ LEVEL DETAILS: ", end="")
                    # methodology_det += methodology_det + "\n"
                    # if level_appl : methodology_det += methodology_det + "Aplicado, ";     print("Aplicado", end=", ")
                    # if level_pred : methodology_det += methodology_det + "Predictivo, ";   print("Predictivo", end=", ")
                    # if level_expi : methodology_det += methodology_det + "Explicativo, ";  print("Explicativo", end=", ")
                    # if level_rela : methodology_det += methodology_det + "Relacional, ";   print("Relacional", end=", ")
                    # if level_desc : methodology_det += methodology_det + "Descriptivo, ";  print("Descriptivo", end=", ")
                    # if level_expo : methodology_det += methodology_det + "Exploratorio";   print("Exploratorio", end="")
                    # addText_background("N", "Metodología Detalles:\n" + methodology_det, page)
                
                addText_background("N", "Muestra: ")
                addText_background("N", samples)

                addText_background("B", "\nRESULTADOS")
                result_text = list(filter(lambda x : x != '', result_text.split('\n\n')))
                # result_text = result_text.replace("\n", "")
                # result_text = result_text.replace(".  ", ".\n\n")
                if result_text=="":
                    addText_background("N", "No existe información específica sobre Resultados.")
                else:
                    addText_background("N", result_text)
                    
                addText_background("B", "\nCONCLUSIONES")
                if conclusion_text=="":
                    addText_background("N", "No existe información específica sobre Conclusiones.")
                else:
                    addText_background("N", conclusion_text)
                
                # Create the REFERENCE
                # doi_print = ""
                # if doi_band :   doi_print = doi_text
                # elif URL_band : doi_print = 'Obtenido de: ' + URL_text
                # reference_text = authors_text + ' ('+str(year)+'). ' + title_text.capitalize().replace('\n', ' ') + '. ' + article_text + '. ' + doi_print
                # addText_background("B", '\nREFERENCIAS')
                # addText_background("N", reference_text)
                # print('text_pdf', text_pdf)
            
            np += 1

    
    return is_article, text_pdf, language, title_text