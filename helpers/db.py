import os
import sqlite3


def con_db():
    con = sqlite3.connect(os.path.join(os.getcwd(), 'api', 'db', "apmm.db"))
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur


def close_db(con):
    con.commit()
    con.close()
