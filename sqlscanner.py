from tkinter import *
#from PIL import ImageTk
import requests
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
from pprint import pprint
import re


s = requests.Session()
s.headers["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"

root = Tk()

root.title("SQL Injection")
root.geometry("550x500+200+70")
root.resizable(False, False)
#image = ImageTk.PhotoImage(file="foto.jpg")
label = Label(root)
label.pack()

frame = Frame(root)
frame.place(x=0, y=0, width=550, height=500)
frame.config(bg="#ffee38")

validateLabel = Label(frame, text="", font=("Andalus", 8 , 'bold'), fg='#000000', bg="#91cbde")
validateLabel.place(x=80, y=0)

Label(frame, text="URL :", font=("Bahnschift bold SemiCondensed ", 16), bg="#ffee38", fg="navy").place(
            x=40, y=60)

entryUrl = Entry(frame, font=("times new roman", 15))
entryUrl.place(x=110, y=64, width=390)

Label(frame, text="Results after scanning", font=("Bahnschift bold SemiCondensed ", 16), bg="#ffee38", fg="navy").place(
            x=165, y=210)

txt = Text(frame, width=58, height=10, wrap=WORD)
txt.place(x=45, y=240)
txt.configure(state="disable")

def delete():
    entryUrl.delete(0,END)
    validateLabel.config(text=" ")
    txt.configure(state="normal")
    txt.delete('1.0', END)
    txt.configure(state="disable")

button1 = Button(frame, text='Delete this scan', activebackground="#00b0f0", activeforeground='white', fg='#000000',
               bg="#ea4343", font=("Arial", 13, 'bold'), command=delete)
button1.place(x=310, y=410, width=185)

def valid():
    if not ((entryUrl.get().startswith("http://") or entryUrl.get().startswith("https://"))):
        validateLabel.config(text="URL should start with http:// or https://")
        return False
    return True

def is_vulnerable(response):
    """A simple boolean function that determines whether a page 
    is SQL Injection vulnerable from its `response`"""
    errors = {
        # MySQL
        "you have an error in your sql syntax;",
        "warning: mysql",
        # SQL Server
        "unclosed quotation mark after the character string",
        # Oracle
        "quoted string not properly terminated",
    }
    for error in errors:
        # if you find one of these errors, return True
        if error in response.content.decode().lower():
            return True
    # no error detected
    return False


def scan_sql_injection():
    output = ""
    # test on URL
    for c in "\"'":
        # add quote/double quote character to the URL
        print("[!] URL=", entryUrl.get())
        new_url = f"{entryUrl.get()}{c}"
        output += "[!] Trying " + new_url
        # make the HTTP request
        res = s.get(new_url)
        if is_vulnerable(res):
            # SQL Injection detected on the URL itself, 
            # no need to preceed for extracting forms and submitting them
            print("[+] SQL Injection vulnerability detected, link:", new_url)
            output += os.linesep + "[+] SQL Injection vulnerability detected"
            output += os.linesep + "Target is vulnerable."
            urls = [new_url + "'", new_url + '"', new_url[:-4] + ';',
                    new_url + ")", new_url + "')", new_url + '")',
                    new_url + '*']
            DBDict = {
                "MySQL": ['MySQL', 'MySQL Query fail:', 'SQL syntax', 'You have an error in your SQL syntax',
                          'mssql_query()', 'mssql_num_rows()', 'warning: mysql'],
                "PostGre": ['PostgreSQL.*?ERROR','valid PostgreSQL result','Npgsql\.', ,'PG::SyntaxError:', 'dafafdfds'],
                "Microsoft_SQL": ['Driver.*? SQL[\-\_\ ]*Server','Warning.*?\W(mssql|sqlsrv)_','Microsoft SQL Native Client error "'[0-9a-fA-F]{8}"','\[SQL Server\]','dafafdfds'],
                "Oracle": ['Oracle error','Warning.*?\W(oci|ora)_','SQL command not properly ended','dafafdfds'],
                "Advantage_Database": ['dafafdfds'],
                "Firebird": ['dafafdfds']
            }
            DBFound = 0
            DBType = ''
            try:
                for url in urls:
                    results = requests.get(url)
                    data = results.text
                    soup = bs(data, features='html.parser')
                    while not DBFound:
                        for db, identifiers in DBDict.items():
                            for dbid in identifiers:
                                if dbid in data.lower():
                                    DBType = db
                                    DBFound = 1
                                    output += os.linesep + "Database is " + db
                                    print("databaza" + db)
                                    break
            except:
                DBType = 'Unknown'
            if (len(output) > 1):
                txt.insert(1.0, output)
            return
        else:    
            output += os.linesep + "Target is secure"  
            if (len(output) > 1):
                txt.insert(1.0, output)  
            return

def scan():
    txt.configure(state="normal")
    txt.delete('1.0', END)
    if valid():
        scan_sql_injection()
    txt.configure(state="disable")

button = Button(frame, text='SCAN', activebackground="#00b0f0", activeforeground='white', fg='#ffee38',
                bg="navy", font=("Arial", 15, 'bold'), command=scan)
button.place(x=180, y=120, width=185)


if __name__ == "__main__":
    root=mainloop()
    
    

