import sqlite3
import secrets
import json
import os

def get_pdf_info(cursor, tablename, file_pdf):
    """Get column names of main table, given its name and a cursor (or connection) to the database.
    """
    query = f"""
                SELECT pdf_id, pdf_name, pdf_npages FROM {tablename}
                WHERE pdf_name = "{file_pdf}" 
            """
    cursor.execute(query)
    return cursor.fetchone()

def get_col_names(cursor, tablename):
    """Get column names of a table, given its name and a cursor
       (or connection) to the database.
    """
    reader=cursor.execute("SELECT * FROM {}".format(tablename))
    return [x[0] for x in reader.description] 

def get_thesisByName(file_pdf):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pdf_attributes'
    table_colnames = None
    pdf = dict()
    pdf_foundlistY = []      #   Atributos Encontrados SI
    pdf_foundlistN = []      #   Atributos Encontrados NO
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        pdf_info = get_pdf_info(cursor, 'pdf_info', file_pdf)
        pdf_id, pdf_name, pdf_npages = pdf_info
        query = f"""
                    SELECT b.det_id, b.det_attribute, c.att_name, b.det_value, b.det_npage, b.det_x, b.det_y, b.det_width, b.det_height
                    FROM (pdf_info a INNER JOIN pdf_details b ON a.pdf_id = b.det_info) INNER JOIN pdf_attributes c ON b.det_attribute = c.att_id
                    WHERE a.pdf_id = "{pdf_id}" 
                    ORDER BY b.det_id ASC
                """ 
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        
        for record in records:
            if record[3] :
                pdf_foundlistY.append({
                                'det_id':       record[0],
                                'det_attribute':record[1],
                                'det_name':     record[2], 
                                'det_value':    record[3],
                                'det_npage':    record[4],
                                'det_x':        record[5],
                                'det_y':        record[6],
                                'det_width':    record[7],
                                'det_height':   record[8]
                                })
            else:
                pdf_foundlistN.append({
                                'det_id':       record[0],
                                'det_attribute':record[1],
                                'det_name':     record[2]
                                })

        pdf = {
            'id':           pdf_id,
            'name':         pdf_name,
            'npages':       pdf_npages,
            'foundlistY':   pdf_foundlistY,
            'foundlistN':   pdf_foundlistN,
        }
        # print(json.dumps(pdf))
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
        return pdf

def get_listThesisByWord(keyword):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pdf_keywords'
    pdfs = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    SELECT a.pdf_id, a.pdf_name, a.pdf_npages, a.pdf_size, b.det_value, d.key_name
                    FROM  ((pdf_info a INNER JOIN pdf_details b ON a.pdf_id = b.det_info) INNER JOIN pdf_key_details c ON a.pdf_id = c.pdf_id) INNER JOIN key_info d ON c.key_id = d.key_id
                    WHERE d.key_name LIKE "%{keyword}%" AND b.det_attribute = 2
                """
        print(query)
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
            print("The SQLite connection is closed")
        return pdfs

def upd_detailByIds(det_id, det_info, det_attribute, text, npage=1, rect=dict):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pdf_details'
    # table_colnames = None
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    UPDATE pdf_details SET det_value="{text}", det_npage={npage}, det_x={rect['x']}, det_y={rect['y']}, det_width={rect['w']}, det_height={rect['h']}
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
            print("The SQLite connection is closed")
        
        return result


# ----------------------------------- FORM UPLOAD -----------------------------------
def put_newProject(project=dict):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'project_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()

        print(json.dumps(project))
        print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (pro_title, pro_uni, pro_career, pro_type, pro_n_articles, pro_n_process, pro_created) 
                    VALUES ("{project['title']} ", "{project['university']}", "{project['career']}", "{project['type']}", "{project['n_articles']}", "{project['n_process']}", "{project['created']}")
                """
        print(query)
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
            print("The SQLite connection is closed")
        
        return result, id

def put_newPKdetail(id, key, current_date):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pro_key_details'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    INSERT INTO "{table_name}" (pro_id, key_id, pro_key_created)
                    VALUES ("{id} ", "{key}", "{current_date}")                
                """
        print(query)
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

def get_listUniversities():
    # List of TOP 10
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'uni_info'
    universities = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    SELECT uni_id, uni_name, uni_nickname
                    FROM "{table_name}"
                    WHERE  uni_active = 1
                """
        print(query)
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
            print("The SQLite connection is closed")
        return universities

def get_listKeywords():
    # List of TOP 10
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'key_info'
    keywords = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    SELECT key_name
                    FROM "{table_name}"
                    WHERE  key_active = 1
                """
        print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            keywords.append(record[0])
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return keywords

def get_listProjects():
    # List of TOP 10
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'project_info'
    projects = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    SELECT a.pro_id, a.pro_title, b.uni_nickname, a.pro_career
                    FROM "{table_name}" a INNER JOIN uni_info b ON a.pro_uni = b.uni_id
                    ORDER BY a.pro_id DESC
                    LIMIT 5
                """
        print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            projects.append({
                    'pro_id':       record[0],
                    'pro_title':    record[1],
                    'pro_uni':      record[2],
                    'pro_career':   record[3],
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return projects

def get_projectById(id):
    # List of TOP 10
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'project_info'
    project = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    SELECT a.pro_title, b.uni_name, a.pro_career, a.pro_type, a.pro_n_articles, a.pro_n_process, a.pro_created
                    FROM "{table_name}" a INNER JOIN uni_info b ON a.pro_uni = b.uni_id
                    WHERE  a.pro_id = "{id}"
                """
        print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        record = cursor.fetchone()
        project.append({
                'pro_title':      record[0],
                'pro_uni':        record[1],
                'pro_career':     record[2],
                'pro_type':       record[3],
                'pro_n_articles': record[4],
                'pro_n_process':  record[5],
                'pro_date':       record[6],
            })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return project

def get_pkDetailById(id):
    # List of TOP 10
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pro_key_details'
    pk_details = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    SELECT c.key_name
                    FROM   (project_info a INNER JOIN "{table_name}" b ON a.pro_id = b.pro_id) INNER JOIN key_info c ON b.key_id = c.key_id
                    WHERE  b.pro_id = "{id}"
                """
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        for record in records:
            pk_details.append({
                'key_name':  record[0]
            })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return pk_details

def upd_projectById(id, n_articles, n_process):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'project_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    UPDATE "{table_name}" SET pro_n_articles="{n_articles}", pro_n_process={n_process}
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
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'project_info'
    projects = []
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        query = f"""
                    SELECT DISTINCT a.pro_id, a.pro_title, a.pro_career, a.pro_n_articles, a.pro_n_process, a.pro_created
                    FROM  ("{table_name}" a INNER JOIN pro_key_details b ON a.pro_id = b.pro_id) INNER JOIN key_info c ON b.key_id = c.key_id
                    WHERE a.pro_title LIKE "%{keyword}%" OR c.key_name LIKE "%{keyword}%"
                """
        print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        # print(json.dumps(records))

        colors = ['primary', 'success', 'danger', 'warning', 'info', 'dark']
        # years = []
        for record in records:
            # if record[5].split('/')[-1] in years:
            projects.append({
                    'pro_id':         record[0],
                    'pro_title':      record[1],
                    'pro_career':     record[2],
                    'pro_n_articles': record[3], 
                    'pro_n_process':  record[4],
                    'pro_created':    record[5],
                    'pro_color':      secrets.choice(colors)
                    })
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to list data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return projects