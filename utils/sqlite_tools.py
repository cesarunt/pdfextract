# -*- coding: utf_8 -*-
from utils.config import cfg
import sqlite3
import secrets
import json
import os

global data_base
data_base = cfg.FILES.GLOBAL_PATH + '/db.sqlite'

def get_pdf_info(cursor, tablename, file_pdf):
    """Get column names of main table, given its name and a cursor (or connection) to the database.
    """
    query = f"""
                SELECT pdf_id, pdf_name, pdf_npages FROM {tablename}
                WHERE pdf_name = "{file_pdf}" 
            """
    cursor.execute(query)
    return cursor.fetchone()

def get_pdfById(cursor, tablename, pro_id, pdf_id):
    """Get column names of main table, given its name and a cursor (or connection) to the database.
    """
    query = f"""
                SELECT a.pdf_name, a.pdf_npages, b.pdf_pages
                FROM  {tablename} a INNER JOIN pro_pdf_details b ON a.pdf_id = b.pdf_id
                WHERE a.pdf_id = "{pdf_id}" and b.pro_id = "{pro_id}"
            """
    cursor.execute(query)
    return cursor.fetchone()

def get_pdfsByProId(cursor, tablename, pro_id):
    """Get pdf_id list from tablename -> pro_pdf_details
    """
    ids = ()
    query = f"""
                SELECT pdf_id
                FROM  {tablename}
                WHERE pro_id = "{pro_id}"
            """
    cursor.execute(query)
    records = cursor.fetchall()

    pdf_ids = list(ids)
    for record in records:
        pdf_ids.append(record[0])
        
    return records, tuple(pdf_ids)

def get_col_names(cursor, tablename):
    """Get column names of a table, given its name and a cursor
       (or connection) to the database.
    """
    reader=cursor.execute("SELECT * FROM {}".format(tablename))
    return [x[0] for x in reader.description] 

def get_listThesisByWord(keyword):
    table_name = 'pdf_keywords'
    pdfs = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT a.pdf_id, a.pdf_name, a.pdf_npages, a.pdf_size, b.det_value, d.key_name
                    FROM  ((pdf_info a INNER JOIN pdf_details b ON a.pdf_id = b.det_info) INNER JOIN pdf_key_details c ON a.pdf_id = c.pdf_id) INNER JOIN key_info d ON c.key_id = d.key_id
                    WHERE d.key_name LIKE "%{keyword}%" AND b.det_attribute = 2
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            if record[4] == "":
                pdf_title = "Titulo No registrado"
            else:
                pdf_title = record[4]
            pdfs.append({
                    'pdf_id':       record[0],
                    'pdf_name':     record[1],
                    'pdf_npages':   record[2], 
                    'pdf_size':     record[3],
                    'det_value':    pdf_title,
                    'key_name':     record[5]
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return pdfs

# SAVE DATA WHEN DRAW RECTANGLE (TEXT, X, Y, W, H)
def upd_detailCanvasByIds(det_id, det_info, det_attribute, text='', npage=1, rect=dict()):
    table_name = 'pdf_details'
    # table_colnames = None
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE pdf_details SET det_value='{text}', det_npage={npage}, det_x={rect['x']}, det_y={rect['y']}, det_width={rect['w']}, det_height={rect['h']}
                    WHERE det_id = {det_id} AND det_info = {det_info} AND det_attribute = {det_attribute}
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to update data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result

# SAVE DATA WHEN DRAW RECTANGLE (TEXT)
def upd_detailTextByIds(det_id, det_info, det_attribute, text='', npage=1):
    table_name = 'pdf_details'
    # table_colnames = None
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE pdf_details SET det_value='{text}', det_npage={npage}
                    WHERE det_id = {det_id} AND det_info = {det_info} AND det_attribute = {det_attribute}
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to update data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result

# ----------------------------------- FORM UPLOAD -----------------------------------
def put_newProject(project=dict()):
    table_name = 'project_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print(json.dumps(project))
        # print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (pro_title, pro_uni, pro_department, pro_province, pro_district, pro_career, pro_comment, pro_type_a, pro_type_m, pro_n_articles, pro_n_process, pro_user, pro_created) 
                    VALUES ("{project['title']} ", "{project['university']}", "{project['department']}", "{project['province']}", "{project['district']}", "{project['career']}", "{project['comment']}", "{project['type_a']}", "{project['type_m']}", "{project['n_articles']}", "{project['n_process']}", "{project['user']}", "{project['created']}")
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        id = cursor.lastrowid
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result, id

def put_newPKdetail(id, key, current_date):
    table_name = 'pro_key_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    INSERT INTO "{table_name}" (pro_id, key_id, pro_key_created)
                    SELECT "{id}", "{key}", "{current_date}"
                    WHERE NOT EXISTS(SELECT 1 FROM "{table_name}" WHERE pro_id = "{id}" AND key_id = "{key}");
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result

def get_lastVariable():
    table_name = 'key_info'
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    SELECT * FROM {table_name} ORDER BY key_id DESC LIMIT 1           
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        record = cursor.fetchone()
        result = record[0]
    except sqlite3.Error as error:
        print("Failed to get data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result

def put_newKeyword(key_name, current_date):
    table_name = 'key_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (key_name, key_active, key_created)
                    VALUES ("{key_name}", "1", "{current_date}")                
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        id = cursor.lastrowid
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return result, id

def get_listUniversities():
    table_name = 'uni_info'
    universities = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT uni_id, uni_name, uni_nickname
                    FROM "{table_name}"
                    WHERE  uni_active = 1
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            universities.append({
                    'uni_id':       record[0],
                    'uni_name':     record[1],
                    'uni_nickname': record[2],
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return universities

def get_listDepartments():
    table_name = 'ubigeo_departments'
    departments = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT id, name
                    FROM {table_name}
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print(records)

        for record in records:
            departments.append({
                    'dpt_id':       record[0],
                    'dpt_name':     record[1],
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return departments

def get_listProvinces(department):
    table_name = 'ubigeo_provinces'
    provinces = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT id, name, department_id
                    FROM {table_name}
                    WHERE  department_id = {department}
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print(records)

        for record in records:
            provinces.append({
                    'prv_id':        record[0],
                    'prv_name':      record[1],
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return provinces

def get_listDistricts(province, department):
    table_name = 'ubigeo_districts'
    districts = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT id, name, province_id, department_id
                    FROM {table_name}
                    WHERE province_id = {province} and department_id = {department}
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            districts.append({
                    'dis_id':        record[0],
                    'dis_name':      record[1],
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return districts

def get_listKeywords():
    # List of TOP 10
    table_name = 'key_info'
    keywords = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT key_id, key_name
                    FROM "{table_name}"
                    WHERE  key_active = 1
                """
        # print("listKeywords", query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            keywords.append(str(record[0])+"-"+record[1])
        # print("keywords", keywords)
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return keywords

def get_listProjects(limit=-1):
    # List of TOP 10
    # print("data_base... ", data_base)
    table_name = 'project_info'
    projects = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT a.pro_id, a.pro_title, b.uni_nickname, a.pro_career, a.pro_user
                    FROM "{table_name}" a INNER JOIN uni_info b ON a.pro_uni = b.uni_id
                    ORDER BY a.pro_id DESC
                    LIMIT "{limit}"
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            projects.append({
                    'pro_id':     record[0],
                    'pro_title':  record[1],
                    'pro_uni':    record[2],
                    'pro_career': record[3],
                    'pro_user':   record[4],
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to connect... ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return projects

def get_projectById(id):
    # List of TOP 10
    table_name = 'project_info'
    project = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT a.pro_id, a.pro_title, a.pro_uni, b.uni_name, a.pro_department, a.pro_province, a.pro_district, a.pro_career, a.pro_comment, a.pro_type_a, a.pro_type_m, a.pro_n_articles, a.pro_n_process, a.pro_user, a.pro_created
                    FROM "{table_name}" a INNER JOIN uni_info b ON a.pro_uni = b.uni_id
                    WHERE  a.pro_id = "{id}"
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        record = cursor.fetchone()
        project.append({
                'pro_id':         record[0],
                'pro_title':      record[1],
                'pro_uniid':      record[2],
                'pro_uni':        record[3],
                'pro_department': record[4],
                'pro_province':   record[5],
                'pro_district':   record[6],
                'pro_career':     record[7],
                'pro_comment':    record[8],
                'pro_type_a':     record[9],
                'pro_type_m':     record[10],
                'pro_n_articles': record[11],
                'pro_n_process':  record[12],
                'pro_user':       record[13],
                'pro_created':    record[14],
            })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return project

def get_listKeywordsById(id):
    # List of TOP 10
    table_name = 'pro_key_details'
    pk_details = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT c.key_name, c.key_id
                    FROM   (project_info a INNER JOIN "{table_name}" b ON a.pro_id = b.pro_id) INNER JOIN key_info c ON b.key_id = c.key_id
                    WHERE  b.pro_id = "{id}"
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            pk_details.append({
                'key_name': record[0],
                'key_id':   record[1],
            })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return pk_details

def upd_projectById(id, project):
    table_name = 'project_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE "{table_name}" SET pro_title='{project['title']}', pro_uni={project['university']}, pro_department={project['department']}, pro_province={project['province']}, pro_district={project['district']}, pro_career="{project['career']}", pro_comment="{project['comment']}", pro_type_a={project['type_a']}, pro_type_m={project['type_m']}
                    WHERE pro_id = {id}
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to update data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return result

def upd_projectProcess(id, n_articles, n_process):
    table_name = 'project_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE "{table_name}" SET pro_n_articles='{n_articles}', pro_n_process={n_process}
                    WHERE pro_id = {id}
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to update data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
        return result

def get_squareProjects_ByWord(keyword):
    table_name = 'project_info'
    projects = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT DISTINCT a.pro_id, a.pro_title, a.pro_career, a.pro_n_articles, a.pro_n_process, u.name, a.pro_created
                    FROM  (("{table_name}" a LEFT JOIN pro_key_details b ON a.pro_id = b.pro_id) LEFT JOIN key_info c ON b.key_id = c.key_id) INNER JOIN user u ON a.pro_user = u.id
                    WHERE a.pro_title LIKE "%{keyword}%" OR c.key_name LIKE "%{keyword}%"
                    ORDER BY a.pro_id DESC
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print(json.dumps(records))

        colors = ['success', 'danger', 'warning', 'info', 'dark']
        # years = []
        for record in records:
            # if record[5].split('/')[-1] in years:
            projects.append({
                    'pro_id':         record[0],
                    'pro_title':      record[1],
                    'pro_career':     record[2],
                    'pro_n_articles': record[3], 
                    'pro_n_process':  record[4],
                    'pro_user_name':  record[5].split(' ')[0],
                    'pro_created':    record[6],
                    'pro_color':      secrets.choice(colors)
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return projects

def get_userById(id):
    # List of TOP 10
    table_name = 'user'
    user = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT email, name
                    FROM "{table_name}"
                    WHERE  id = "{id}"
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        record = cursor.fetchone()
        user.append({
                'user_email':  record[0],
                'user_name':   record[1],
            })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return user

def put_newPDFattribute(name, current_date):
    table_name = 'pdf_attributes'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (att_name, att_fecha) 
                    VALUES ("{name} ", "{current_date}")
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        id = cursor.lastrowid
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result, id

def put_newPDFdetail(det_info, det_attribute, det_value, det_npage, det_visible):
    table_name = 'pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (det_info, det_attribute, det_value, det_npage, det_visible)
                    VALUES ("{det_info} ", "{det_attribute}", "{det_value}", "{det_npage}", "{det_visible}")
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result

def del_itemPDFdetail(det_id):
    # data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE "{table_name}" SET det_visible=0
                    WHERE det_id = {det_id}
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return result

# ----------------------------------- SAVE AFTER PROCESS -----------------------------------
def put_newPDF(pdf=dict()):
    table_name = 'pdf_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (pdf_name, pdf_npages, pdf_size, pdf_created) 
                    VALUES ("{pdf['name']} ", "{pdf['npages']}", "{pdf['size']}", "{pdf['created']}")
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        id = cursor.lastrowid
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        
        return id

def put_newPPdetail(id, pdf, name, pages, current_date):
    table_name = 'pro_pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (pro_id, pdf_id, pdf_name, pdf_pages, pro_pdf_created)
                    VALUES ("{id} ", "{pdf}", "{name}", "{pages}", "{current_date}")
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
        return result

def upd_PPdetail(id, pro_id, pdf_id, name, current_date):
    table_name = 'pro_pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE "{table_name}" SET pdf_name='{name}', pro_pdf_created="{current_date}"
                    WHERE pro_id = {pro_id} AND pdf_id = {pdf_id}
                """
        
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
        return result

def get_projectPDFById(id):
    # List of TOP 10
    table_name = 'pro_pdf_details'
    pp_details = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT b.pro_id, b.pdf_id, b.pdf_name, a.pdf_name, a.pdf_npages, a.pdf_size
                    FROM   pdf_info a INNER JOIN "{table_name}" b ON a.pdf_id = b.pdf_id
                    WHERE  b.pro_id = "{id}"
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        i = 0
        for record in records:
            words = record[2].split()
            for word in words:
                if len(word)>20:
                    index = words.index(word)
                    words.remove(word)
                    words.insert(index, "-")
            text = ' '.join(words)
            i = i + 1
            pp_details.append({
                'pro_id':      record[0],
                'pdf_id':      record[1],
                'pdf_fullname': text,
                'pdf_name':    text[0:199],
                'pdf_file':    record[3],
                'pdf_npages':  record[4],
                'pdf_size':    record[5],
                'pdf_i':       i
            })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return pp_details

def get_pdfDetailByProId(pro_id):
    table_name = 'pdf_details'
    pdf_details = []
    pdfs = dict()
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        pdf_records, pdf_ids = get_pdfsByProId(cursor, 'pro_pdf_details', pro_id)
        # print("Connected to SQLite")
        query = f"""
                    SELECT b.det_id, b.det_info, b.det_attribute, c.att_name, b.det_value, b.det_npage
                    FROM   "{table_name}" b INNER JOIN pdf_attributes c ON b.det_attribute = c.att_id
                    WHERE  b.det_info IN {pdf_ids} and b.det_visible = 1
                    ORDER BY b.det_id ASC
                """ 
        # print('pdf_details', query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print("RECORDS")
        # for record in records:
        #     print(record)
        # input("..... records .....")
        i = 0
        for record in records:
            if pdf_records[i][0] == record[1]:
                pdf_details.append({
                        'det_id':       record[0],
                        'det_info':     record[1],
                        'det_attribute':record[2],
                        'det_name':     record[3], 
                        'det_value':    record[4],
                        'det_npage':    record[5]
                        })
            else:
                pdfs[i] = {
                    'id':    pdf_records[i][0],
                    'details':  pdf_details,
                }
                pdf_details = []
                pdf_details.append({
                    'det_id':       record[0],
                    'det_info':     record[1],
                    'det_attribute':record[2],
                    'det_name':     record[3], 
                    'det_value':    record[4],
                    'det_npage':    record[5]
                })
                i = i + 1

        pdfs[i] = {
            'id':    pdf_records[i][0],
            'details':  pdf_details,
        }
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
        return pdfs

def get_pdfDetailByIds(pro_id, pdf_id):
    table_name = 'pdf_details'
    pdf = dict()
    pdf_foundlist = []      #   Atributos
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        pdf_info = get_pdfById(cursor, 'pdf_info', pro_id, pdf_id)
        # print("pdf_info")
        # print(pdf_info)
        pdf_name, pdf_npages, pdf_pages = pdf_info
        query = f"""
                    SELECT b.det_id, b.det_attribute, c.att_name, b.det_value, b.det_npage, b.det_visible, b.det_x, b.det_y, b.det_width, b.det_height
                    FROM   (pdf_info a INNER JOIN "{table_name}" b ON a.pdf_id = b.det_info) INNER JOIN pdf_attributes c ON b.det_attribute = c.att_id
                    WHERE  a.pdf_id = "{pdf_id}"
                    ORDER BY b.det_id ASC
                """ 
        # print('pdfDetail', query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        
        i = 0
        for record in records:
            i = i + 1
            pdf_foundlist.append({
                    'det_id':       record[0],
                    'det_attribute':record[1],
                    'det_name':     record[2], 
                    'det_value':    record[3],
                    'det_npage':    record[4],
                    'det_visible':  record[5],
                    'det_x':        record[6],
                    'det_y':        record[7],
                    'det_width':    record[8],
                    'det_height':   record[9],
                    'det_i':        i
                    })
        pdf = {
            'id':        pdf_id,
            'name':      pdf_name,
            'npages':    pdf_npages,
            'pages':     pdf_pages,
            'foundlist': pdf_foundlist,
        }
        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
        return pdf