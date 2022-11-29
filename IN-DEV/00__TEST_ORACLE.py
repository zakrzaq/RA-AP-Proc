
import cx_Oracle
import os
lib_dir = r"C:\oracle\ora121"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]

# # import getpass # library to input password
username = 'jzakrze'
password = 'raint2022!'
db_service = 'rtd'

try:
    sqlfilename = "test.sql"
    sqlfilename = r"C:\Users\JZakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\New AP Process\APP\SQL\1_insert.sql"
    # sqlfilename = r"C:\Users\JZakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\AP_MIF_SOERF.sql"
    # sqlfilename = r"C:\Users\JZakrzewski\dev\RA-SCRIPTS\SQL\AP PROC\2021-09-22 - Tax V in 5070.sql"
    f = open(sqlfilename)
    sql_string = f.read()
    connection = cx_Oracle.connect('jzakrze/raint2022@rtd')
    cursor = connection.cursor()

    # run the query
    # for r in cursor.execute(sql_string):
    #     print(r)

    cursor.execute(sql_string)

    # # table description
    # for column in cursor.description:
    #     print(column)

    # # return each row - OR
    # # for row in cursor:
    # #     print(row)

    # # download all date and process by row - OR
    # rows = cursor.fetchall()
    # for r in rows:
    #     print(r)

except cx_Oracle.DatabaseError as e:
    print("There is a problem with Oracle", e)

# finally:
#     if cursor:
#         cursor.close()
#     if connection:
#         connection.close()
