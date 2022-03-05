import os, re, json
from flask import Blueprint, Response, render_template, request, redirect, make_response, jsonify, send_file, send_from_directory, redirect
from utils.config import cfg
from utils.handle_files import allowed_file, allowed_file_filesize, get_viewProcess_CPU
from werkzeug.utils import secure_filename
from scripts.split import pdf_remove, pdf_splitter, img_splitter
from scripts.process import pdf_process
from datetime import datetime
from datetime import date
from utils.sqlite_tools import *
from __init__ import create_app, db

import cv2
import pytesseract
from docx import Document
from docx.shared import Pt 
from fold_to_ascii import fold
from flask_login import current_user
from wtforms import TextField, Form

main = Blueprint('main', __name__)

# app = Flask(__name__)
app = create_app() # we initialize our flask app using the __init__.py function

app.jinja_env.auto_reload = True
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config['MAX_CONTENT_LENGTH'] = cfg.FILES.MAX_CONTENT_LENGTH 
app.config['UPLOAD_EXTENSIONS']  = cfg.FILES.UPLOAD_EXTENSIONS
app.config['SINGLE_UPLOAD']      = cfg.FILES.SINGLE_UPLOAD
app.config['SINGLE_SPLIT']       = cfg.FILES.SINGLE_SPLIT
app.config['SINGLE_OUTPUT']      = cfg.FILES.SINGLE_OUTPUT
app.config['SINGLE_FORWEB']      = cfg.FILES.SINGLE_FORWEB
app.config['MULTIPLE_UPLOAD']    = cfg.FILES.MULTIPLE_UPLOAD
app.config['MULTIPLE_SPLIT_PDF'] = cfg.FILES.MULTIPLE_SPLIT_PDF
app.config['MULTIPLE_SPLIT_IMG'] = cfg.FILES.MULTIPLE_SPLIT_IMG
app.config['MULTIPLE_OUTPUT']    = cfg.FILES.MULTIPLE_OUTPUT
app.config['MULTIPLE_FORWEB']    = cfg.FILES.MULTIPLE_FORWEB
app.config['SINGLE_SPLIT_WEB']   = cfg.FILES.SINGLE_SPLIT_WEB
app.config['MULTIPLE_SPLIT_WEB'] = cfg.FILES.MULTIPLE_SPLIT_WEB

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['PDF', 'pdf'])
ILLEGAL_XML_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]")


def strip_illegal_xml_characters(s, default, base=10):
    # Compare the "invalid XML character range" numerically
    n = int(s, base)
    if n in (0xb, 0xc, 0xFFFE, 0xFFFF) or 0x0 <= n <= 0x8 or 0xe <= n <= 0x1F or 0xD800 <= n <= 0xDFFF:
        return ""
    return default

def delete_paragraph(paragraph):
    paragraph._element.getparent().remove(paragraph._element)
    paragraph._p = paragraph._element = None

def validate_path(path):
    new_path = path
    path_split = path.split("/")
    filename = path_split[-1]

    if filename[0] == "_":
        i = 0
        for c in filename:
            if c != filename[0]:
                pos = i
                break
            i += 1
        new_path = "/".join(path_split[:-1])+"/"+filename[pos:]

    return new_path

def build_document_(title, text_pdf, language):
    document.add_heading(title)

    keywords = "sample"
    texts = []

    # add a paragraphs
    if language != '' :
        for key, value in text_pdf:
            p = document.add_paragraph()

            patt = re.search(rf"\b{keywords}\b", value, re.IGNORECASE)
            # print("values")
            if patt != None:
                text_1 = value[:patt.start(0)]
                text_2 = keywords
                text_3 = value[patt.end(0):]
                texts = [tuple(["N", text_1]), tuple(["I", text_2]), tuple(["N", text_3])]
                band = True
            else:
                texts = [tuple([key, value])]

            for key_text, value_text in texts :
                # line = p.add_run(str(value.encode('utf-8').decode("utf-8")))
                try:
                    # p = document.add_paragraph(str(value.encode('utf-8').decode("utf-8")))
                    line = p.add_run(str(value_text.encode('utf-8').decode("utf-8")))
                except:
                    delete_paragraph(p)
                    p = document.add_paragraph()
                    html = value_text.encode("ascii", "xmlcharrefreplace").decode("utf-8")
                    html = re.sub(r"&#(\d+);?", lambda c: strip_illegal_xml_characters(c.group(1), c.group(0)), html)
                    html = re.sub(r"&#[xX]([0-9a-fA-F]+);?", lambda c: strip_illegal_xml_characters(c.group(1), c.group(0), base=16), html)
                    html = ILLEGAL_XML_CHARS_RE.sub("", html)
                    # p = document.add_paragraph(str(html.encode('utf-8').decode("utf-8")))
                    line = p.add_run(str(html.encode('utf-8').decode("utf-8")))

                if key_text == "B": line.bold = True
                if key_text == "I": line.bold = True; line.italic = True; line.font.size = Pt(12) #line.font.color.rgb = RGBColor(0x22, 0x8b, 0x22)
            
            texts = []
            # if key == "B":  p.add_run('bold').bold = True

    return document

def build_document(title, text_pdf, language):
    # document = Document() 
    document.add_heading(title)

    # add a paragraphs
    if language != '' :
        for key, value in text_pdf:
            # doc = docx.Document()
            p = document.add_paragraph()
            # line = p.add_run(str(value.encode('utf-8').decode("utf-8")))
            try:
                # p = document.add_paragraph(str(value.encode('utf-8').decode("utf-8")))
                line = p.add_run(str(value.encode('utf-8').decode("utf-8")))
            except:
                delete_paragraph(p)
                p = document.add_paragraph()
                html = value.encode("ascii", "xmlcharrefreplace").decode("utf-8")
                html = re.sub(r"&#(\d+);?", lambda c: strip_illegal_xml_characters(c.group(1), c.group(0)), html)
                html = re.sub(r"&#[xX]([0-9a-fA-F]+);?", lambda c: strip_illegal_xml_characters(c.group(1), c.group(0), base=16), html)
                html = ILLEGAL_XML_CHARS_RE.sub("", html)
                # p = document.add_paragraph(str(html.encode('utf-8').decode("utf-8")))
                # line = p.add_run(str(html.encode('utf-8').decode("utf-8")))
                line = p.add_run(str(html))

            if key == "B": line.bold = True
            
            # texts = []
            # if key == "B":  p.add_run('bold').bold = True

    return document

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class SearchForm(Form):
    autocomp = TextField('Busca palabras claves', id='keyword_autocomplete')

# ------------------------------------ ROUTING ------------------------------------

# Home
@main.route('/home')
def home():
    if current_user.is_authenticated:
        list_projects = get_listProjects()
        return render_template('home.html', name=current_user.name.split()[0], projects=list_projects)
    else:
        return render_template('login.html')

@main.route('/create/upload')
def upload_form():
    if current_user.is_authenticated:
        list_universities = get_listUniversities()
        list_keywords = get_listKeywords()
        return render_template('upload_form.html', name=current_user.name.split()[0], universities=list_universities, keywords=list_keywords)
    else:
        return render_template('upload_form.html')

@app.route('/create/upload', methods=['GET', 'POST'])
def upload_form():
    form = SearchForm(request.form)
    return render_template("upload_form.html", keywords_form=form)

@main.route('/create/db')
def db_form():
    if current_user.is_authenticated:
        # list_projects = get_listProjects()
        return render_template('db_form.html', name=current_user.name.split()[0], n_projects = 0, keyword = "")
    else:
        return render_template('db_form.html')

@main.route('/upload/home/<id>')
def upload_home(id):
    if current_user.is_authenticated:
        one_project = get_projectById(id)
        list_keywords = get_pkDetailById(id)

        print("list_keywords", list_keywords)
        return render_template('upload_home.html', name=current_user.name.split()[0], project=one_project[0], keywords=list_keywords, pro_id=id)
    else:
        return render_template('upload_home.html')

# Papers
@main.route('/paper_one')
def paper_one():
    if current_user.is_authenticated:
        return render_template('paper_one.html', name=current_user.name.split()[0])
    else:
        return render_template('paper_one.html')

@main.route('/paper_mul/<id>')
def paper_mul(id):
    if current_user.is_authenticated:
        return render_template('paper_mul.html', name=current_user.name.split()[0], pro_id=id)
    else:
        return render_template('paper_mul.html')

# Thesis
@main.route('/thesis_one')
def thesis_one():
    if current_user.is_authenticated:
        return render_template('thesis_one.html', name=current_user.name.split()[0])
    else:
        return render_template('thesis_one.html')

@main.route('/thesis_mul/<id>')
def thesis_mul(id):
    if current_user.is_authenticated:
        return render_template('thesis_mul.html', name=current_user.name.split()[0], pro_id=id)
    else:
        return render_template('thesis_mul.html')

@main.route('/thesis_search')
def thesis_search():
    if current_user.is_authenticated:
        return render_template('thesis_search.html', name=current_user.name.split()[0])
    else:
        return render_template('thesis_search.html')

@main.route('/report')
def report():
    return render_template('report.html')


"""
    FORM UPLOAD DOCUMENTS
    =====================
"""
@main.route("/save_upload", methods=["POST"])
def save_upload():
    id = 0
    msg_project = ""
    msg_pkdetail = ""
    if request.method == 'POST':
        current_date = date.today().strftime("%d/%m/%Y")
        try:
            if request.form['type_a']:
                type_a = 1
        except:
            type_a = 0
        
        try:
            if request.form['type_m']:
                type_m = 1
        except:
            type_m = 0

        if current_user.is_authenticated:
            user_id = current_user.id

        project = {
            'title' :       request.form['title'],
            'university' :  request.form['university'],
            'career' :      request.form['career'],
            'type_a' :      type_a,
            'type_m' :      type_m,
            'n_articles':   0,
            'n_process':    0,
            'user' :        user_id,
            'created' :     current_date
        }
        keywords = request.form['keywords_out'].split(',')
        print("keywords", keywords)
        
        try:
            response_project, id = put_newProject(project)
            if response_project is True:
                msg_project = "Proyecto registrado con éxito"
        except:
            msg_project = "Error en registro del proyecto"
        
        try:
            for key in keywords:
                response_pkdetail = put_newPKdetail(id, key, current_date)
            if response_pkdetail is True:
                msg_pkdetail = "PKdetail registrado con éxito"
        except:
            msg_pkdetail = "Error en registro de PKdetail"
        
        finally:
            print(msg_project)
            print(msg_pkdetail)
            return redirect('/upload/home/'+str(id))


@main.route("/add_variable", methods=["POST"])
def add_variable():
    id = 0
    msg_variable = ""
    action = request.values.get("action")

    if request.method == 'POST' and action == 'add':
        current_date = date.today().strftime("%d/%m/%Y")
        value = request.values.get("value")

        try:
            response_key = put_newKeyword(value, current_date)
            if response_key is True:
                msg_variable = "Variable registrada con éxito"
        except:
            msg_variable = "Error en registro de variable"
        
        finally:
            print(msg_variable)
            list_universities = get_listUniversities()
            list_keywords = get_listKeywords()
            title = request.values.get("title")
            return render_template('upload_form.html', name=current_user.name.split()[0], universities=list_universities, keywords=list_keywords, title=title)

"""
    FORM SEARCH DATABASES
    =====================
"""
@main.route("/search_db", methods=["POST"])
def search_db():
    num_projects = 0
    list_projects = None

    if current_user.is_authenticated:
        if request.method == "POST":
            keyword = request.values.get("keyword") 
            if len(keyword) > 1:
                list_projects = get_squareProjects_ByWord(keyword)
                num_projects = len(list_projects)
                
                print("len projects: " + str(num_projects))
        return render_template('db_form.html', name=current_user.name.split()[0], n_projects = num_projects, projects = list_projects, keyword = keyword)
    else:
        return render_template('db_form.html', keyword = "")

    

# ----------------------------------- PDF EXTRACT ONE -----------------------------------
@main.route('/paper_one', methods=['POST'])
def paper_one_load():
    global file_pdf
    active_show = "active show"
    # _analytic = request.form.get('analytic')
    # 
    if request.method == "POST":
        # Code for One pdf
        if "filesize" in request.cookies:
            if not allowed_file_filesize(request.cookies["filesize"], app.config["MAX_CONTENT_LENGTH"]):
                # print("Filesize exceeded maximum limit")
                return redirect(request.url)
            file = request.files["file"]
            filesize = request.cookies.get("filesize")

            if file.filename == "":
                # print("No filename")
                return redirect(request.url)
            if int(filesize) > 0 :
                res = make_response(jsonify({"message": f"El PDF fue cargado con éxito."}), 200)
                # print("File uploaded")
                upload = True
            if allowed_file(file.filename, app.config["UPLOAD_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config["UPLOAD_PATH_UP"], filename))
                file.save(os.path.join(app.config["SINGLE_UPLOAD"], filename))
                file_pdf = filename
                print("File saved")
                if (upload == True):
                    return res
            else:
                print("That file extension is not allowed")
                return redirect(request.url)

@main.route("/action_paper_one", methods=["GET", "POST"])
def action_paper_one():
    result_split = False
    text_pdf = []
    is_article = True

    if request.method == "POST":
        global file_pdf, document
        resultCPU = False
        result_save = None
        result_file_text = ""
        result_file_down = ""

        # Verify if posible to process
        if get_viewProcess_CPU() is True :
            
            document = Document()
            print("Paper")

            file_pdf = fold(file_pdf)  
            path = os.path.join(app.config['SINGLE_UPLOAD'],file_pdf)
            fname = os.listdir(app.config['SINGLE_SPLIT']) #fname: List contain pdf documents names in folder
            # 1. SPLIT PDF
            # print("\n------------------- START SPLIT PROCESS -------------------")
            pdf_remove(fname, app.config['SINGLE_SPLIT'])       # Call pdf remove function
            result_split = pdf_splitter(path, app.config['SINGLE_SPLIT'])      # Call pdf splitter function
            
            if result_split == 0:
                result_save = False
                result_file_text = "No se completó el procesamiento."
                
            if result_split == 2:
                result_save = False
                result_file_text = "El PDF debe tener máximo " + str(cfg.FILES.MAX_NUMPAGES) + " páginas."
            
            if result_split == 1:
                # 2. Process PDF
                # print("\n------------------ START EXTRACT PROCESS ------------------")
                is_article, text_pdf, language = pdf_process(app.config['SINGLE_SPLIT'], app.config['SINGLE_OUTPUT'])           # Call pdf process function
                # print("Len TEXT PDF")
                document = build_document(file_pdf, text_pdf, language)
            # if result_split==True :
                if is_article == False:
                    result_save = 0
                    result_file_text = "Error cargando formato de Tesis ... \nMuy pronto estará disponible"
                elif len(text_pdf) > 1 :
                    file_save = app.config['SINGLE_OUTPUT']+'/background_'+file_pdf+'.docx'
                    document.save(file_save)
                    result_save = 1
                    result_file_text = file_pdf.split(".pdf")[0]
                    result_file_down = app.config['SINGLE_FORWEB']+'/background_'+file_pdf+'.docx'
                else:
                    result_save = 0
                    result_file_text = "Error en la carga del PDF"
            # else:
            #     result_save = 0
            #     result_file_text = "Error en el PDF"
        else:
            resultCPU = True
            result_file_text = "El servidor está procesando, debe esperar un momento."
    
    # print("File Download: " + str(result_file_down))
    # print(result_save)
    return render_template('paper_one.html', result_save=result_save, result_file_text=result_file_text, result_file_down=result_file_down)

@main.route("/close_paper_one/<source>")
def close_paper_one(source):
    url = "/" + source
    return redirect(url)

@main.route("/save_paper_one", methods=["POST"])
def save_paper_one():
    if request.method == "POST":
        down_image = request.form.get('down_image')
        
    return send_file(down_image, as_attachment=True)

# --------------------------------------------------------
@main.route('/thesis_one', methods=['POST'])
def thesis_one_load():
    global file_pdf
    active_show = "active show"
    print("TESIS ONE ....!!!!!!!!!!!!!!!!!!!!!!!!!!")
    # _analytic = request.form.get('analytic')
    # 
    if request.method == "POST":
        # Code for One pdf
        if "filesize" in request.cookies:
            if not allowed_file_filesize(request.cookies["filesize"], app.config["MAX_CONTENT_LENGTH"]):
                # print("Filesize exceeded maximum limit")
                return redirect(request.url)
            file = request.files["file"]
            filesize = request.cookies.get("filesize")

            if file.filename == "":
                # print("No filename")
                return redirect(request.url)
            if int(filesize) > 0 :
                res = make_response(jsonify({"message": f"El PDF fue cargado con éxito."}), 200)
                # print("File uploaded")
                upload = True
            if allowed_file(file.filename, app.config["UPLOAD_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                # file.save(os.path.join(app.config["UPLOAD_PATH_UP"], filename))
                file.save(os.path.join(app.config["SINGLE_UPLOAD"], filename))
                file_pdf = filename
                print("File saved")
                if (upload == True):
                    return res
            else:
                print("That file extension is not allowed")
                return redirect(request.url)

@app.route('/files/single/upload/<filename>')
def thesis_upload(filename):
    return send_from_directory(app.config['SINGLE_UPLOAD'], filename)

@app.route('/files/single/split/<filename>')
def thesis_split(filename):
    return send_from_directory(app.config['SINGLE_SPLIT'], filename)

@app.route('/files/multiple/split_img/<filename>')
def thesis_split_img(filename):
    return send_from_directory(app.config['MULTIPLE_SPLIT_IMG'], filename)

@main.route("/action_thesis_one", methods=["POST"])
def action_thesis_one():
    result_split = False
    global file_pdf
    global pdf_id

    if request.method == "POST":
        result_cpu = False
        action = None
        text = None
        pdf = None
        pdf_file = None
        pdf_result = None

        # Verify if posible to process
        if get_viewProcess_CPU() is True :
            file_pdf = fold(file_pdf)
            fname = os.listdir(app.config['SINGLE_SPLIT'])
            path = os.path.join(app.config['SINGLE_UPLOAD'],file_pdf)
            action = request.values.get("action")
            print("Action", action)

            if action == "save_canvas":
                det_id =        int(request.values.get("det_id"))
                det_attribute = int(request.values.get("det_attribute"))
                rect = {
                        'x': int(request.values.get("x")),
                        'y': int(request.values.get("y")),
                        'w': int(request.values.get("w")),
                        'h': int(request.values.get("h"))
                    }
                page = int(request.values.get("page"))                
                image = app.config['SINGLE_SPLIT_WEB'] + "/page_" + str(page-1) + ".jpg"
                image = cv2.imread(image, 0)
                thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                ROI = thresh[rect['y']:rect['y']+rect['h'],rect['x']:rect['x']+rect['w']]

                print("ROI len", str(len(ROI)))
                text = ""
                try:
                    text = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
                    print(text)
                except:
                    print("Error generate text")
                
                if text is None or text == "":
                    text = "..."
                pdf = upd_detailByIds(det_id, pdf_id, det_attribute, text, page, rect)
                result_split = 1
            
            if action == "save_text":
                det_id =        int(request.values.get("det_id"))
                det_attribute = int(request.values.get("det_attribute"))
                det_value =     request.values.get("det_value")
                
                if text is None or text == "":
                    text = "..."
                pdf = upd_detailTextByIds(det_id, pdf_id, det_attribute, det_value)
                result_split = 1
            
            if action == "save_attribute":
                current_date = date.today().strftime("%d/%m/%Y")
                att_value =  request.values.get("new_att")

                try:
                    response_att, id = put_newPDFattribute(att_value, current_date)
                    if response_att is True:
                        msg_att = "Atributo registrado con éxito"
                except:
                    msg_att = "Error en registro del atributo"
                
                try:
                    response_pdf = put_newPDFdetail(pdf_id, id)
                    if response_pdf is True:
                        msg_pdf = "PDF detail registrado con éxito"
                except:
                    msg_pdf = "Error en registro de PDFdetail"
                
                finally:
                    print(msg_att)
                    print(msg_pdf)
                    result_split = 1
            
            if action == "remove_attribute":
                det_id = int(request.values.get("det_id"))
                
                try:
                    response_pdf = del_itemPDFdetail(det_id)
                    if response_pdf is True:
                        msg_pdf = "PDF detail eliminado con éxito"
                except:
                    msg_pdf = "Error en eliminación de PDFdetail"
                
                finally:
                    print(msg_pdf)
                    result_split = 1

            # 1. SPLIT PDF
            # print("\n------------------- START SPLIT PROCESS -------------------")
            if action is None:
                pdf_remove(fname, app.config['SINGLE_SPLIT'])                   # Call pdf remove function
                result_split, npages = img_splitter(path, app.config['SINGLE_SPLIT'], 1)   # Call pdf splitter function
            
            if result_split == 0:
                result_save = 0
                pdf_text = {'result': "Procesamiento Incompleto"}
            
            if result_split == 1:
                # print("\n------------------ START EXTRACT PROCESS ------------------")
                
                # get data for "pdf"
                pdf = get_thesisByName(file_pdf)
                pdf_id = pdf['id']
                """Verificar pdf_details, encontrados y no encontradps"""
                if len(pdf['foundlist']): select = None 
                else: select = "."
                list_npages = list(range(1, int(pdf['npages']+1)))
                list_npages = [str(int) for int in list_npages]
                pdf['listnpages'] = list_npages
                # get data for pdf_file
                pdf_file = {
                        'name': file_pdf,
                        'path_upload': "http://127.0.0.1:5000/files/single/upload/" + file_pdf,
                        'path_page':   app.config['SINGLE_SPLIT_WEB'] + '/page_0.jpg',
                        'num_pages':   int(pdf['npages']),
                        }
        else:
            result_cpu = True
            pdf_text = {'result': "Servidor Ocupado", 'found': "", 'not_found': ""}
            # result_file_text = "El servidor está procesando, debe esperar un momento."
    
    print("SQL report")
    print(json.dumps(pdf))
    return render_template('thesis_one.html', _pdf_file = pdf_file, _pdf = pdf)


@main.route('/thesis_mul', methods=['POST'])
def thesis_mul_load():
    global file_pdfs
    upload = False
    file_pdfs = []
    result_split = []

    if request.method == "POST":
        pro_id = request.form.get('pro_id')
        print("PRO_ID", pro_id)
        # Code for multiple pdfs
        if 'files[]' not in request.files:
            print('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            file_pdfs.append(file.filename)
            if file and allowed_file(file.filename, app.config["UPLOAD_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['MULTIPLE_UPLOAD'], filename))
                upload = True
        
        if (upload == True):
            print('File(s) successfully uploaded')
            return render_template('thesis_mul.html', resultLoad=upload, pro_id=pro_id)

#
# FUNCTION TO GET DATA 

# 
# FUNCTION TO PROCESS PDF 
# 
@main.route("/action_thesis_mul", methods=["POST"])
def action_thesis_mul():
    global file_pdfs
    text_pdf = []

    if request.method == "POST":
        global file_pdf, document
        resultCPU = False
        action = None
        result_save = None
        result_file_text = "None"
        result_invalid_text = ""
        result_file_down = "None"
        result_valid = 0
        result_invalid = 0
        result_invalid_process = []
        pro_id = request.form.get('pro_id')

        # Verify if posible to process
        if get_viewProcess_CPU() is True :

            document = Document() 
            print("NumPDFs Cargados")
            print(len(file_pdfs))
            for filename in file_pdfs :
                filename = fold(filename)
                fname = os.listdir(app.config['MULTIPLE_SPLIT_PDF'])
                path = os.path.join(app.config['MULTIPLE_UPLOAD'],filename)
                path = validate_path(path)
                path = path.replace('(','').replace(')','').replace(',','').replace('<','').replace('>','').replace('?','').replace('!','').replace('@','').replace('%','').replace('$','').replace('#','').replace('*','').replace('&','').replace(';','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace('=','').replace('+','').replace(' ','_')
                action = request.values.get("action")
                print("Action", action)

                if action == "save_canvas":
                    det_id =        int(request.values.get("det_id"))
                    det_attribute = int(request.values.get("det_attribute"))
                    rect = {
                            'x': int(request.values.get("x")),
                            'y': int(request.values.get("y")),
                            'w': int(request.values.get("w")),
                            'h': int(request.values.get("h"))
                        }
                    page = int(request.values.get("page"))                
                    image = app.config['SINGLE_SPLIT_WEB'] + "/page_" + str(page-1) + ".jpg"
                    image = cv2.imread(image, 0)
                    thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                    ROI = thresh[rect['y']:rect['y']+rect['h'],rect['x']:rect['x']+rect['w']]

                    print("ROI len", str(len(ROI)))
                    text = ""
                    try:
                        text = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
                        print(text)
                    except:
                        print("Error generate text")
                    
                    if text is None or text == "":
                        text = "..."
                    pdf = upd_detailByIds(det_id, pdf_id, det_attribute, text, page, rect)
                    result_split = 1
                
                if action == "save_text":
                    det_id =        int(request.values.get("det_id"))
                    det_attribute = int(request.values.get("det_attribute"))
                    det_value =     request.values.get("det_value")
                    
                    if text is None or text == "":
                        text = "..."
                    pdf = upd_detailTextByIds(det_id, pdf_id, det_attribute, det_value)
                    result_split = 1
                
                if action == "save_attribute":
                    current_date = date.today().strftime("%d/%m/%Y")
                    att_value =  request.values.get("new_att")

                    try:
                        response_att, id = put_newPDFattribute(att_value, current_date)
                        if response_att is True:
                            msg_att = "Atributo registrado con éxito"
                    except:
                        msg_att = "Error en registro del atributo"
                    
                    try:
                        response_pdf = put_newPDFdetail(pdf_id, id)
                        if response_pdf is True:
                            msg_pdf = "PDF detail registrado con éxito"
                    except:
                        msg_pdf = "Error en registro de PDFdetail"
                    
                    finally:
                        print(msg_att)
                        print(msg_pdf)
                        result_split = 1
                
                if action == "remove_attribute":
                    det_id = int(request.values.get("det_id"))
                    
                    try:
                        response_pdf = del_itemPDFdetail(det_id)
                        if response_pdf is True:
                            msg_pdf = "PDF detail eliminado con éxito"
                    except:
                        msg_pdf = "Error en eliminación de PDFdetail"
                    
                    finally:
                        print(msg_pdf)
                        result_split = 1

                # 1. SPLIT PDF
                # print("\n------------------- START SPLIT PROCESS -------------------")
                if action is None:
                    print("filename", filename)
                    print("fname", fname)
                    # 1. Remove and split PDF
                    # pdf_remove(fname, app.config['MULTIPLE_SPLIT_PDF'])
                    result_split, pdf_npages = pdf_splitter(path, app.config['MULTIPLE_SPLIT_PDF'])   # Call pdf splitter function
                
                print("result_split", result_split)
                if result_split == 0:
                    result_invalid += 1
                    result_invalid_process.append(filename + " ...NO se procesó")
                if result_split == 2:
                    result_invalid += 1
                    result_invalid_process.append(filename + " ...supera el Nro páginas")
                
                if result_split == 1:
                    # Put data on pdf_info
                    pdf_size = os.path.getsize(path)
                    current_date = date.today().strftime("%d/%m/%Y")
                    pdf = {
                        'name' :     filename,
                        'npages' :   pdf_npages,
                        'size' :     pdf_size,
                        'created' :  current_date
                    }
                    try:
                        pdf_info_id = put_newPDF(pdf)
                    except:
                        print("Error en registro del PDF info")

                    if pdf_info_id:
                        img_split, img_npages = img_splitter(path, app.config['MULTIPLE_SPLIT_IMG'], pdf_info_id)   # Call img splitter function
                        print(img_split)
                        print("Number IMG_pages", img_npages)
                    # 2. Process PDF
                    # print("\n------------------ START EXTRACT PROCESS ------------------")
                    _, text_pdf, language, title_text = pdf_process(app.config['MULTIPLE_SPLIT_PDF'], app.config['MULTIPLE_OUTPUT'], pdf_info_id)  # Call pdf process function
                    # print("Out web: " + app.config['MULTIPLE_FORWEB'])
                    print("title_text", title_text)

                    if len(text_pdf) > 1 :
                        now = datetime.now()
                        document = build_document(filename, text_pdf, language)
                        file_save = app.config['MULTIPLE_OUTPUT']+'/background_multiple_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
                        document.save(file_save)
                        result_valid += 1
                        result_file_text = "Antecedente Múltiple"
                        result_file_down = app.config['MULTIPLE_FORWEB']+'/background_multiple_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
                
                print("result_valid", result_valid)
                if result_valid > 0 :
                    result_save = True

                    try:
                        _ = put_newPPdetail(pro_id, pdf_info_id, title_text, current_date)
                    except:
                        print("Error en registro de PRO PDF detail")
                    
                if result_invalid > 0 and result_valid == 0 :
                    result_save = False
                    result_file_text = "No fue posible procesar"
                
                if len(result_invalid_process) > 0 :
                    # result_save = False
                    result_invalid_text = (',  \n'.join(result_invalid_process))
            
            # Save resutls on database
            # Get data from project_info
            project = get_projectById(pro_id)
            n_process = int(project[0]["pro_n_process"]) + 1

            # Put data on pro_pdf_details

            # Update data on project_info
            saveDB = upd_projectById(pro_id, result_valid, n_process)
            if saveDB is True:
                print("Se actualizó con éxito project_info")
                    
        else:
            result_file_text = "El servidor está procesando, espere un momento."
    
    return render_template('thesis_mul.html', result_save=result_save, result_file_text=result_file_text, result_invalid_text=result_invalid_text, result_file_down=result_file_down, pro_id=pro_id)

"""
    PROJECT PDF 
    =====================
"""
#   AQUI ME QUEDE ... 
#   SOLUCION: ENVIAR DATOS POR GET OR POST HACIA ESTA FUNCION, PARA ACTIVAR LA PAG SELECCIONADA .. 

@main.route('/project/pdfs/<id>')
def project_pdfs(id):
    global pro_id
    pro_id = id
    if current_user.is_authenticated:
        project = get_projectById(id)
        pdfs = get_projectPDFById(id)
        # pdfs = get_pdfDetailById(id)
        # pdf = get_thesisByName(file_pdf)
        for pdf in pdfs:
            # revisar esto ... luego de hacer el input pdf_details
            # pdf_id = pdf['id']
            # pdf_id = pdf['pdf_id']
            """Verificar pdf_details, encontrados y no encontradps"""
            # if len(pdf['foundlist']): select = None 
            # else: select = "."
            list_npages = list(range(1, int(pdf['pdf_npages']+1)))
            list_npages = [str(int) for int in list_npages]
            pdf['listnpages'] = list_npages

            # get data for pdf_file
            pdf_path = {
                    'name': pdf['pdf_name'],
                    # 'path_upload': "http://127.0.0.1:5000/files/multiple/upload/" + pdf['pdf_name'],
                    # 'path_page':   app.config['MULTIPLE_SPLIT_WEB'] + '/' + str(pdf['id']) + 'page_0.jpg',
                    'num_pages':   int(pdf['pdf_npages']),
                    }
            pdf['pdf_path'] = pdf_path
        # return render_template('thesis_one.html', _pdf_file = pdf_file, _pdf = pdf)
        
        return render_template('project_pdfs.html', name=current_user.name.split()[0], pdfs=pdfs, pdf=None, project=project[0], pro_id=id)
        # project = one_project
    else:
        return render_template('project_pdfs.html')


@main.route('/<pdf_id>')
def project_pdf(pdf_id):
    if current_user.is_authenticated:
        project = get_projectById(pro_id)
        pdfs = get_projectPDFById(pro_id)
        pdf = get_pdfDetailById(pdf_id)
        print("NEW PDFs")
        """Verificar pdf_details, encontrados y no encontradps"""
        list_npages = list(range(1, int(pdf['npages']+1)))
        list_npages = [str(int) for int in list_npages]
        pdf['listnpages'] = list_npages

        # get data for pdf_file
        pdf_path = {
                'name':        pdf['name'],
                # 'path_upload': "http://127.0.0.1:5000/files/multiple/upload/" + pdf['name'],
                'path_page':   app.config['MULTIPLE_SPLIT_WEB'] + '/' + str(pdf['id']) + 'page_0.jpg',
                'num_pages':   int(pdf['npages']),
                }
        pdf['pdf_path'] = pdf_path

        return render_template('project_pdfs.html', name=current_user.name.split()[0], pdfs=pdfs, pdf=pdf, project=project[0], pro_id=pro_id)
        # project = one_project
    else:
        return render_template('project_pdfs.html')


@main.route("/<pdf_id>", methods=["POST"])
def pdf_post(pdf_id):
    global file_pdfs
    text_pdf = []

    if request.method == "POST":
        action = request.values.get("action")
        print("Action", action)

        if action == "save_canvas":
            det_id =        int(request.values.get("det_id"))
            det_attribute = int(request.values.get("det_attribute"))
            rect = {
                    'x': int(request.values.get("x")),
                    'y': int(request.values.get("y")),
                    'w': int(request.values.get("w")),
                    'h': int(request.values.get("h"))
                }
            page = int(request.values.get("page"))                
            image = app.config['SINGLE_SPLIT_WEB'] + "/page_" + str(page-1) + ".jpg"
            image = cv2.imread(image, 0)
            thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
            ROI = thresh[rect['y']:rect['y']+rect['h'],rect['x']:rect['x']+rect['w']]

            print("ROI len", str(len(ROI)))
            text = ""
            try:
                text = pytesseract.image_to_string(ROI, lang='eng',config='--psm 6')
                print(text)
            except:
                print("Error generate text")
            
            if text is None or text == "":
                text = "..."
            pdf = upd_detailByIds(det_id, pdf_id, det_attribute, text, page, rect)
            result_split = 1
        
        if action == "save_text":
            det_id =        int(request.values.get("det_id"))
            det_attribute = int(request.values.get("det_attribute"))
            det_value =     request.values.get("det_value")
            
            if text is None or text == "":
                text = "..."
            pdf = upd_detailTextByIds(det_id, pdf_id, det_attribute, det_value)
            result_split = 1
        
        if action == "save_attribute":
            current_date = date.today().strftime("%d/%m/%Y")
            att_value =  request.values.get("new_att")

            try:
                response_att, id = put_newPDFattribute(att_value, current_date)
                if response_att is True:
                    msg_att = "Atributo registrado con éxito"
            except:
                msg_att = "Error en registro del atributo"
            
            try:
                response_pdf = put_newPDFdetail(pdf_id, id)
                if response_pdf is True:
                    msg_pdf = "PDF detail registrado con éxito"
            except:
                msg_pdf = "Error en registro de PDFdetail"
            
            finally:
                print(msg_att)
                print(msg_pdf)
                result_split = 1
        
        if action == "remove_attribute":
            det_id = int(request.values.get("det_id"))
            
            try:
                response_pdf = del_itemPDFdetail(det_id)
                if response_pdf is True:
                    msg_pdf = "PDF detail eliminado con éxito"
            except:
                msg_pdf = "Error en eliminación de PDFdetail"
            
            finally:
                print(msg_pdf)
                result_split = 1

        if current_user.is_authenticated and result_split == 1:
            project = get_projectById(pro_id)
            pdfs = get_projectPDFById(pro_id)
            pdf = get_pdfDetailById(pdf_id)
            print("NEW PDFs")
            """Verificar pdf_details, encontrados y no encontradps"""
            list_npages = list(range(1, int(pdf['npages']+1)))
            list_npages = [str(int) for int in list_npages]
            pdf['listnpages'] = list_npages

            # get data for pdf_file
            pdf_path = {
                    'name':        pdf['name'],
                    # 'path_upload': "http://127.0.0.1:5000/files/multiple/upload/" + pdf['name'],
                    'path_page':   app.config['MULTIPLE_SPLIT_WEB'] + '/' + str(pdf['id']) + 'page_0.jpg',
                    'num_pages':   int(pdf['npages']),
                    }
            pdf['pdf_path'] = pdf_path

            return render_template('project_pdfs.html', name=current_user.name.split()[0], pdfs=pdfs, pdf=pdf, project=project[0], pro_id=pro_id)
        

@main.route("/action_thesis_search", methods=["POST"])
def action_thesis_search():
    pdfs = None

    if request.method == "POST":
        keyword = request.values.get("keyword") 
        
        if len(keyword) > 1:
            pdfs = get_listThesisByWord(keyword)
            print("len pdfs: " + str(len(pdfs)))
        
    return render_template('thesis_search.html', _pdfs = pdfs)


@main.route("/close_thesis_one/<source>")
def close_thesis_one(source):
    url = "/" + source
    return redirect(url)

@main.route("/save_thesis_one", methods=["POST"])
def save_thesis_one():
    if request.method == "POST":
        down_image = request.form.get('down_image')
        
    return send_file(down_image, as_attachment=True)

# ----------------------------------- PDF EXTRACT MULTIPLE -----------------------------------
@main.route('/paper_mul', methods=['POST'])
def paper_mul_load():
    global file_pdfs
    upload = False
    file_pdfs = []
    result_split = []

    if request.method == "POST":
        pro_id = request.form.get('pro_id')
        # Code for multiple pdfs
        if 'files[]' not in request.files:
            print('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')

        for file in files:
            file_pdfs.append(file.filename)
            if file and allowed_file(file.filename, app.config["UPLOAD_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['MULTIPLE_UPLOAD'], filename))
                upload = True
        
        if (upload == True):
            print('File(s) successfully uploaded')
            return render_template('paper_mul.html', resultLoad=upload, pro_id=pro_id)


@main.route("/action_paper_mul", methods=["POST"])
def action_paper_mul():
    global file_pdfs
    text_pdf = []

    if request.method == "POST":
        global file_pdf, document
        resultCPU = False
        action = None
        result_save = None
        result_file_text = "None"
        result_invalid_text = ""
        result_file_down = "None"
        result_valid = 0
        result_invalid = 0
        result_invalid_process = []
        pro_id = request.form.get('pro_id')

        # Verify if posible to process
        if get_viewProcess_CPU() is True :

            document = Document() 
            print("NumPDFs Cargados")
            print(len(file_pdfs))
            for filename in file_pdfs :
                filename = fold(filename)                
                fname = os.listdir(app.config['MULTIPLE_SPLIT_PDF'])
                path = os.path.join(app.config['MULTIPLE_UPLOAD'],filename)
                path = validate_path(path)
                path = path.replace('(','').replace(')','').replace(',','').replace('<','').replace('>','').replace('?','').replace('!','').replace('@','').replace('%','').replace('$','').replace('#','').replace('*','').replace('&','').replace(';','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace('=','').replace('+','').replace(' ','_')
                action = request.values.get("action")
                print("Action", action)

                if action is None:
                    # 1. Remove and split PDF
                    pdf_remove(fname, app.config['MULTIPLE_SPLIT_PDF'])                     # Call pdf remove function
                    result_split = pdf_splitter(path, app.config['MULTIPLE_SPLIT_PDF'])     # Call pdf splitter function

                if result_split == 0:
                    # result_save = False
                    result_invalid += 1
                    result_invalid_process.append(filename + " ...NO se procesó")
                    # result_file_text = "No se logró procesar"
                if result_split == 2:
                    # result_save = False
                    result_invalid += 1
                    result_invalid_process.append(filename + " ...supera el Nro páginas")
                    # result_file_text = "El PDF debe tener máximo " + str(cfg.FILES.MAX_NUMPAGES) + " páginas."
                if result_split == 1:
                    # 2. Process PDF
                    # print("\n------------------ START EXTRACT PROCESS ------------------")
                    _, text_pdf, language = pdf_process(app.config['MULTIPLE_SPLIT_PDF'], app.config['MULTIPLE_OUTPUT'])  # Call pdf process function
                    # print("Out web: " + app.config['MULTIPLE_FORWEB'])
                    print("len text_pdf", str(len(text_pdf)))

                    if len(text_pdf) > 1 :
                        now = datetime.now()
                        document = build_document(filename, text_pdf, language)
                        file_save = app.config['MULTIPLE_OUTPUT']+'/background_multiple_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
                        document.save(file_save)
                        result_valid += 1
                        result_file_text = "Antecedente Múltiple"
                        result_file_down = app.config['MULTIPLE_FORWEB']+'/background_multiple_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'

                if result_valid > 0 :
                    result_save = True
                
                if result_invalid > 0 and result_valid == 0 :
                    result_save = False
                    result_file_text = "No fue posible procesar"
                
                if len(result_invalid_process) > 0 :
                    # result_save = False
                    result_invalid_text = (',  \n'.join(result_invalid_process))
            
            # Save resutls on database
            project = get_projectById(pro_id)
            n_process = int(project[0]["pro_n_process"]) + 1
            saveDB = upd_projectById(pro_id, result_valid, n_process)
            if saveDB is True:
                print("Se actualizó con éxito project_info")
        else:
            result_file_text = "El servidor está procesando, espere un momento."
    
    return render_template('paper_mul.html', result_save=result_save, result_file_text=result_file_text, result_invalid_text=result_invalid_text, result_file_down=result_file_down, pro_id=pro_id)

# CLOSE PAPER
@main.route("/<source>")
def close_paper_mul(source):
    url = "/" + source
    return redirect(url)

@main.route("/save_paper_mul", methods=["POST"])
def save_paper_mul():
    if request.method == "POST":
        down_image = request.form.get('down_image')
        
    return send_file(down_image, as_attachment=True)

# CLOSE THESIS
@main.route("/<source>")
def close_thesis_mul(source):
    url = "/" + source
    return redirect(url)

@main.route("/save_paper_mul", methods=["POST"])
def save_thesis_mul():
    if request.method == "POST":
        down_image = request.form.get('down_image')
        
    return send_file(down_image, as_attachment=True)

# INIT PROJECT
if __name__ == '__main__':
    db.create_all(app=create_app()) # create the SQLite database
    # start the flask app
    app.run(debug=True, use_reloader=True)
    # app.run(host="0.0.0.0", port="5000", debug=True, threaded=True, use_reloader=True)