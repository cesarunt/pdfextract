import pandas as pd
import sqlite3
import os
from datetime import date

def put_newUniversity(df):
    data_base = os.path.abspath(os.getcwd())+'/db.sqlite'
    table_name = 'uni_info'
    result = False
    try:
        sqliteConnection = sqlite3.connect(data_base)
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")
        current_date = date.today().strftime("%d/%m/%Y")
        # Insert DataFrame to Table
        for row in df.itertuples():
            # try:
                query = f"""
                        INSERT INTO "{table_name}" (uni_name, uni_nickname, uni_type, uni_validity, uni_venues, uni_created)
                        VALUES ("{row.uni_name} ", "{row.uni_nickname}", "{row.uni_type}", "{row.uni_validity}", "{row.uni_venues}", "{current_date}") 
                    """
                cursor.execute(query)
            # except Exception as e:
            #     print("Error... ", e)
            #     result= False
        sqliteConnection.commit()
        result = True
    except sqlite3.Error as error:
        print("Failed to insert data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")
        return result


data = pd.read_csv (r'/Users/cesar/Projects/esConsultores/project-v2/source-code/pdfextract/files/list_uni_process.csv')   
df = pd.DataFrame(data)
# print(df)
result = put_newUniversity(df)
print(result)