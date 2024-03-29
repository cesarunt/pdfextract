# -*- coding: utf_8 -*-
from utils.config import cfg
import unidecode
import datetime
import sqlite3

global data_base
data_base = cfg.FILES.GLOBAL_PATH + '/db.sqlite'

def get_pdf_info(cursor, tablename, file_pdf):
    """Get column names of main table, given its name and a cursor (or connection) to the database."""
    query = f"""
                SELECT pdf_id, pdf_name, pdf_npages FROM {tablename}
                WHERE pdf_name = "{file_pdf}" 
            """
    cursor.execute(query)
    return cursor.fetchone()

# pdf_attributes
def get_keys_attr(type_val, attribute):
    result = False
    val_def = str(attribute['key_id']) + "_definición"
    val_imp = str(attribute['key_id']) + "_importancia"
    val_mod = str(attribute['key_id']) + "_modelos"
    val_con = str(attribute['key_id']) + "_conceptos"
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                SELECT att_id
                FROM  pdf_attributes
                WHERE att_type = "{type_val}" and (att_name = "{val_def}" or att_name = "{val_imp}" or att_name = "{val_mod}" or att_name = "{val_con}")
            """
        cursor.execute(query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to get data from ", error)
    finally:
        return result, cursor.fetchall()

def get_proKeyById(cursor, tablename, pro_id):
    """Get column names of main table, given its name and a cursor (or connection) to the database."""
    query = f"""
                SELECT b.key_id, c.key_name
                FROM  ({tablename} a INNER JOIN pro_key_details b ON a.pro_id = b.pro_id) INNER JOIN key_info c ON b.key_id = c.key_id
                WHERE a.pro_id = "{pro_id}"
            """
    cursor.execute(query)
    records = cursor.fetchall()
    pro_keyInfo = []

    for record in records:
        pro_keyInfo.append({
                    'key_id':       record[0],
                    'key_name':     record[1]
                    })

    return pro_keyInfo

def get_pdfDetById(cursor, tablename, pro_id, pdf_id):
    """Get column names of main table, given its name and a cursor (or connection) to the database."""
    query = f"""
                SELECT a.pdf_name, a.pdf_npages, b.pdf_type, b.pdf_nation, b.pdf_double, b.pdf_pages
                FROM  {tablename} a INNER JOIN pro_pdf_details b ON a.pdf_id = b.pdf_id
                WHERE a.pdf_id = "{pdf_id}" and b.pro_id = "{pro_id}"
            """
    cursor.execute(query)
    return cursor.fetchone()

# AQUI
def get_pdfInfoById(pdf_id):
    """Get column names of main table, given its name and a cursor (or connection) to the database."""
    sqliteConnection = sqlite3.connect(data_base)
    cursor = sqliteConnection.cursor()
    query = f"""
                SELECT pdf_name, pdf_npages, pdf_size
                FROM  pdf_info
                WHERE pdf_id = "{pdf_id}"
            """
    cursor.execute(query)
    return cursor.fetchone()

def get_pdfDetailById(pro_id, pdf_id):
    """Get column names of main table, given its name and a cursor (or connection) to the database."""
    sqliteConnection = sqlite3.connect(data_base)
    cursor = sqliteConnection.cursor()
    query = f"""
                SELECT pdf_id, pdf_name, pdf_name_search, pdf_type, pdf_nation, pdf_double, pdf_pages, pdf_attributes, pdf_visible
                FROM  pro_pdf_details
                WHERE pdf_id = "{pdf_id}" and pro_id = "{pro_id}"
            """
    cursor.execute(query)
    return cursor.fetchone()

def get_pdfsByProId(cursor, tablename, pro_id):
    """Get pdf_id list from tablename -> pro_pdf_details"""
    query = f"""
                SELECT pdf_id, pdf_type
                FROM  {tablename}
                WHERE pro_id = "{pro_id}" and pdf_visible = 1
            """
    cursor.execute(query)
    records = cursor.fetchall()
    pdf_ids = tuple()
    for record in records:
        pdf_ids = pdf_ids + (record[0],)
    return records, pdf_ids

def get_col_names(cursor, tablename):
    """Get column names of a table, given its name and a cursor
       (or connection) to the database.
    """
    reader=cursor.execute("SELECT * FROM {}".format(tablename))
    return [x[0] for x in reader.description] 

def get_listThesisByWord(keyword):
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
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        text = text.replace("'","").replace("\n"," ").replace(" -","-")
        # print("Connected to SQLite")
        query = f"""
                    UPDATE pdf_details SET det_value='{text}', det_npage={npage}, det_x={rect['x']}, det_y={rect['y']}, det_width={rect['w']}, det_height={rect['h']}
                    WHERE det_id = {det_id} AND det_info = {det_info} AND det_attribute = {det_attribute}
                """
        print("QQQ", query)
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
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        text = text.replace("'","").replace("\n"," ").replace(" -","-")
        # print("Connected to SQLite")
        query = f"""
                    UPDATE pdf_details SET det_value='{text}', det_npage={npage}
                    WHERE det_id = {det_id} AND det_info = {det_info} AND det_attribute = {det_attribute}
                """
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

def upd_detailPDFnameByIds(pro_id, pdf_id, text='', text_search=""):
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        text = text.replace("'","").replace("\n"," ").replace(" -","-")
        # print("Connected to SQLite")
        query = f"""
                    UPDATE pro_pdf_details SET pdf_name='{text}', pdf_name_search='{text_search}'
                    WHERE pro_id = {pro_id} AND pdf_id = {pdf_id}
                """
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
        # print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (pro_title, pro_title_search, pro_uni, pro_department, pro_province, pro_district, pro_career, pro_comment, pro_type_a, pro_type_m, pro_n_articles, pro_n_process, pro_user, pro_created, pro_updated) 
                    VALUES ("{project['title']} ", "{project['title_search']} ", "{project['university']}", "{project['department']}", "{project['province']}", "{project['district']}", "{project['career']}", "{project['comment']}", "{project['type_a']}", "{project['type_m']}", "{project['n_articles']}", "{project['n_process']}", "{project['user']}", "{project['created']}", "{project['updated']}")
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        id = cursor.lastrowid
        sqliteConnection.commit()
        result = True
        # print("SAVE put_newProject")
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
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            keywords.append(str(record[0])+"-"+record[1])
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            # print("The SQLite connection is closed")
        return keywords

def get_listProjects(limit=-1, user_id=1):
    # List of TOP 10
    table_name = 'project_info'
    projects = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT a.pro_id, a.pro_title, b.uni_nickname, a.pro_career, a.pro_user, a.pro_updated
                    FROM "{table_name}" a INNER JOIN uni_info b ON a.pro_uni = b.uni_id
                    WHERE a.pro_user = "{user_id}"
                    ORDER BY a.pro_updated DESC
                    LIMIT "{limit}"
                """
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
    table_name = 'project_info'
    project = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    SELECT a.pro_id, a.pro_title, a.pro_uni, b.uni_name, a.pro_department, a.pro_province, a.pro_district, a.pro_career, a.pro_comment, a.pro_type_a, a.pro_type_m, a.pro_n_articles, a.pro_n_process, a.pro_user, a.pro_created, a.pro_updated
                    FROM "{table_name}" a INNER JOIN uni_info b ON a.pro_uni = b.uni_id
                    WHERE  a.pro_id = "{id}"
                """
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
                    UPDATE "{table_name}" SET pro_title='{project['title']}', pro_title_search='{project['title_search']}', pro_uni={project['university']}, pro_department={project['department']}, pro_province={project['province']}, pro_district={project['district']}, pro_career="{project['career']}", pro_comment="{project['comment']}", pro_type_a={project['type_a']}, pro_type_m={project['type_m']}, pro_updated='{project['updated']}'
                    WHERE pro_id = {id}
                """
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

def get_squareProjects_ByWord(bydoc, keyword_list, typedoc, typeAnac, typeAint, bydate, startDate, endDate):
    table_name = 'project_info'
    projects = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        keyword_search = unidecode.unidecode(keyword_list[0])
        if bydoc == '1':
            query = f"""
                        SELECT DISTINCT a.pro_id, b.pdf_id, b.pdf_name, b.pdf_type, b.pdf_nation, u.name, a.pro_created, s.uni_name, p.name, d.det_value
                        FROM  ((((({table_name} a INNER JOIN pro_pdf_details b ON a.pro_id = b.pro_id) 
						LEFT JOIN pdf_info c ON b.pdf_id = c.pdf_id) 
						LEFT JOIN pdf_details d ON c.pdf_id = d.det_info)
						LEFT JOIN user u ON a.pro_user = u.id) 
						LEFT JOIN uni_info s ON a.pro_uni = s.uni_id) 
						LEFT JOIN ubigeo_departments p ON a.pro_department = p.id
						WHERE b.pdf_visible = 1 AND b.pdf_name_search LIKE "%{keyword_search}%"
                    """
            if len(keyword_list) > 1:
                for i in range(1, len(keyword_list)): 
                    query += f""" OR b.pdf_name_search LIKE "%{keyword_list[i]}%" """

        if bydoc == '2':
            query = f"""
                        SELECT DISTINCT a.pro_id, b.pdf_id, b.pdf_name, b.pdf_type, b.pdf_nation, u.name, a.pro_created, s.uni_name, p.name, d.det_value
                        FROM  ((((({table_name} a INNER JOIN pro_pdf_details b ON a.pro_id = b.pro_id) 
						LEFT JOIN pdf_info c ON b.pdf_id = c.pdf_id) 
						LEFT JOIN pdf_details d ON c.pdf_id = d.det_info)
						LEFT JOIN user u ON a.pro_user = u.id) 
						LEFT JOIN uni_info s ON a.pro_uni = s.uni_id) 
						LEFT JOIN ubigeo_departments p ON a.pro_department = p.id
						WHERE b.pdf_visible = 1 AND a.pro_title_search LIKE "%{keyword_search}%"
                    """
            if len(keyword_list) > 1:
                for i in range(1, len(keyword_list)): 
                    query += f""" OR a.pro_title_search LIKE "%{keyword_list[i]}%" """

        if bydate == '1':
            query += f""" 
                    AND (d.det_attribute = 3 OR d.det_attribute = 18)
                    """
            if startDate:
                startYear = str(startDate).split("/")[2]
                query += f""" 
                    AND d.det_value >= "{startYear}"
                    """
            if endDate:
                endYear = str(endDate).split("/")[2]
                query += f""" 
                    AND d.det_value <= "{endYear}"
                    """

        if bydate == '2':
            query += f""" 
                    AND (d.det_attribute = 3 OR d.det_attribute = 18)
                    """
            if startDate and endDate:
                date_init = startDate[3:5] + "-" + startDate[:2] + "-" + startDate[6:]
                date_end = endDate[3:5] + "-" + endDate[:2] + "-" + endDate[6:]
                query += f""" 
                    AND b.pro_pdf_created BETWEEN "{date_init}" AND "{date_end}"
                    """
        
        if typedoc == 'A':
            query += f""" AND b.pdf_type = 'A' """
            if typeAnac == None and typeAint == None:
                query += f""" AND (b.pdf_nation = '' OR b.pdf_nation = '') """
            elif typeAnac == '1' and typeAint == '1':
                query += f""" AND (b.pdf_nation = 'N' OR b.pdf_nation = 'I') """
            else:
                if typeAnac == '1':
                    query += f""" AND b.pdf_nation = 'N' """
                if typeAint == '1':
                    query += f""" AND b.pdf_nation = 'I' """
        
        if typedoc == 'M':
            query += f""" AND b.pdf_type = 'M' """
        
        query += f"""
                    ORDER BY a.pro_id DESC
                """
        # print("QQQ", query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        project = []
        pdfs = []
        nation = ""
        i = 1
        colors = ['info', 'danger', 'warning', 'info', 'secondary']
        # secrets.choice(colors)
        aux_pro_id = 0
        for record in records:
            if record[4] == "N" :
                nation = "Nacional"
            if record[4] == "I" :
                nation = "Internacional"
            if record[4] == "ON" :
                nation = "None"
            if (aux_pro_id == record[0]):
                i = i + 1
                pdfs.append({
                    'pro_id':        record[0],
                    'pdf_id':        record[1],
                    'pdf_name':      record[2][0:250],
                    'pdf_type':      record[3],
                    'pdf_nation':    record[4],
                    'pdf_nationtext':nation,
                    'pdf_user':      record[5],
                    'pdf_created':   record[6],
                    'pdf_year':      record[9],
                    'pdf_i':         i
                })
            else:
                aux_pro_id = record[0]
                project = get_projectPDFById(record[0])
                i = 1
                pdfs = []
                pdfs.append({
                    'pro_id':        record[0],
                    'pdf_id':        record[1],
                    'pdf_name':      record[2][0:250],
                    'pdf_type':      record[3],
                    'pdf_nation':    record[4],
                    'pdf_nationtext':nation,
                    'pdf_user':      record[5],
                    'pdf_created':   record[6],
                    'pdf_year':      record[9],
                    'pdf_i':         i
                })
                projects.append({
                        'pro_id':       project[0]['pro_id'],
                        'pro_title':    project[0]['pro_title'],
                        'pro_career':   project[0]['pro_career'],
                        'pro_articles': project[0]['pro_articles'], 
                        'pro_process':  project[0]['pro_process'],
                        'pro_user':     project[0]['pro_user'],
                        'pro_created':  project[0]['pro_created'],
                        'pro_exist':    project[0]['pro_id'],
                        'pro_color':    colors[3],
                        'pro_uni':      record[7],
                        'pro_city':     str(record[8]).upper(),  # DEPARTMENT
                        'pro_year':     record[9],
                        'pdfs':         pdfs
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
    table_name = 'user'
    user = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    SELECT id, name, gender, birthday, email, password, phone, address, photo, active, created, updated
                    FROM "{table_name}"
                    WHERE  id = "{id}"
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        record = cursor.fetchone()
        user.append({
                'usr_id':       record[0],
                'usr_name':     record[1],
                'usr_gender':   record[2],
                'usr_birthday': record[3],
                'usr_email':    record[4],
                'usr_password': record[5],
                'usr_phone':    record[6],
                'usr_address':  record[7],
                'usr_photo':    record[8],
                'usr_active':   record[9],
                'usr_created':  record[10],
                'usr_updated':  record[11],
            })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
    
    return user

def put_newPDFattribute(name, type, current_date):
    table_name = 'pdf_attributes'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    INSERT INTO "{table_name}" (att_name, att_type, att_fecha) 
                    VALUES ("{name}", "{type}", "{current_date}")
                """
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
        
        return result, id

def put_newPDFdetail(det_info, det_attribute, det_value, det_npage, det_visible):
    table_name = 'pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    INSERT INTO "{table_name}" (det_info, det_attribute, det_value, det_npage, det_visible)
                    VALUES ("{det_info}", "{det_attribute}", "{det_value}", "{det_npage}", "{det_visible}")
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
        
        return result

def del_attributeById(det_id):
    table_name = 'pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    UPDATE "{table_name}" SET det_visible = 0
                    WHERE det_id = {det_id}
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        
        return result

def del_attributeByProId(pro_id, list_attributes):
    table_name = 'pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    DELETE FROM "{table_name}"
                    WHERE det_info = {pro_id} and det_attribute > 0
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        
        return result

def del_PDF(pro_id, pdf_id):
    table_name = 'pro_pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    UPDATE "{table_name}" SET pdf_visible=0
                    WHERE pro_id = {pro_id} and pdf_id = {pdf_id}
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        
        return result

def get_pdfDetailForDelete(pdf_detid, list_attributes):
    table_name = 'pdf_details'
    records = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    SELECT b.det_attribute, b.det_value, b.det_npage
                    FROM   "{table_name}" b
                    WHERE  b.det_info = {pdf_detid} and b.det_attribute IN {list_attributes} and b.det_visible = 1
                    ORDER BY b.det_id ASC
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()        
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return records

def edit_PDF(pro_id, pdf_id, pdf_dettype, pdf_nation):
    table_name = 'pro_pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    UPDATE "{table_name}" SET pdf_type='{pdf_dettype}', pdf_nation="{pdf_nation}"
                    WHERE pro_id = {pro_id} and pdf_id = {pdf_id}
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to delete data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        
        return result

# ----------------------------------- SAVE AFTER PROCESS -----------------------------------
def put_newPDF(pdf=dict()):
    table_name = 'pdf_info'
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    INSERT INTO "{table_name}" (pdf_name, pdf_npages, pdf_size, pdf_created) 
                    VALUES ("{pdf['name']}", "{pdf['npages']}", "{pdf['size']}", "{pdf['created']}")
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        id = cursor.lastrowid
        sqliteConnection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return id

def put_newPPdetail(id, pdf, name, name_search, type_doc, nation_doc, double, pages, attributes, visible, current_date):
    table_name = 'pro_pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    INSERT INTO "{table_name}" (pro_id, pdf_id, pdf_name, pdf_name_search, pdf_type, pdf_nation, pdf_double, pdf_pages, pdf_attributes, pdf_visible, pro_pdf_created)
                    VALUES ("{id} ", "{pdf}", "{name}", "{name_search}", "{type_doc}", "{nation_doc}", "{double}", "{pages}", "{attributes}", "{visible}", "{current_date}")
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
            print("The SQLite connection is WRONG")
        return result

def upd_PPdetail(pro_id, pdf_id, text, text_search, current_date):
    table_name = 'pro_pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    UPDATE "{table_name}" SET pdf_name='{text}', pdf_name_search='{text_search}', pro_pdf_created="{current_date}"
                    WHERE pro_id = {pro_id} AND pdf_id = {pdf_id} and pdf_visible = 1
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

def upd_nationPDF(pro_id, pdf_id, pdf_nation, current_date):
    table_name = 'pro_pdf_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE "{table_name}" SET pdf_nation="{pdf_nation}", pro_pdf_created="{current_date}"
                    WHERE pro_id = {pro_id} AND pdf_id = {pdf_id} and pdf_visible = 1
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

def get_projectPDFById(pro_id):
    table_name = 'project_info'
    pp_details = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    SELECT a.pro_id, a.pro_title, a.pro_career, a.pro_n_articles, a.pro_n_process, u.name, a.pro_created
                    FROM   "{table_name}" a INNER JOIN user u ON a.pro_user = u.id
                    WHERE  a.pro_id = "{pro_id}"
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        record = cursor.fetchone()
        # for record in records:
        pp_details.append({
            'pro_id':      record[0],
            'pro_title':   record[1],
            'pro_career':  record[2],
            'pro_articles':record[3],
            'pro_process': record[4],
            'pro_user':    str(record[5]).split(' ')[0],
            'pro_created': record[6]            
        })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return pp_details

def get_projectsById(id, type_doc):
    table_name = 'pro_pdf_details'
    pp_details = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        if type_doc == "T":
            query = f"""
                        SELECT b.pro_id, b.pdf_id, b.pdf_name, b.pdf_type, b.pdf_nation, a.pdf_name, a.pdf_npages, a.pdf_size
                        FROM   pdf_info a INNER JOIN "{table_name}" b ON a.pdf_id = b.pdf_id
                        WHERE  b.pro_id = "{id}" AND b.pdf_visible = 1
                    """
        else:
            query = f"""
                        SELECT b.pro_id, b.pdf_id, b.pdf_name, b.pdf_type, b.pdf_nation, a.pdf_name, a.pdf_npages, a.pdf_size
                        FROM   pdf_info a INNER JOIN "{table_name}" b ON a.pdf_id = b.pdf_id
                        WHERE  b.pro_id = "{id}" AND b.pdf_visible = 1 AND b.pdf_type = "{type_doc}"
                    """
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
                'pdf_name':    text[0:149],
                'pdf_type':    record[3],
                'pdf_nation':  record[4],
                'pdf_file':    record[5],
                'pdf_npages':  record[6],
                'pdf_size':    record[7],
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

# Download PDF -> get data by PdfID
def get_pdfDetailByIds(pro_id, pdf_id, atts = []):
    table_name = 'pdf_details'
    pdf = dict()
    pdf_foundlist = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        pdf_info = get_pdfDetById(cursor, 'pdf_info', pro_id, pdf_id)
        pdf_name, pdf_npages, pdf_type, pdf_nation, pdf_double, pdf_pages = pdf_info
        pro_keylist = get_proKeyById(cursor, 'project_info', pro_id)
        query = f"""
                    SELECT b.det_id, b.det_attribute, c.att_name, c.att_type, b.det_value, b.det_npage, b.det_visible, b.det_x, b.det_y, b.det_width, b.det_height
                    FROM   (pdf_info a INNER JOIN "{table_name}" b ON a.pdf_id = b.det_info) LEFT JOIN pdf_attributes c ON b.det_attribute = c.att_id
                    WHERE  a.pdf_id = "{pdf_id}"
                """
        if len(atts) > 0:
            if len(atts) == 1:
                result = str(tuple(atts)).replace(',', '')
            else:
                result = tuple(atts)
            query += f""" AND ( b.det_attribute < 23 OR b.det_attribute IN {result} ) """

        query += f"""
                    ORDER BY b.det_attribute ASC
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        
        i = 0
        for record in records:
            i = i + 1
            keyname = record[2]
            for key in pro_keylist:
                if str(record[2]).split('_')[0] == str(key['key_id']) :
                    keyname = key['key_name'] + " " + str(record[2]).split('_')[1]
                    break
            pdf_foundlist.append({
                    'det_id':       record[0],
                    'det_attribute':record[1],
                    'det_name':     keyname,
                    'det_type':     record[3],
                    'det_value':    record[4],
                    'det_npage':    record[5],
                    'det_visible':  record[6],
                    'det_x':        record[7],
                    'det_y':        record[8],
                    'det_width':    record[9],
                    'det_height':   record[10],
                    'det_i':        i
                    })
        pdf = {
            'id':        pdf_id,
            'name':      pdf_name,
            'npages':    pdf_npages,
            'type':      pdf_type,
            'nation':    pdf_nation,
            'double':    pdf_double,
            'pages':     pdf_pages,
            'foundlist': pdf_foundlist
        }
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return pdf

# Download PROJECT -> get data by ProID
def get_pdfDetailByProId(pro_id):
    table_name = 'pdf_details'
    pdf_details = []
    pdfs = dict()
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        pdf_records, pdf_ids = get_pdfsByProId(cursor, 'pro_pdf_details', pro_id)
        i = 0
        for id in list(pdf_ids):
            pro_keylist = get_proKeyById(cursor, 'project_info', pro_id)
            query = f"""
                        SELECT b.det_id, b.det_info, b.det_attribute, c.att_name, b.det_value, b.det_npage
                        FROM   "{table_name}" b INNER JOIN pdf_attributes c ON b.det_attribute = c.att_id
                        WHERE  b.det_info = {id} and b.det_visible = 1
                        ORDER BY b.det_attribute ASC
                    """
            sqlite_select_query = query
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            pdf_details = []

            for record in records:
                keyname = record[3]
                for key in pro_keylist:
                    if str(record[3]).split('_')[0] == str(key['key_id']) :
                        keyname = key['key_name'] + " " + str(record[3]).split('_')[1]
                        break
                pdf_details.append({
                        'det_id':       record[0],
                        'det_info':     record[1],
                        'det_attribute':record[2],
                        'det_name':     keyname, 
                        'det_value':    record[4],
                        'det_npage':    record[5]
                        })
            pdfs[i] = {
                'id':    pdf_records[i][0],
                'type':  pdf_records[i][1],
                'details':  pdf_details,
            }
            i = i + 1
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return pdfs

# Load ATTRIBUTES -> get data by ProID and PdfID
def get_attributesDetails(pro_id, pdf_id):
    table_name = 'pdf_details'
    pdf_details = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        pro_keylist = get_proKeyById(cursor, 'project_info', pro_id)
        query = f"""
                    SELECT b.det_id, b.det_info, b.det_attribute, c.att_name, b.det_value, b.det_npage
                    FROM   "{table_name}" b INNER JOIN pdf_attributes c ON b.det_attribute = c.att_id
                    WHERE  b.det_info = {pdf_id} and b.det_attribute > 22 and b.det_visible = 1
                    ORDER BY b.det_id ASC
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        pdf_details = []
        for record in records:
            keyname = record[3]
            for key in pro_keylist:
                if str(record[3]).split('_')[0] == str(key['key_id']) :
                    keyname = key['key_name'] + " " + str(record[3]).split('_')[1]
                    break
            if record[4]:
                pdf_details.append({
                        'det_id':       record[0],
                        'det_info':     record[1],
                        'det_attribute':record[2],
                        'det_name':     keyname, 
                        'det_value':    record[4][0:129],
                        'det_npage':    record[5]
                        })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return pdf_details


# Users
def get_listUsers(limit=-1):
    # List of TOP 10
    table_name = 'user'
    users = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    SELECT  id, name, gender, email, active, updated, COUNT(b.pro_id) as num_pro
                    FROM "{table_name}" a LEFT JOIN "project_info" b ON a.id = b.pro_user
                    GROUP BY a.id
                    ORDER BY a.id DESC
                    LIMIT "{limit}"
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            users.append({
                    'usr_id':       record[0],
                    'usr_name':     record[1],
                    'usr_gender':   record[2],
                    'usr_email':    record[3],
                    'usr_active':   record[4],
                    'usr_updated':  record[5],
                    'usr_num_pro':  record[6],
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to connect... ", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return users


def upd_userById(user):
    table_name = 'user'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        query = f"""
                    UPDATE {table_name} SET name="{user['usr_name']}", gender="{user['usr_gender']}", birthday="{user['usr_birthday']}",  email="{user['usr_email']}", phone="{user['usr_phone']}", address="{user['usr_address']}", active={user['usr_active']}, updated="{user['usr_updated']}"
                    WHERE id = {user['usr_id']}
                """
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to update data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
        return result


def upd_statusUserById(user_id, val):
    table_name = 'user'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        # print("Connected to SQLite")
        query = f"""
                    UPDATE {table_name} SET active={val}
                    WHERE id = {user_id}
                """
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