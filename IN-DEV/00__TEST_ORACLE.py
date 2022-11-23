
import os
lib_dir=r"C:\Program Files (x86)\InstantClient"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]

# import cx_Oracle
# # import getpass # library to input password

username = 'JZAKRZE'
password = 'AlexEllaJudy2022!'
db_service = 'rtd'

# try: 
#     # input username and password
#     # username = input("Please enter your FDW username: ")
#     # password = getpass.getpass("Enter your LDAP password: ")

#     # read sql query from file
#     sqlfilename = "test.sql"
#     f = open(sqlfilename)
#     sql_string = f.read()
#     print("SQL = " + sql_string)

#     # set up connection through LDAP
#     con = cx_Oracle.connect('{0}/{1}@[rtd][.]'.format(username, password)) 
      
#     # create a cursor instance 
#     cursor = con.cursor() 
      
#     # run the query 
#     cursor.execute(sql_string) 

#     # print out metadata
#     for column in cursor.description:
#         print(column)
      
# except cx_Oracle.DatabaseError as e: 
#     print("There is a problem with Oracle", e) 
  
# finally: 
#     if cursor: 
#         cursor.close() 
#     if con: 
#         con.close() 

import cx_Oracle
# con = cx_Oracle.connect('{0}/{1}@{2}'.format(username, password, db_service))
con = cx_Oracle.connect("JZAKRZE/EllaAlexJudy2022!@https://jameson.mke.ra.rockwell.com:1534/rtd.mke.ra.rockwell.com", mode=cx_Oracle.SYSDBA)

version_script = "SELECT * FROM v$version"
cursor = con.cursor()
cursor.execute(version_script)
version = cursor.fetchall()
print(version[0][0])

# JZAKRZE/EllaAlexJudy2022!@//jameson.mke.ra.rockwell.com:1534/rtd.mke.ra.rockwell.com