from curses.ascii import isdigit
import os, re
import datetime
import spacy
# from scipy import stats as s
from bs4 import BeautifulSoup as soup
from sqlalchemy import true
from utils.process_pdf import *
from utils.process_data import *
from utils.sqlite_tools import *
from utils.config import PATTERN_METHOD_EN, cfg


def addText_view(value, att_id, page):
    try:
        _ = put_newPDFdetail(pdf_id, att_id, value, page, 1)
    except:
        print("Error en registro del PDF details")

def removeAuthorsDuplicates(lst):
    return [t for t in (set(tuple(i) for i in lst))]

def pdf_process(files_split, pdf_attributes, pdf_info_id, pdfs, pdf_npages, type_val):
    # clear_report(files_output)
    fname = os.listdir(files_split+"/")
    precedes = [x for x in fname if '.DS_Store' not in x]
    fname = sorted(precedes)
    length = len(fname)

    # global text_pdf
    global pdf_id
    global attributes

    pdf_id = pdf_info_id
    attributes = []

    page = 0
    language = "es"
    language_band = False
    text_page = ""

    # Title
    title_font = 7
    title_font_last = 10
    title_font_max = 30
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

    # Introduction
    intro_font = 0
    font_max = 0

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
    # OBJECTIVE PATTERN
    objective = ""
    objective_band = False
    typelevel = ""          #  -. FIND THE PATTERN TYPE
    typelevel_band = False
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
    conclusion_text = ""
    conclusion_band = False
    conclusion_title = ""
    result_res = False
    pagelines_list = []

    # PAPER PATTERN
    paper = ""
    paper_band = False
    # VOLUMEN PATTERN
    volume = ""
    volume_band = False
    # PAGE PATTERN
    pagem = ""
    pagem_band = False

    if len(pdfs)>0:
        list_pages = pdfs[str(pdf_id)]
        length = len(list_pages)
    else:
        list_pages = range(pdf_npages)
    
    np = 0
    key_att_ids = []
    for page in list_pages: #Repeat each operation for each document.
        # 1. EXTRACT ALL TEXT PAGE
        # ============================================================================================
        # - Extract text with functions PDFminer
        file_page = files_split+'/'+str(pdf_info_id)+'page'+'_{}.pdf'.format(page+1)
        text_page = convert_pdf_to_text(file_page) #Extract text with PDF_to_text Function call
        text_html = convert_pdf_to_html(file_page) #Extract text with PDF_to_html Function call
        # text_html_out = text_html.decode("utf-8")     #Decode result from bytes to text

        # 2. GET THE LANGUAGE
        # ============================================================================================
        if language_band == False:
            if page == 0:
                # language = lang_getLanguage(text_page)
                # print("Language ...", language)
                language = "es"
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

            title_font_max  = max(text_parser, key=lambda x:x[1] )[1] 
            # title_font_max = title_font
            # print("FONT_MAX", title_font_max)
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
                            break
                if intro_font == 0 : 
                    for item in PATTERN_INTRO :
                        patt = re.search(rf"\b{item}\b", key_on)
                        if patt != None :
                            intro_font = value
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

            if title_font_max > title_font and title_font_max <= 125:
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
        
        if (title_text!="" or resumen_text != "" or authors_text!= "") and page > 0:
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
                if methodology_res :
                    methodology_text_list = methodology_text.split("\n")
                    for item in methodology_text_list:
                        if item.isdigit() or len(item)<=1: methodology_text_list.remove(item)
                    methodology_text = str(''.join(methodology_text_list))
                    methodology_text = methodology_text.replace("\n", " ")

                if typelevel == "" :   typelevel  = getData_LongText(methodology_text, PATTERN_TYPE, 'S', ', ')
                if approach == "" :    approach  = getData_LongText(methodology_text, PATTERN_APPR, 'S', ', ')
                if design == "" :      design   = getData_LongText(methodology_text, PATTERN_DESI, 'S', ', ')

                if samples == "":     samples = getData_LongText(methodology_text, PATTERN_SAMP, 'E', '. ')
                if samples == "":     samples = getData_LongText(resumen_text, PATTERN_SAMP, 'E', '. ')
                if tools_text == "":  tools_text = getData_LongText(methodology_text, PATTERN_TOOL, 'E', '. ')
                if tools_text == "":  tools_text = getData_LongText(resumen_text, PATTERN_TOOL, 'E', '. ')
            
            # 6. GET THE RESULT TEXT
            # ============================================================================================
            # finding the title of methodology using PATTERN_RESU
            if result_title=="":
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
            if conclusion_title != "":
                # Desde este punto (pagina) comienza el texto para la sección de conclusiones
                if conclusion_text == "" :
                    conclusion_text, conclusion_res, font_max, font_submax, font_lastmax  = getData_ResultMethodology(pagelines_list, conclusion_pos, PATTERN_CONC, 18, True, 0, 0, 0)
                elif conclusion_res == False :
                    conclusion_text_, conclusion_res, _, _, _ = getData_ResultMethodology(pagelines_list, conclusion_pos, PATTERN_CONC, 18, conclusion_res, font_max, font_submax, font_lastmax)
                    if conclusion_text_!= "" :
                        conclusion_text = conclusion_text + conclusion_text_
                if conclusion_res :                  
                    conclusion_text = conclusion_text.replace(".\n\n", "._")
                    conclusion_text_list = conclusion_text.split("\n\n")
                    for item in conclusion_text_list:
                        if item.isdigit() or len(item)<=1: conclusion_text_list.remove(item)
                    conclusion_text = str(' '.join(conclusion_text_list))
                    conclusion_text = conclusion_text.replace("\n", "")
                    conclusion_text = conclusion_text.replace("._", ".\n\n")

        if type_val == "A":
            if title_text and title_band == False:
                addText_view(title_text, 1, page+1)
                title_band = True
            if authors_text and authors_band == False:
                addText_view(authors_text, 2, page+1)
                authors_band = True
            if year and year_band == False:
                addText_view(year, 3, page+1)
                year_band = True
            if objective and objective_band == False:
                addText_view(objective, 4, page+1)
                objective_band = True
            if approach and approach_band == False:
                addText_view(approach, 5, page+1)
                approach_band = True
            if design and design_band == False:
                addText_view(design, 6, page+1)
                design_band = True
            if len(typelevel)>0 and typelevel_band == False:
                addText_view(typelevel, 7, page+1)
                typelevel_band = True
            if len(samples)>0 and samples_band == False:
                addText_view(samples, 8, page+1)
                samples_band = True
            if len(tools_text)>0 and tools_band == False:
                addText_view(tools_text, 9, page+1)
                tools_band = True
            if len(result_text)>0 and result_band == False:
                addText_view(result_text, 10, page+1)
                result_band = True
            if len(conclusion_text)>0 and conclusion_band == False:
                addText_view(conclusion_text, 11, page+1)
                conclusion_band = True

            if title_ctrl == True and title_text!="" and np == length-1 :
                if title_band == False:
                    addText_view(title_text, 1, 1)
                if authors_band == False:
                    addText_view(authors_text, 2, 1)
                if year_band == False:
                    addText_view(year, 3, 1)
                if objective_band == False:
                    addText_view(objective, 4, 1)
                if approach_band == False:
                    addText_view(approach, 5, 1)
                if design_band == False:
                    addText_view(design, 6, 1)
                if typelevel_band == False:
                    addText_view(typelevel, 7, 1)
                if samples_band == False:
                    addText_view(samples, 8, 1)
                if tools_band == False:
                    addText_view(tools_text, 9, 1)
                if result_band == False:
                    addText_view(result_text, 10, page-1)
                if conclusion_band == False:
                    addText_view(conclusion_text, 11, page)
                    
                addText_view("http://", 12, pdf_npages)
                addText_view("_", 13, 1)
        
        if type_val == "M":
            if title_text and title_band == False:
                addText_view(title_text, 14, page+1)
                title_band = True
            if authors_text and authors_band == False:
                addText_view(authors_text, 15, page+1)
                authors_band = True
            if year and year_band == False:
                addText_view(year, 16, page+1)
                year_band = True
            if paper and paper_band == False:
                addText_view(paper, 17, page+1)
                paper_band = True
            if volume and volume_band == False:
                addText_view(volume, 18, page+1)
                volume_band = True
            if pagem and pagem_band == False:
                addText_view(pagem, 19, page+1)
                pagem_band = True
                        
            if len(key_att_ids) == 0:
                for value in pdf_attributes :
                    key_result, key_attributes = get_keys_attr(type_val, value)
                    if key_result:
                        for value in key_attributes :
                            key_att_ids.append(value[0])

                if len(key_att_ids) > 0:
                    for key in key_att_ids:
                        addText_view("", key, page+1)

            if title_ctrl == True and title_text!="" and np == length-1 :
                if title_band == False:
                    addText_view(title_text, 14, 1)
                if authors_band == False:
                    addText_view(authors_text, 15, 1)
                if year_band == False:
                    addText_view(year, 16, 1)
                if paper_band == False:
                    addText_view(paper, 17, 1)
                if volume_band == False:
                    addText_view(volume, 18, 1)
                if pagem_band == False:
                    addText_view(pagem, 19, 1)
        np += 1

    return language, title_text