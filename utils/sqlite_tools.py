import sqlite3
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

def get_ThesisByName(file_pdf):
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
    # table_colnames = None
    pdfs = []
    # pdf_foundlistY = []      #   Atributos Encontrados SI
    # pdf_foundlistN = []      #   Atributos Encontrados NO
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        # pdf_info = get_pdf_info(cursor, table_name, keyword)
        # pdf_id, pdf_name, pdf_npages = pdf_info
        query = f"""
                    SELECT a.pdf_id, a.pdf_name, a.pdf_npages, a.pdf_size, b.det_value, c.key_name
                    FROM (pdf_info a INNER JOIN pdf_details b ON a.pdf_id = b.det_info) INNER JOIN pdf_keywords c ON a.pdf_id = c.key_info
                    WHERE c.key_name LIKE "%{keyword}%" AND b.det_attribute = 2
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
            print("The SQLite connection is closed")
        
        return pdfs

# def update_DetailByIds(pd_id, pd_pdf, text, num):
def update_DetailByIds(det_id, det_info, det_attribute, text, npage=1, rect=dict):
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


"""
def readAllTable():
    data_base = 'db.sqlite'
    table_name = 'pdf_detail'
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        
        sqlite_select_query = 'SELECT * from pdf_detail'
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row\n")

        for row in records:
            print("pdf_id: ",       row[1])
            print("pe_author: ",    row[2])
            print("pe_title: ",     row[3])
            print("pe_entity: ",    row[4])
            print("pe_abstract: ",  row[5])
            print("ct_method: pag.",    row[16])
            print("\n")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
"""

# readAllTable()
# readOneTable()