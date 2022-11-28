
import cx_Oracle
import os
import dotenv
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
lib_dir = r"C:\Program Files (x86)\InstantClient"
os.environ["PATH"] = lib_dir + ";" + os.environ["PATH"]

# # import getpass # library to input password

username = os.environ['RTD_USR']
password = os.environ['RTD_PSW']
db_service = 'rtd'

try:
    # input username and password
    # username = input("Please enter your FDW username: ")
    # password = getpass.getpass("Enter your LDAP password: ")

    # read sql query from file
    sqlfilename = "test.sql"
    f = open(sqlfilename)
    sql_string = f.read()
    print("SQL = " + sql_string)

    # set up connection through LDAP
    con = cx_Oracle.connect(
        '{0}/{1}@[{2}]][.]'.format(username, password, db_service))

    # create a cursor instance
    cursor = con.cursor()

    # run the query
    cursor.execute(sql_string)

    # print out metadata
    for column in cursor.description:
        print(column)

except cx_Oracle.DatabaseError as e:
    print("There is a problem with Oracle", e)

finally:
    if cursor:
        cursor.close()
    if con:
        con.close()
