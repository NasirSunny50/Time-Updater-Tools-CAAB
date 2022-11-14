# import pyodbc
# print(pyodbc.drivers())

import sys
import socket
import pyodbc as odbc
from datetime import datetime

# step 1

now = datetime.now()
cur_time = now.strftime('%m/%d/%Y %H:%M:%S.%f')


DRIVER = 'ODBC Driver 17 for SQL Server'
SERVER_NAME = '********'
DATABASE_NAME = '********'
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
    # messagebox.showerror('TimeUpdater','Connection Error. Please Check Your Authorization!')
    sys.exit()
else:
    print('Connected Successfully')
    cursor = conn.cursor()


def branch(value):
    select_statement = """
        SELECT LastOpenDate FROM UFN_SFS_GetLastOpenDateInfo(?)
    """

    select = [
        [value]
    ]

    for i in select:
        print(i)
        cursor.execute(select_statement, i)
    print("Successful")

    max_date = ''
    # Step 2
    for i in cursor:
        max_date = (str(i[0]))
        print(max_date)

    try:
        update_statement = """
                UPDATE SFS_VALIDTRANSACTIONDATETIME SET VTDENDTIME=? WHERE VTDBRANCHCODE=? AND VTDTRANSDATE=?
        """
        update = [
            [cur_time[:23], value, max_date[:23]]
        ]
    except Exception:
        print('Date already exists!')
        # messagebox.showerror('TimeUpdater','Date already exists!')
        sys.exit()
    else:
        for i in update:
            print(i)
            cursor.execute(update_statement, i[:23])
        print('records updated successfully')
        # messagebox.showinfo('TimeUpdater','Success!')

    insert_statement = """
        INSERT INTO SFS_VALIDTRANSACTIONDATETIME
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    records = [
        [value, cur_time[:23], cur_time[:23], None, 'Scheduler', None, None, None, cur_time[:23], 'Scheduler', 'N',
         '1']
    ]
    # Step 4
    for i in records:
        print(i)
        cursor.execute(insert_statement, i)
    print('records inserted successfully')

    cursor.commit()


branch("0007")
branch("0008")
branch("0009")
branch("0010")
cursor.close()

print('connection closed')
conn.close()
