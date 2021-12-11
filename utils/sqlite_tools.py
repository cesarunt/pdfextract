import sqlite3
import json
import os

def get_col_names(cursor, tablename):
    """Get column names of a table, given its name and a cursor
       (or connection) to the database.
    """
    reader=cursor.execute("SELECT * FROM {}".format(tablename))
    return [x[0] for x in reader.description] 

def get_ThesisByName(file_pdf):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pdf_detail'
    table_colnames = None
    pdf = dict()
    pdf_foundlistY = []      #   Atributos Encontrados SI
    pdf_foundlistN = []      #   Atributos Encontrados NO
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        table_colnames = get_col_names(cursor, table_name)
        query = f'SELECT a.pdf_name, a.pdf_npage, b.* FROM pdf a INNER JOIN pdf_detail b ON a.pdf_id = b.pd_pdf WHERE a.pdf_name = "{file_pdf}" ORDER BY pd_id DESC LIMIT 2' 
        # print(query)
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()

        row = 0
        for record in records:
            if row == 0 :
                record_num = record
            if row == 1:
                i = 4
                for value in record[4:-1]:
                    if value :
                        pdf_foundlistY.append({
                                        'colname':  table_colnames[i-2], 
                                        'value':    str(table_colnames[i-2].split('_')[-1]).capitalize(),
                                        'num':      record_num[i]
                                        })
                    else:
                        pdf_foundlistN.append({
                                        'colname':  table_colnames[i-2], 
                                        'value':    str(table_colnames[i-2].split('_')[-1]).capitalize(),
                                        'num':      None
                                        })
                    i+=1
            row=row+1
            print("...")
        
        pdf = {
            'id':           record[2],
            'det':          record[3],
            'name':         record[0],
            'npage':        record[1],
            'foundlistY':   pdf_foundlistY,
            'foundlistN':   pdf_foundlistN,
        }
        print(json.dumps(pdf))
        cursor.close()
    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        
        return pdf


def update_DetailByIds(pd_id, pd_pdf, text, num):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'pdf_detail'
    table_colnames = None
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        # table_colnames = get_col_names(cursor, table_name)
        query = f'UPDATE pdf_detail SET pd_titulo = "{text}" WHERE pd_id = "{pd_id}" AND pd_pdf = "{pd_pdf}"' 
        sqlite_select_query = query
        cursor.execute(sqlite_select_query)
        query = f'UPDATE pdf_detail SET pd_titulo = "{num}" WHERE (pd_id = 5 OR pd_id = 6) AND pd_pdf = "{pd_pdf}"'
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