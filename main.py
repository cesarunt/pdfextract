# -*- coding: utf_8 -*-
import os, re, json
from flask import Blueprint, render_template, request, redirect, jsonify, send_file, send_from_directory, Response
from requests import post
from sqlalchemy import true
from utils.config import cfg
from utils.handle_files import allowed_file, get_viewProcess_CPU
from werkzeug.utils import secure_filename
from scripts.split import pdf_splitter, split_thumb, split_img, split_img_qr, pdf_getNpages
from scripts.process import pdf_process
from scripts.search import pdf_search
from scripts.qrcode import qr_read
from datetime import datetime
from datetime import date
from utils.sqlite_tools import *
from utils.process_doc import *
from __init__ import create_app, db

import cv2
from PIL import Image
import pytesseract, unidecode
from docx import Document
from fold_to_ascii import fold
from flask_login import current_user
from wtforms import TextField, Form
from pdf2image import convert_from_path
from PyPDF2 import PdfFileReader

main = Blueprint('main', __name__)

# app = Flask(__name__)
app = create_app() # we initialize our flask app using the __init__.py function
app.jinja_env.auto_reload = True
app.config['MAX_CONTENT_LENGTH'] = cfg.FILES.MAX_CONTENT_LENGTH
app.config['UPLOAD_EXTENSIONS']  = cfg.FILES.UPLOAD_EXTENSIONS
app.config['QR_EXTENSIONS']     = cfg.FILES.QR_EXTENSIONS
app.config['UPLOAD']            = cfg.FILES.UPLOAD
app.config['QR_UPLOAD']         = cfg.FILES.QR_UPLOAD
app.config['SPLIT_PDF']         = cfg.FILES.SPLIT_PDF
app.config['SPLIT_IMG']         = cfg.FILES.SPLIT_IMG
app.config['SPLIT_IMG_WEB']     = cfg.FILES.SPLIT_IMG_WEB
app.config['SPLIT_THUMB']       = cfg.FILES.SPLIT_THUMB
app.config['SPLIT_THUMB_WEB']   = cfg.FILES.SPLIT_THUMB_WEB
app.config['OUTPUT']            = cfg.FILES.OUTPUT
app.config['FORWEB']            = cfg.FILES.FORWEB
app.config['UPLOAD_WEB']        = cfg.FILES.UPLOAD_WEB
app.config['QR_UPLOAD']         = cfg.FILES.QR_UPLOAD
# app.config['QR_VOUCHER_WEB']    = cfg.FILES.QR_VOUCHER_WEB
app.config['QR_IMG']            = cfg.FILES.QR_IMG
app.config['QR_IMG_WEB']        = cfg.FILES.QR_IMG_WEB
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Allowed extension you can set your own
LANGUAGE_PAGE = "es"
ALLOWED_EXTENSIONS = set(['PDF', 'pdf'])
ILLEGAL_XML_CHARS_RE = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1F\uD800-\uDFFF\uFFFE\uFFFF]")
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
pytesseract.pytesseract.tesseract_cmd = cfg.FILES.GLOBAL_TESSERACT


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

def allowed_files(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class SearchForm(Form):
    autocomp = TextField('Busca palabras claves', id='keyword_autocomplete')

# ------------------------------------ ROUTING ------------------------------------
# Home
# ====
@main.route('/home')
def home():
    if current_user.is_authenticated:
        list_projects = get_listProjects(5, current_user.id)
        print("current_user", current_user.id)
        crumb = { 'band':0, 'pre': '', 'post': "Portada" }
        return render_template('home.html', name=current_user.name.split()[0], projects=list_projects, crumb=crumb)
    else:
        return render_template('login.html')

"""
    USERS LOGIN 
    =====================
"""
@main.route('/user/create/<id>')
def user_create(id):
    if current_user.is_authenticated:
        list_userOne = get_userById(id)
        result = {
                'view': "d-none",
                'alert': "",
                'message': ""
            }
        crumb = { 'band':1, 'pre': 'Usuarios', 'post': "Registro" }
        return render_template('user_form.html', name=current_user.name.split()[0], crumb=crumb, user=list_userOne[0], result=result, admin=current_user.id)
    else:
        return render_template('login.html')

@main.route("/user/active/<int:val>/<int:id>")
def user_active(val, id):
    if current_user.is_authenticated:
        # Enable active from user
        response_user = upd_statusUserById(id, int(val))
        if response_user is True and val == 1:
            result = {
                'view': "", 'alert': "alert-success",
                'message': "Usuario Habilitado con éxito"
            }
        if response_user is True and val == 0:
            result = {
                'view': "", 'alert': "alert-danger",
                'message': "Usuario Inhabilitado con éxito"
            }
        # print("Usuario Actualizado con éxito")
        list_users = get_listUsers(10)
        crumb = { 'band':1, 'pre': 'Usuarios', 'post': "Listado" }
        return render_template('user_list.html', name=current_user.name.split()[0], users=list_users, crumb=crumb, result=result, admin=current_user.id)


@main.route("/user/update/", methods=["POST"])
def user_update():
    # id = 0
    user = None
    response_user = False
    if request.method == 'POST':
        current_date = date.today().strftime("%d-%m-%Y")
        action = request.form['action']
        val = request.form['val']

        user = {
                'usr_id':       int(request.form['id']),
                'usr_name':     request.form['name'],
                'usr_gender':   request.form['gender'],
                'usr_email':    request.form['email'],
                'usr_birthday': request.form['birthday'],
                'usr_address':  request.form['address'],
                'usr_phone':    request.form['phone'],
                'usr_active':   request.form['active'],
                'usr_updated':  current_date,
            }

        if action == 'H' or action == 'I':
            # Enable active from user
            response_user = upd_statusUserById(user['usr_id'], int(val))
 
            if response_user is True and action == 'H':
                result = {
                    'view': "", 'alert': "alert-success",
                    'message': "Usuario Habilitado con éxito"
                }
            if response_user is True and action == 'I':
                result = {
                    'view': "", 'alert': "alert-danger",
                    'message': "Usuario Inhabilitado con éxito"
                }
            print("Usuario Actualizado con éxito")

        if action == 'G':
            # Update the current user
            response_user = upd_userById(user)
            if response_user is True:
                result = {
                    'view': "", 'alert': "alert-success",
                    'message': "Usuario actualizado con éxito"
                }
                print("Usuario Actualizado con éxito")
            else:
                result = {
                    'view': "", 'alert': "alert-warning",
                    'message': "Usuario NO fue actualizado"
                }
                print("ERROR Actualizando Usuario")
        
        crumb = { 'band':1, 'pre': 'Usuarios', 'post': "Registro" }
        return render_template('user_form.html', name=current_user.name.split()[0], user=user, crumb=crumb, result=result, admin=current_user.id)


@main.route('/user/list')
def user_list():
    if current_user.is_authenticated:
        list_users = get_listUsers(10)
        result = {
                'view': "d-none",
                'alert': "",
                'message': ""
            }
        crumb = { 'band':1, 'pre': 'Usuarios', 'post': "Listado" }
        return render_template('user_list.html', name=current_user.name.split()[0], users=list_users, crumb=crumb, result=result, admin=current_user.id)
    else:
        return render_template('login.html')

@main.route('/province/<department>')
def province(department):
    list_provinces = get_listProvinces(department)
    return jsonify({'provinces': list_provinces})

@main.route('/district/<province>/province/<department>')
def district(province, department):
    list_districts = get_listDistricts(province, department)
    return jsonify({'districts': list_districts})

@main.route('/create/upload')
def upload_form():
    if current_user.is_authenticated:
        list_universities = get_listUniversities()
        list_departments = get_listDepartments()
        list_keywords = get_listKeywords()
        one_project = []
        key_id = ""
        crumb = { 'band':1, 'pre': 'Proyectos', 'post': "Registro" }
        return render_template('upload_form.html', name=current_user.name.split()[0], project=one_project, key_id=key_id, universities=list_universities, departments=list_departments, keywords=list_keywords, crumb=crumb)
    else:
        return render_template('upload_form.html')

@main.route('/edit/update/<id>')
def update_form(id):
    if current_user.is_authenticated:
        list_universities = get_listUniversities()
        list_departments = get_listDepartments()
        one_project = get_projectById(id)
        list_keywords = get_listKeywords()
        list_keywordsOne = get_listKeywordsById(id)
        list_keywordsOneId = [val['key_id'] for val in list_keywordsOne]
        key_id = ""
        list_provinces = get_listProvinces(one_project[0]['pro_department'])
        list_districts = get_listDistricts(one_project[0]['pro_province'], one_project[0]['pro_department'])
        return render_template('upload_form.html', name=current_user.name.split()[0], project=one_project[0], key_id=key_id, universities=list_universities, departments=list_departments, provinces=list_provinces, districts=list_districts, keywords=list_keywords, keywordsOne=list_keywordsOne, keywordsOneId=list_keywordsOneId, pro_id=id)
    else:
        return render_template('upload_form.html')

@app.route('/create/upload', methods=['GET', 'POST'])
def upload_form():
    form = SearchForm(request.form)
    return render_template("upload_form.html", keywords_form=form)


@main.route('/upload/home/<id>')
def upload_home(id):
    global pro_id
    pro_id = id
    global type_doc
    type_doc = "T"  # DOC type on Project
    
    if current_user.is_authenticated:
        one_project = get_projectById(id)
        list_keywordsOne = get_listKeywordsById(id)
        return render_template('upload_home.html', name=current_user.name.split()[0], project=one_project[0], keywordsOne=list_keywordsOne, pro_id=id)
    else:
        return render_template('upload_home.html')

# Thesis
# ======
@main.route('/thesis_one')
def thesis_one():
    if current_user.is_authenticated:
        return render_template('thesis_one.html', name=current_user.name.split()[0])
    else:
        return render_template('thesis_one.html')

@main.route('/thesis_mul/<id>')
def thesis_mul(id):
    if current_user.is_authenticated:
        one_project = get_projectById(id)
        return render_template('thesis_mul.html', name=current_user.name.split()[0], project=one_project[0], pro_id=id)
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
    keywords = ""
    if request.method == 'POST':
        current_date = date.today().strftime("%d-%m-%Y")
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
            'title_search' :unidecode.unidecode(request.form['title']),
            'university' :  request.form['university'],
            'department' :  request.form['department'],
            'province' :    request.form['province'],
            'district' :    request.form['district'],
            'career' :      request.form['career'],
            'comment' :     request.form['comment'],
            'type_a' :      type_a,
            'type_m' :      type_m,
            'n_articles':   0,
            'n_process':    0,
            'user' :        user_id,
            'created' :     current_date
        }
        k_out = request.form['keywords_out']
        k_out = k_out.replace('[','').replace(']','')
        if k_out=='':
            keywords = None
        else:
            keywords = request.form['keywords_out'].split(',')
        save_type = request.form['save_type']
        if save_type == "new" :
            project['updated'] = current_date
            response_project, id = put_newProject(project)
            if response_project is True:
                if keywords != None:
                    for key in keywords:
                        response_pkdetail = put_newPKdetail(id, key, current_date)
        else:
            id = request.form['save_id']
            project['updated'] = current_date
            response_project = upd_projectById(id, project)
            if response_project is True:
                if keywords != None:
                    for key in keywords:
                        response_pkdetail = put_newPKdetail(id, key, current_date)
        return redirect('/upload/home/'+str(id))

@main.route('/last_variable')
def last_variable():
    key_id = get_lastVariable()
    return jsonify({'key_id': key_id})

@main.route("/add_variable", methods=["POST"])
def add_variable():
    action = request.values.get("action")

    if request.method == 'POST' and action == 'add':
        current_date = date.today().strftime("%d-%m-%Y")
        value = request.values.get("value")
        try:
            response_key, response_id = put_newKeyword(value, current_date)
            if response_key is True:
                # msg_variable = "Variable registrada con éxito"
                key_id = response_id
                _, _ = put_newPDFattribute(str(response_id)+"_"+'definición', "M", current_date)
                _, _ = put_newPDFattribute(str(response_id)+"_"+'importancia', "M", current_date)
                _, _ = put_newPDFattribute(str(response_id)+"_"+'modelos',      "M", current_date)
                _, _ = put_newPDFattribute(str(response_id)+"_"+'conceptos', "M", current_date)
        except:
            print("Error en registro de variable")
        finally:
            return jsonify({'key_id': key_id})

@main.route('/get_attributes/<pro_id>/<pdf_id>')
def get_attributes(pro_id, pdf_id):
    list_attributes = get_attributesDetails(pro_id, pdf_id)
    return jsonify({'attributes': list_attributes})

"""
    FORM SEARCH DATABASES
    =====================
"""
@main.route('/search_db')
def search_db():
    if current_user.is_authenticated:
        crumb = { 'band':1, 'pre': 'Proyectos', 'post': "Búsqueda" }
        return render_template('db_form.html', name=current_user.name.split()[0], crumb=crumb, n_projects = 0, keyword = "", typedoc = "A", typeAnac = '1', typeAint = '1', bydoc = '1')
    else:
        return render_template('db_form.html')

@main.route("/search_db", methods=["POST"])
def search_db_post():
    num_projects = 0
    list_projects = None

    if current_user.is_authenticated:
        if request.method == "POST":
            bydoc = request.values.get("bydoc")
            keyword = request.values.get("keyword_search")
            typedoc = request.values.get("typedoc")
            bydate = request.values.get("bydate")
            startDate = request.values.get("startDate")
            endDate = request.values.get("endDate")
            if (typedoc=='A' or typedoc=='M'):
                typeAnac = request.values.get("type_a_nac")
                typeAint = request.values.get("type_a_int")

            if len(keyword) > 1:
                keyword_list, keyword_trans = pdf_search(str(keyword), cfg.FILES.GLOBAL_PATH)
                list_projects = get_squareProjects_ByWord(bydoc, keyword_list, typedoc, typeAnac, typeAint, bydate, startDate, endDate)
                num_projects = len(list_projects)
        crumb = { 'band':1, 'pre': 'Proyectos', 'post': "Búsqueda" }
        return render_template('db_form.html', name=current_user.name.split()[0], crumb=crumb, n_projects = num_projects, projects = list_projects, keyword_search = keyword, keyword_trans = keyword_trans, typedoc = typedoc, typeAnac = typeAnac, typeAint = typeAint, bydoc = bydoc)
    else:
        return render_template('db_form.html', keyword = "")

@main.route("/create_db", methods=["POST"])
def create_db_post():
    result_total = False

    if current_user.is_authenticated:
        if request.method == "POST":
            action = request.form.get('btn_action')
            
            if action == 'C':
                process = request.form.get('process')
                _pdfs = request.form.getlist('pdfs')
                user_id = current_user.id
                if process == '1' and len(_pdfs) > 0:
                    complete_date = datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
                    current_date = date.today().strftime("%d-%m-%Y")
                    project = {
                            'title' :      "Nuevo proyecto, creado el " + complete_date,
                            'title_search': unidecode.unidecode(request.form['title']),
                            'university' :  1,
                            'department' :  10,
                            'province' :    1001,
                            'district' :    100101,
                            'career' :      "",
                            'comment' :     "",
                            'type_a' :      1,
                            'type_m' :      1,
                            'n_articles':   0,
                            'n_process':    1,
                            'user' :        user_id,
                            'created' :     current_date,
                            'updated' :     current_date
                        }
                    pro_result, pro_id = put_newProject(project)
                    
                    for _pdf in _pdfs:
                        item = _pdf.split("_")
                        pro_pdf_id  = item[0]
                        pdf_id     = item[1]
                        pdf_type  = item[2]
                        pdf_year = item[3]
                        
                        pdf_info = get_pdfInfoById(pdf_id)
                        pdf_detail = get_pdfDetailById(pro_pdf_id, pdf_id)
                        pdf = {
                                'name' :     pdf_info[0],
                                'npages' :   pdf_info[1],
                                'size' :     pdf_info[2],
                                'created' :  current_date
                            }
                        
                        if pro_result:
                            pdf_info_id = put_newPDF(pdf)
                            result = put_newPPdetail(pro_id, pdf_info_id, pdf_detail[1], pdf_detail[2], pdf_detail[3], pdf_detail[4], pdf_id, pdf_detail[5], pdf_detail[6], 1, current_date)
                        if result == True:
                            if pdf_type == "A":
                                put_newPDFdetail(pdf_info_id, 1, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 2, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 3, pdf_year, 1, 1)
                                put_newPDFdetail(pdf_info_id, 4, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 5, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 6, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 7, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 8, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 9, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 10, "", int(pdf['npages'])-1, 1)
                                put_newPDFdetail(pdf_info_id, 11, "", int(pdf['npages'])-1, 1)
                                put_newPDFdetail(pdf_info_id, 12, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 13, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 14, "http://", int(pdf['npages']), 1)
                                put_newPDFdetail(pdf_info_id, 15, "_", 1, 1)
                            if pdf_type == "M":
                                put_newPDFdetail(pdf_info_id, 16, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 17, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 18, pdf_year, 1, 1)
                                put_newPDFdetail(pdf_info_id, 19, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 20, "", 1, 1)
                                put_newPDFdetail(pdf_info_id, 21, "http://", int(pdf['npages']), 1)
                                put_newPDFdetail(pdf_info_id, 22, "", 1, 1)
                            result_total = True

                    if result_total == True :
                        print("El nuevo proyecto fue creado con éxito")
                        one_project = get_projectById(pro_id)
                        list_keywordsOne = get_listKeywordsById(pro_id)
                        return render_template('upload_home.html', name=current_user.name.split()[0], project=one_project[0], keywordsOne=list_keywordsOne, pro_id=pro_id)

            if action == 'D':
                document = Document()
                pdfs = dict()
                _pdfs = request.form.getlist('pdfs')
                user_id = current_user.id
                
                if len(_pdfs) > 0:
                    now = datetime.datetime.now()
                    i = 0
                    _atts = []
                    for _pdf in _pdfs:
                        item = _pdf.split("_")
                        pro_pdf_id  = item[0]
                        pdf_id     = item[1]
                        pdf_type  = item[2]
                        pdf_year = item[3]
                        _atts = request.form.getlist('attributes_'+pro_pdf_id+'_'+pdf_id)
                        text_schemes = get_pdfDetailByIds(pro_pdf_id, pdf_id, tuple(_atts))

                        for detail in text_schemes['foundlist']:
                            pdfs[detail['det_name']] = detail['det_value']
                        
                        if (pdfs['título']=='') : pdfs['título']=='<<Título>>'
                        if (pdfs['autor']=='') : pdfs['autor']=='<<Autor>>'
                        if (pdfs['año']=='') : pdfs['año']=='<<Año>>'
                        if pdf_type == 'A':
                            document, i = build_pdfA(text_schemes, document, i)
                        if pdf_type == 'M':
                            document, i = build_pdfMT(text_schemes, document, i)
                    
                    file_save = app.config['OUTPUT']+'/exportPDFs_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
                    document.save(file_save)
                    result_pdf = app.config['FORWEB']+'/exportPDFs_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
                    if result_pdf:
                        return send_file(result_pdf, as_attachment=True)  
    else:
        return render_template('db_form.html', keyword = "")

@app.route('/files/split_thumb/<filename>')
def thesis_split_thumb(filename):
    return send_from_directory(app.config['SPLIT_THUMB'], filename)

@app.route('/files/split_img/<filename>')
def thesis_split_img(filename):
    return send_from_directory(app.config['SPLIT_IMG'], filename)


# FUNCTION TO UPLOAD PDF 
# ======================
@main.route('/thesis_mul', methods=['POST'])
def thesis_mul_load():
    global file_pdfs
    global pdf_ids
    # aqui hay que crear un nuevo ARRAY para almacenar los pdf_ids (pdf_info_id)
    pdf_info_id = None
    upload = False
    pdf_ids = []

    if request.method == "POST":
        file_pdfs = []
        pro_id = request.form.get('pro_id')
        # Code for multiple pdfs
        if 'files[]' not in request.files:
            return redirect(request.url)

        current_date = date.today().strftime("%d-%m-%Y")
        pdfs = []
        files = request.files.getlist('files[]')
        
        # 1. Remove and split IMG
        for file in files:
            if file and allowed_file(file.filename, app.config["UPLOAD_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                path = os.path.join(app.config['UPLOAD'], filename)
                path = validate_path(path)
                path = path.replace('(','').replace(')','').replace(',','').replace('<','').replace('>','').replace('?','').replace('!','').replace('@','').replace('%','').replace('$','').replace('#','').replace('*','').replace('&','').replace(';','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace('=','').replace('+','').replace(' ','_')
                file_pdfs.append(path.split("/")[-1])
                file.save(path)
                upload = True

                # Put data on pdf_info
                pdf_size = os.path.getsize(path)
                pdf_npages = pdf_getNpages(path)

                if pdf_npages > 0 :
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
                        pdf_ids.append(pdf_info_id)
                        result_thumb = split_thumb(path, app.config['SPLIT_THUMB'], pdf_info_id)   # Call img splitter function
                        pdf['pdf_id'] = pdf_info_id
                        pdf['pdf_path'] = app.config['SPLIT_THUMB_WEB'] + '/' + str(pdf_info_id) + 'page_'
                        pdf['file_path'] = path
                        pdfs.append(pdf)
                else:
                    continue
        
        for pdf in pdfs:
            result_img = split_img(pdf['file_path'], app.config['SPLIT_IMG'], pdf['pdf_id'])   # Call img splitter function
            if result_img == 1:
                pdf['pdf_path_img'] = app.config['SPLIT_IMG_WEB'] + '/' + str(pdf['pdf_id']) + 'page_'

        if (upload == True):
            one_project = get_projectById(pro_id)
            print('File(s) successfully uploaded')
            return render_template('thesis_mul.html', resultLoad=upload, pdfs = pdfs, project=one_project[0], pro_id=pro_id)


# READ QR
# =======
@app.route('/files/qr_upload/<filename>')
def qr_upload(filename):
    return send_from_directory(app.config['QR_UPLOAD'], filename)

@app.route('/files/qr_img/<filename>')
def qr_img(filename):
    return send_from_directory(app.config['QR_IMG'], filename)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
@main.route('/qr')
def qr():
    global data_code
    global files_img
    files_img = []
    data_code = []
    print("HOME")
    if current_user.is_authenticated:
        return render_template('qr.html', result_upload = True, result_process = False, name=current_user.name.split()[0])
    if len(data_code)==0:
        return render_template('qr.html', result_upload = True, result_process = False)

@main.route('/qr', methods=['POST'])
def qr_post():
    global files_img
    global data_code
    global len_files
    result_process = False

    if request.method == "POST":
        result_img = False
        result_pdf = False
        result_type = ""
        len_data = 0
        
        if 'files[]' not in request.files:
            print("NOT FILES")
            return redirect(request.url)

        current_date = date.today().strftime("%d-%m-%Y")
        files = request.files.getlist('files[]')
        
        # 1. Remove and split IMG
        for file in files:
            if file and allowed_file(file.filename, app.config["QR_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                filename = filename.replace('(','').replace(')','').replace(',','').replace('<','').replace('>','').replace('?','').replace('!','').replace('@','').replace('%','').replace('$','').replace('#','').replace('*','').replace('&','').replace(';','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace('=','').replace('+','').replace(' ','_')
                path = os.path.join(app.config['QR_UPLOAD'], filename)
                path = validate_path(path)
                file.save(path)
                # Verify Image Name and Extension
                filename = path.split("/")[-1]
                file_ext = path.split(".")[-1]

                if (file_ext.upper()=='JPG' or  file_ext.upper()=='JPEG'):
                    file_image = cv2.imread(path)
                    # print(file_image)
                    image_width  = 0
                    image_height = 0

                    if int(file_image.shape[1])>int(file_image.shape[0]):
                        image_height = 500
                        image_width = 740
                    else:
                        file_width  = file_image.shape[1]
                        file_height = file_image.shape[0]
                        fw = float(int(file_height) / int(file_width))
                        if fw > 2.0:
                            image_width = 420
                            image_height = 900
                        elif fw > 1.75:
                            image_width = 480
                            image_height = 900
                        else:
                            image_width = 640
                            image_height = 900
                    # SAVE and ready to read by QR
                    path = os.path.join(app.config['QR_IMG'], filename)
                    file_resize = cv2.resize(file_image, (image_width, image_height), interpolation = cv2.INTER_AREA)
                    cv2.imwrite(path, file_resize, [cv2.IMWRITE_JPEG_QUALITY, 90])
                    result_img = True
                elif (file_ext.upper()=='PDF'):
                    # Extract IMG, SAVE IMG and ready to read by QR
                    result_pdf, filename = split_img_qr(path, app.config['QR_IMG'])
                                        
                if result_img==True:
                    result_type = "JPG"
                else:
                    result_type = "PDF"

                my_image = {
                    'name' :    filename,
                    'type'  :   result_type,
                    'created':  current_date
                }
                files_img.append(my_image)
        len_files = len(files_img)

        if len_files > 0:
            # result = True
            len_files = len_files + 1
            print("RENDER ...")
            print(result_process)
            return render_template('qr.html', result_upload = False, result_process = result_process, data_code = data_code, data_len = len_files)
        else:
            return redirect(request.url)
        

@main.route('/qr_action', methods=['POST'])
def qr_action():
    global files_img
    global data_code
    global len_files
    data_qr = None
    # data_code = None
    result_qr = ""
    result_process = True

    if request.method == "POST":
        action = request.values.get("action")

        if len(files_img) > 0 :
            # index = int(request.values.get("index"))-1
            print("len files Img: ", len(files_img))
            
            divisor = 10
            if len(files_img)>divisor:
                limit = divisor
            else:
                mod_file = len(files_img) % divisor
                limit = mod_file

            files = []
            files = files_img[0:limit]
            data_code = []

            i = 0
            for file in files:
                if file["type"]=="JPG":
                    filename = app.config['QR_UPLOAD'] + "/" + file["name"]
                else:
                    filename = app.config['QR_IMG'] + "/" + file["name"]

                if filename:
                    result_qr, data_qr = qr_read(filename)
                    if result_qr == "OK":
                        index = int(len_files - len(files_img))
                        data_qr["index"] = index
                        data_qr["currency"] = "S"
                        data_qr["type_doc"] = "F"
                        if data_qr["path"] == "":
                            data_qr["path"] = app.config['QR_IMG_WEB'] + "/" + file["name"]
                        data_code.append(data_qr)
                        del files_img[0]
                        i = i + 1
                        print('...............File(s) IMG generated successfully............\n')
            
            return jsonify({'data_code': data_code})
            
        else:
            data_code = []
            return jsonify({'data_code': data_code })
               
            # len_data = len(data_code)
            # if result_process:
            #     result_process = False
            #     return render_template('qr.html', result_upload = False, result_process = False, data_code = data_code, data_len = len_data)
            # else:
            #     print("len_data", len_data)
            #     return jsonify({'data_code': data_code})
            
        # return render_template('qr.html', result_upload = False, result_process = False, data_code = data_code, data_len = len_data)


@main.route('/qr_canvas', methods=['POST'])
def qr_canvas():
    global files_img
    text_canvas = ""
    result_save = False
    result_canvas = False
    # data_code = []
    if request.method == "POST":
        # ---------------------------------------
        # Read Action
        action = request.values.get("action")

        if action == "save_voucher":
            index = int(request.values.get("index"))-1
            data_code[index]['cli_dat']  = request.values.get("data_dat")
            data_code[index]['currency'] = request.values.get("data_cur")
            data_code[index]['type']     = request.values.get("data_type")
            data_code[index]['cli_fac']  = request.values.get("data_bill")
            data_code[index]['cia_ruc']  = request.values.get("data_ciaruc")
            data_code[index]['cli_ruc']  = request.values.get("data_cliruc")
            data_code[index]['cli_tot']  = request.values.get("data_tot")
            data_code[index]['cli_igv']  = request.values.get("data_igv")
            data_code[index]['is_full']  = 1
            result_save = True
        
        if action == "get_canvas":
            index = int(request.values.get("index"))
            path = request.values.get("path")
            current_date = date.today().strftime("%d-%m-%Y")
            dictCanvas = json.loads(request.values.get("dictCanvas"))
            i = 0
            text = ""
            image = None
            for dictVal in dictCanvas:
                i += 1                
                image = app.config['QR_IMG'] + '/' + str(path).split("/")[-1]
                print("image path", image)
                image = cv2.imread(image, 0)
                _y = dictVal['y']
                _h = dictVal['h']
                _x = dictVal['x']
                _w = dictVal['w']
                ROI = image[_y: _y + _h, _x: _x + _w]
                language = "spa"
                try:
                    text_canvas = pytesseract.image_to_string(ROI, lang=language, config='--psm 6')
                    result_canvas = True
                    print("TEXT FINAL,", text_canvas)
                except Exception as e:
                        print(e)
                        print("Error generate text...")
        
        if result_save:
            return jsonify({'data_code': data_code})
        if result_canvas:
            return jsonify({'data_code': text_canvas})

        # else:
        #     len_data = len(data_code)
        #     print("len_data", len_data)
        #     if len_data > 0 :
        #         return render_template('qr.html', result_upload = False, result_process = False, data_code = data_code, data_len = len_data)
        #     else:
        #         return redirect(request.url)

# ////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# FUNCTION TO PROCESS PDF 
# 
@main.route("/action_thesis_mul", methods=["POST"])
def action_thesis_mul():
    global file_pdfs
    global pdf_ids
    pdfs = {}

    if request.method == "POST":
        global file_pdf, document
        resultCPU = False
        action = None
        band_parcial = False
        result_save = None
        result_file_text = "None"
        result_invalid_text = ""
        result_file_down = "None"
        result_split = 0
        result_valid = 0
        result_invalid = 0
        result_invalid_process = []
        
        pro_id = request.form.get('pro_id')
        process = request.form.get('process')
        _pages = request.form.getlist('page')
        pdfs_remove = request.form.get('pdfs_remove')

        if process == '1' and len(_pages) > 0:
            temp_page = ""
            for _page in _pages:
                item = _page.split("_")
                if temp_page != item[0]:
                    pages = []
                    temp_page = item[0]
                pages.append(int(item[1]))
                pdfs[item[0]] = pages
            band_parcial = True
        
        # Verify if posible to process
        if get_viewProcess_CPU() is True :
            document = Document()
            # print("NumPDFs Cargados", len(file_pdfs))
            if len(pdfs_remove):
                pdfs_remove = pdfs_remove.split("/")
                for pdf_rem in pdfs_remove :
                    if pdf_rem != "":
                        file_pdfs.remove(pdf_rem)

            i = 0
            for filename in file_pdfs :
                filename = fold(filename)
                path = os.path.join(app.config['UPLOAD'],filename)
                path = validate_path(path)
                path = path.replace('(','').replace(')','').replace(',','').replace('<','').replace('>','').replace('?','').replace('!','').replace('@','').replace('%','').replace('$','').replace('#','').replace('*','').replace('&','').replace(';','').replace('{','').replace('}','').replace('[','').replace(']','').replace('|','').replace('=','').replace('+','').replace(' ','_')
                action = request.values.get("action")

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

                    # print("ROI_language", LANGUAGE_PAGE)
                    if LANGUAGE_PAGE=="es":
                        language = "spa"
                    else:
                        language = "eng"
                    text = ""
                    try:
                        text = pytesseract.image_to_string(ROI, lang=language, config='--psm 6')
                    except Exception as e:
                        print(e)
                        print("Error generate text")
                    
                    if text is None or text == "":
                        text = "..."
                    result1 = upd_detailCanvasByIds(det_id, pdf_id, det_attribute, text, page, rect)
                    result_split = 1
                
                if action == "make_zoom":
                    print("ZOOM for thesis POST")
                
                if action == "save_text":
                    det_id =        int(request.values.get("det_id"))
                    det_attribute = int(request.values.get("det_attribute"))
                    det_value =     request.values.get("det_value")
                    page =          int(request.values.get("page"))
                    
                    # if text is None or text == "":
                    #     text = "..."
                    result_detail = upd_detailTextByIds(det_id, pdf_id, det_attribute, det_value, page)
                    if result_detail is True and (det_attribute==1 or det_attribute==16):
                        pdf_name_search = unidecode.unidecode(det_value)
                        _ = upd_detailPDFnameByIds(pro_id, pdf_id, det_value, pdf_name_search)
                    result_split = 1
                
                # if action == "save_attribute":
                #     current_date = date.today().strftime("%d/%m/%Y")
                #     att_value =  request.values.get("new_att")
                
                if action == "remove_attribute":
                    det_id = int(request.values.get("det_id"))
                    
                    try:
                        response_pdf = del_attributeById(det_id)
                        if response_pdf is True:
                            msg_pdf = "PDF detail eliminado con éxito"
                    except:
                        msg_pdf = "Error en eliminación de PDFdetail"
                    
                    finally:
                        result_split = 1

                # 1. SPLIT PDF
                if action is None:
                    if band_parcial == True:
                        pdf_info_id = list(pdfs.items())[i][0]
                    else:
                        pdf_info_id = pdf_ids[i]
                    # 1. Remove and split PDF
                    result_split, pdf_npages = pdf_splitter(path, app.config['SPLIT_PDF'], pdf_info_id, pdfs)   # Call pdf splitter function
                
                if result_split == -1 and pdf_npages == 0:
                    continue
                else:
                    type_name = "type_" + str(pdf_info_id)
                    type_val = request.form.get(type_name)
                    nation_name = "nation_" + str(pdf_info_id)
                    nation_val = request.form.get(nation_name)
                    
                    if result_split == 0:
                        result_invalid += 1
                        result_invalid_process.append(filename + " ...NO se procesó")
                    if result_split == 2:
                        result_invalid += 1
                        result_invalid_process.append(filename + " ...supera el Nro páginas")
                    if result_split == 1:
                        pdf_attributes = []
                        # Put data on pdf_info
                        current_date = date.today().strftime("%d-%m-%Y")
                        if type_val == 'M':
                            sqliteConnection = sqlite3.connect(data_base)
                            cursor = sqliteConnection.cursor()
                            pdf_attributes = get_proKeyById(cursor, 'project_info', pro_id)
                            nation_val = "ON"
                                            
                        # 2. Process PDF
                        language, title_text = pdf_process(app.config['SPLIT_PDF'], pdf_attributes, pdf_info_id, pdfs, pdf_npages, type_val)  # Call pdf process function
                        LANGUAGE_PAGE = language
                        title_search = unidecode.unidecode(title_text)
                        result_valid = 1
                    
                    if result_valid > 0 :
                        result_save = True
                        try:
                            _ = put_newPPdetail(pro_id, pdf_info_id, title_text, title_search, type_val, nation_val, 0, pdfs[pdf_info_id], pdf_attributes, 1, current_date)
                        except:
                            print("Error en registrar en PRO PDF detail")

                    if result_invalid > 0 and result_valid == 0 :
                        result_save = False
                        result_file_text = "No fue posible procesar"
                    if len(result_invalid_process) > 0 :
                        result_invalid_text = (',  \n'.join(result_invalid_process))
                    i = i + 1
            
            # Save results on database, Get data from project_info
            project = get_projectById(pro_id)
            project01 = project[0]
            n_process = int(project[0]["pro_n_process"]) + 1

            # Put data on pro_pdf_details, Update data on project_info
            saveDB = upd_projectProcess(pro_id, result_valid, n_process)
            if saveDB is True:
                print("Se actualizó con éxito project_info")
                    
        else:
            project01 = None
            result_file_text = "El servidor está procesando, espere un momento."
    
    return render_template('thesis_mul.html', result_save=result_save, result_file_text=result_file_text, result_invalid_text=result_invalid_text, result_file_down = result_file_down, project=project01, pro_id=pro_id)

"""
    PROJECT PDF 
    =====================
"""
@main.route('/project/list')
def project_list():
    if current_user.is_authenticated:
        list_projects = get_listProjects(-1, current_user.id)
        crumb = { 'band':1, 'pre': 'Proyectos', 'post': "Listado" }
        return render_template('project_list.html', name=current_user.name.split()[0], projects=list_projects, crumb=crumb)
    else:
        return render_template('login.html')

@main.route('/project/<id>')
def project_pdfs(id):
    global pro_id
    pro_id = id
    global type_doc
    type_doc = "T"  # DOC type on Project
    if current_user.is_authenticated:
        project = get_projectById(id)
        pdfs = get_projectsById(id, type_doc)
        return render_template('project_pdfs.html', name=current_user.name.split()[0], pdfs=pdfs, pdf_type=type_doc, pdf=None, project=project[0], pro_id=id)
    else:
        return render_template('project_pdfs.html')

@main.route('/<pdf_id>')
def project_pdf(pdf_id):
    listpages = []

    if current_user.is_authenticated:
        project = get_projectById(pro_id)
        pdfs = get_projectsById(pro_id, type_doc)
        pdf = get_pdfDetailByIds(pro_id, pdf_id)

        # print("PDF", json.dumps(pdf))
        """Verificar pdf_details, encontrados y no encontradps"""
        pages_zero = str(pdf['pages']).replace('[','').replace(']','').replace(' ','')
        pages_list = pages_zero.split(',')

        for pag in pages_list:
            listpages.append(int(pag) + 1)
        pages_one = str(listpages).replace('[','').replace(']','').replace(' ','')

        pdf['pages_zero_text'] = pages_zero
        pdf['pages_one_text'] = pages_one
        pdf['pages_one_list'] = listpages
        # get data for pdf_file
        if int(pdf['double']) > 0:
            view_id = pdf['double']
        else:
            view_id = pdf_id
            
        pdf_path = {
                'name':        pdf['name'],
                'path_pdf':    app.config['UPLOAD_WEB'] + '/' + pdf['name'],
                'path_page':   app.config['SPLIT_IMG_WEB'] + '/' + str(view_id) + 'page_0.jpg',
                'num_pages':   int(pdf['npages']),
                }
        pdf['pdf_path'] = pdf_path
        # pdfs, for the left panel
        return render_template('project_pdfs.html', name=current_user.name.split()[0], pdfs=pdfs, pdf_len=len(pdfs), pdf_type=type_doc, pdf=pdf, project=project[0], pro_id=pro_id)
    else:
        return render_template('project_pdfs.html')


@main.route("/<pdf_id>", methods=["POST"])
def pdf_post(pdf_id):
    global file_pdfs
    global type_doc
    text_page = ""
    band_zoom = False
    dict_page = 0
    pro_id = request.values.get("pro_id")

    if request.method == "POST":
        action = request.values.get("action")

        if action == "save_canvas":
            det_id = int(request.values.get("det_id"))
            det_attribute = int(request.values.get("det_attribute"))
            current_date = date.today().strftime("%d-%m-%Y")
            dictCanvas = json.loads(request.values.get("dictCanvas"))
            i = 0
            text = ""
            dictPage = None
            for dictVal in dictCanvas:
                if i == 0:
                    dictPage = dictVal
                    page = int(dictVal['page'])
                i += 1
                images = []
                dict_page = int(dictVal['page'])
                path_pdf = app.config['SPLIT_PDF'] + '/' + str(pdf_id) + "page_" + str(dict_page) + ".pdf"
                images = convert_from_path(path_pdf, dpi=300, size=(640*2, 820*2))
                images[0].save(app.config['SPLIT_IMG'] + '/' + str(pdf_id) + 'page_'+ str(int(dict_page-1)) +'zoom.jpg',  format='JPEG', subsampling=0, quality=100)
                
                image = cfg.FILES.GLOBAL_PATH + '/' + app.config['SPLIT_IMG_WEB'] + '/' + str(pdf_id) + "page_" + str(int(dictVal['page'])-1) + "zoom.jpg"
                image = cv2.imread(image, 0)
                thresh = 255 - cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
                _y = dictVal['y'] * 2
                _h = dictVal['h'] * 2
                _x = dictVal['x'] * 2
                _w = dictVal['w'] * 2
                # ROI = thresh[dictVal['y']:dictVal['y']+dictVal['h'], dictVal['x']:dictVal['x']+dictVal['w']]
                ROI = thresh[_y: _y + _h, _x: _x + _w]
                
                # print("ROI_language", LANGUAGE_PAGE)
                if LANGUAGE_PAGE=="es":
                    language = "spa"
                else:
                    language = "eng"
                try:
                    text_page = pytesseract.image_to_string(ROI, lang=language, config='--psm 6')
                except Exception as e:
                        print(e)
                        print("Error generate text...")
                text = text + text_page + " "
            
            if text is None or text == "":
                text = ".."
            result_detail = upd_detailCanvasByIds(det_id, pdf_id, det_attribute, text, page, dictPage)
            if result_detail is True and (det_attribute==1 or det_attribute==16):
                pdf_name_search = unidecode.unidecode(text)
                _ = upd_PPdetail(pro_id, pdf_id, text, pdf_name_search, current_date)
            result_split = 1
        
        # if action == "make_zoom":
        #     print("ZOOM")
        #     det_id = int(request.values.get("det_id"))
        #     det_attribute = int(request.values.get("det_attribute"))
        #     current_date = date.today().strftime("%d-%m-%Y")
        #     dictCanvas = json.loads(request.values.get("dictCanvas"))
        
        if action == "save_text":
            det_id =        int(request.values.get("det_id"))
            det_attribute = int(request.values.get("det_attribute"))
            det_value =     request.values.get("det_value")
            page =          int(request.values.get("page"))
            
            result_detail = upd_detailTextByIds(det_id, pdf_id, det_attribute, det_value, page)
            if result_detail is True and (det_attribute==1 or det_attribute==16):
                pdf_name_search = unidecode.unidecode(det_value)
                _ = upd_detailPDFnameByIds(pro_id, pdf_id, det_value, pdf_name_search)
            result_split = 1
        
        if action == "save_attribute":
            current_date = date.today().strftime("%d-%m-%Y")
            att_value =  request.values.get("new_att")
            att_type =  request.values.get("det_type")
            response_att, id = put_newPDFattribute(att_value, att_type, current_date)
            if response_att is True:
                # msg_att = "Atributo registrado con éxito"
                response_pdf = put_newPDFdetail(pdf_id, id, "", 1, 1)
                if response_pdf is True:
                    msg_pdf = "PDF detail registrado con éxito"
                result_split = 1
        
        if action == "list_by_doc":
            type_doc = request.values.get("type_doc")
            result_split = 1

        if action == "remove_attribute":
            det_id = int(request.values.get("det_id"))
            response_pdf = del_attributeById(det_id)
            if response_pdf is True:
                # msg_pdf = "PDF detail eliminado con éxito"
                result_split = 1

        if action == "remove_pdf":
            pdf_detid = request.values.get("pdf_detid")
            response_pdf = del_PDF(pro_id, pdf_detid)
            if response_pdf is True:
                # msg_pdf = "PDF eliminado con éxito"
                result_split = 1
        
        if action == "edit_pdf":
            responde_del = False
            response_edit = False 
            pdf_details = []
            pdf_attributes = []
            list_attributes_del = []
            pro_id = request.values.get("pro_id")
            pdf_detid = request.values.get("pdf_detid")
            pdf_dettype = request.values.get("pdf_dettype")
            pdf_detnation = request.values.get("pdf_detnation")
            if pdf_dettype == 'M':
                pdf_nation = 'O' + pdf_detnation[-1]
                list_attributes_del = [*range(1, 16)]
            if pdf_dettype == 'A':
                pdf_nation = pdf_detnation[-1]
                list_attributes_del = [*range(16,23)]
            list_attributes_del = ','.join(str(item) for item in list_attributes_del)
            list_attributes_get = None

            # Insert values in "pdf_details", consider Title, Author, Year
            if pdf_dettype == "A":
                # Get values for Title, Author, Year
                list_attributes_get = (16, 17, 18)
                pdf_details = get_pdfDetailForDelete(pdf_detid, list_attributes_get)
                # Delete det_visible in "pdf_details"
                responde_del = del_attributeByProId(pdf_detid, list_attributes_del)
                if len(pdf_details)>0 and responde_del :
                    put_newPDFdetail(pdf_detid, 1, pdf_details[0][1], pdf_details[0][2], 1)
                    put_newPDFdetail(pdf_detid, 2, pdf_details[1][1], pdf_details[1][2], 1)
                    put_newPDFdetail(pdf_detid, 3, pdf_details[2][1], pdf_details[2][2], 1)
                    put_newPDFdetail(pdf_detid, 4, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 5, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 6, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 7, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 8, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 9, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 10, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 11, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 12, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 13, "", 1, 1)
                    put_newPDFdetail(pdf_detid, 14, "http://", 1, 1)
                    put_newPDFdetail(pdf_detid, 15, "..", 1, 1)
            if pdf_dettype == "M":
                key_att_ids = []
                # Get values for Title, Author, Year
                list_attributes_get = (1, 2, 3)
                pdf_details = get_pdfDetailForDelete(pdf_detid, list_attributes_get)
                # Delete det_visible in "pdf_details"
                responde_del = del_attributeByProId(pdf_detid, list_attributes_del)
                if len(pdf_details)>0 and responde_del :
                    sqliteConnection = sqlite3.connect(data_base)
                    cursor = sqliteConnection.cursor()
                    pdf_attributes = get_proKeyById(cursor, 'project_info', pro_id)
                    # nation_val = "ON"
                    if len(pdf_attributes) > 0:
                        # Insert values basics
                        put_newPDFdetail(pdf_detid, 16, pdf_details[0][1], pdf_details[0][2], 1)
                        put_newPDFdetail(pdf_detid, 17, pdf_details[1][1], pdf_details[1][2], 1)
                        put_newPDFdetail(pdf_detid, 18, pdf_details[2][1], pdf_details[2][2], 1)
                        put_newPDFdetail(pdf_detid, 19, "", 1, 1)
                        put_newPDFdetail(pdf_detid, 20, "", 1, 1)
                        put_newPDFdetail(pdf_detid, 21, "http://", 1, 1)
                        put_newPDFdetail(pdf_detid, 22, "", 1, 1)
                        # Insert values additionals
                        for value in pdf_attributes :
                            key_result, key_attributes = get_keys_attr(pdf_dettype, value)
                            if key_result:
                                for value in key_attributes :
                                    key_att_ids.append(value[0])

                        if len(key_att_ids) > 0:
                            for key in key_att_ids:
                                # addText_view("", key, page+1)  +==== addText_view(value, att_id, page)
                                put_newPDFdetail(pdf_detid, key, "", 1, 1)
            # Update pdf_type (and pdf_nation) in "pro_pdf_details"
            response_edit = edit_PDF(pro_id, pdf_detid, pdf_dettype, pdf_nation)
            if response_edit and responde_del:
                # msg_pdf = "PDF actualizado con éxito"
                pdf_id = pdf_detid
                result_split = 1

        if action == "double_pdf":
            current_date = date.today().strftime("%d-%m-%Y")
            pdf_detid   = request.values.get("pdf_detid")
            pdf_dettype = request.values.get("pdf_dettype")
            
            pdf_info = get_pdfInfoById(pdf_detid)
            pdf_detail = get_pdfDetailById(pro_id, pdf_detid)
            pdf = {
                    'name' :     pdf_info[0],
                    'npages' :   pdf_info[1],
                    'size' :     pdf_info[2],
                    'created' :  current_date
                }
            pdf_info_id = put_newPDF(pdf)
            result = put_newPPdetail(pro_id, pdf_info_id, pdf_detail[1], pdf_detail[2], pdf_detail[3], pdf_detail[4], pdf_id, pdf_detail[5], pdf_detail[6], 1, current_date)
            
            if result == True:
                if pdf_dettype == "A":
                    put_newPDFdetail(pdf_info_id, 1, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 2, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 3, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 4, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 5, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 6, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 7, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 8, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 9, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 10, "", int(pdf['npages'])-1, 1)
                    put_newPDFdetail(pdf_info_id, 11, "", int(pdf['npages'])-1, 1)
                    put_newPDFdetail(pdf_info_id, 12, "http://", int(pdf['npages']), 1)
                    put_newPDFdetail(pdf_info_id, 13, "_", 1, 1)
                if pdf_dettype == "M":
                    put_newPDFdetail(pdf_info_id, 14, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 15, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 16, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 17, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 18, "", 1, 1)
                    put_newPDFdetail(pdf_info_id, 19, "", 1, 1)
            result_split = 1
        
        if action == "nation_pdf":
            current_date = date.today().strftime("%d-%m-%Y")
            pdf_id = request.values.get("pdf_detid")
            pdf_nation = request.values.get("pdf_nation")

            response_nat = upd_nationPDF(pro_id, pdf_id, pdf_nation, current_date)
            if response_nat is True:
                # msg_att = "PDF actualizado con éxito"
                result_split = 1

        # if band_zoom == true:
        #     path_page = app.config['SPLIT_IMG_WEB'] + '/' + str(pdf_id) + 'page_'+ str(int(dict_page-1)) +'zoom.jpg', # dict_page
        #     return jsonify({'path_page': path_page})

        if current_user.is_authenticated and result_split == 1:
            project = get_projectById(pro_id)
            pdf = get_pdfDetailByIds(pro_id, pdf_id)
            pdfs = get_projectsById(pro_id, type_doc)
            """Verificar pdf_details, encontrados y no encontrados"""
            list_npages = list(range(1, int(pdf['npages']+1)))
            list_npages = [str(int) for int in list_npages]
            pdf['listnpages'] = list_npages

            # AQUI, agregar un campo en una tabla para distinguir si fue duplicado, get data for pdf_file
            if pdf['double']>0:
                view_id = pdf['double']
            else:
                view_id = pdf['id']

            pdf_path = {
                    'name':        pdf['name'],
                    'path_pdf':    app.config['UPLOAD_WEB'] + '/' + pdf['name'],
                    'path_page':   app.config['SPLIT_IMG_WEB'] + '/' + str(view_id) + 'page_0.jpg',
                    'num_pages':   int(pdf['npages']),
                    }
            pdf['pdf_path'] = pdf_path

            return render_template('project_pdfs.html', name=current_user.name.split()[0], pdfs=pdfs, pdf_type=type_doc, pdf=pdf, project=project[0], pro_id=pro_id)


@main.route("/export_paper_mul", methods=["POST"])
def export_paper_mul():
    if request.method == "POST":
        export_att = request.form.get('export_att')
    
    return send_file(export_att, as_attachment=True)


@app.route('/files/upload/<filename>')
def thesis_upload_img(filename):
    return send_from_directory(app.config['UPLOAD'], filename)


@main.route("/action_thesis_search", methods=["POST"])
def action_thesis_search():
    pdfs = None
    if request.method == "POST":
        keyword = request.values.get("keyword") 
        if len(keyword) > 1:
            pdfs = get_listThesisByWord(keyword)
        
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

    if request.method == "POST":
        pro_id = request.form.get('pro_id')
        # Code for multiple pdfs
        if 'files[]' not in request.files:
            return redirect(request.url)
        files = request.files.getlist('files[]')

        for file in files:
            file_pdfs.append(file.filename)
            if file and allowed_file(file.filename, app.config["UPLOAD_EXTENSIONS"]):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD'], filename))
                upload = True
        
        if (upload == True):
            print('File(s) successfully uploaded')
            return render_template('paper_mul.html', resultLoad=upload, pro_id=pro_id)


# CLOSE AND SAVE PAPER
@main.route("/<source>")
def close_paper_mul(source):
    url = "/" + source
    return redirect(url)

@main.route("/save_paper_mul", methods=["POST"])
def save_paper_mul():
    if request.method == "POST":
        down_image = request.form.get('down_image')
    
    return send_file(down_image, as_attachment=True)

# CLOSE AND SAVE THESIS
@main.route("/<source>")
def close_thesis_mul(source):
    url = "/" + source
    return redirect(url)

@main.route("/save_thesis_mul", methods=["POST"])
def save_thesis_mul():
    if request.method == "POST":
        down_image = request.form.get('down_image')
        
    return send_file(down_image, as_attachment=True)

# Download PDF
@main.route("/save_pdf_mul", methods=["POST"])
def save_pdf_mul():
    global text_scheme
    text_scheme = []
    pdfs = dict()

    if request.method == "POST":
        pro_id = request.form.get('down_proid')
        pdf_id  = request.form.get('down_pdfid')
        pdf_type = request.form.get('down_pdftype')
        
        text_schemes = get_pdfDetailByIds(pro_id, pdf_id)
        for detail in text_schemes['foundlist']:
            pdfs[detail['det_name']] = detail['det_value']
        
        if (pdfs['título']!='' and pdfs['autor']!='' and pdfs['año']!=''):
            now = datetime.datetime.now()
            if pdf_type == 'A':
                document, _ = build_pdfA(text_schemes)
            if pdf_type == 'M':
                document, _ = build_pdfMT(text_schemes)
            file_save = app.config['OUTPUT']+'/exportPDF_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
            document.save(file_save)
            result_pdf = app.config['FORWEB']+'/exportPDF_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'

            if result_pdf:
                return send_file(result_pdf, as_attachment=True)

# Download PROJECT
@main.route("/save_pro_mul", methods=["POST"])
def save_pro_mul():
    global text_schemes
    text_schemes = []
    result_pdf = ""

    if request.method == "POST":
        pro_id = request.form.get('down_pro')
        pro_type = request.form.get('down_pro_type')
        text_schemes = get_pdfDetailByProId(pro_id)
        if (len(text_schemes) > 0):
            now = datetime.datetime.now()
            document = build_project(text_schemes, pro_type)
            file_save = app.config['OUTPUT']+'/exportPROJECT_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
            document.save(file_save)
            result_pdf = app.config['FORWEB']+'/exportPROJECT_'+now.strftime("%d%m%Y_%H%M%S")+'.docx'
    return send_file(result_pdf, as_attachment=True)


# INIT PROJECT
if __name__ == '__main__':
    print("__main__")
    # start the flask app
    app.run(debug=True, use_reloader=True)
    # app.run(host="0.0.0.0", port="5000", debug=True, threaded=True, use_reloader=True)