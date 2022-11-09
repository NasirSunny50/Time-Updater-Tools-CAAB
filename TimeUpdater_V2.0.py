import sys
import PySimpleGUI as sg
import socket
import pyodbc as odbc
from datetime import datetime
from tkinter import *
from tkinter import messagebox

# step 1
try:
    now = datetime.now()
    cur_time = now.strftime('%m/%d/%Y %H:%M:%S.%f')

    records = [
        ['0007', cur_time[:23], cur_time[:23], None, 'Scheduler', None, None, None, cur_time[:23], 'Scheduler', 'N', '1']
    ]

    DRIVER = 'SQL Server'
    SERVER_NAME = '*******'
    DATABASE_NAME = '******'
    USER = '*******'
    PW = '*******'

    conn_string = f"""
        Driver={{{DRIVER}}};
        Server={SERVER_NAME};
        Database={DATABASE_NAME};
        UID={USER};
        PWD={PW};
    """

    try:
        conn = odbc.connect(conn_string)
    except Exception:
        print('Connection Error. Please Check Your Authorization')
        messagebox.showerror('TimeUpdater','Connection Error. Please Check Your Authorization!')
        sys.exit()
    else:
        cursor = conn.cursor()

    select_statement = """
        SELECT LastOpenDate FROM UFN_SFS_GetLastOpenDateInfo('0007')
    """



    cursor.execute(select_statement)

    max_date = ''
    # Step 2
    for i in cursor:
        max_date = (str(i[0]))
        print(max_date)

    try:
        update_statement ="""
                UPDATE SFS_VALIDTRANSACTIONDATETIME SET VTDENDTIME=? WHERE VTDBRANCHCODE='0007' AND VTDTRANSDATE=?
        """
        update = [
            [cur_time[:23], max_date]
        ]
    except Exception:
        messagebox.showerror('TimeUpdater','Date already exists!')
        sys.exit()
    else:
        for i in update:
            print(i)
            cursor.execute(update_statement, i[:23])
        print('records updated successfully')
        messagebox.showinfo('TimeUpdater','Success!')

    insert_statement = """
        INSERT INTO SFS_VALIDTRANSACTIONDATETIME
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """
    # Step 4
    for i in records:
        print(i)
        cursor.execute(insert_statement, i)
    print('records inserted successfully')

    cursor.commit()
    cursor.close()
except Exception:
    messagebox.showerror('TimeUpdater','Date already exists!')
    sys.exit()


print('connection closed')
conn.close()
