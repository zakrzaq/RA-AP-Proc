import os
import sqlite3
# import shutil

apmm_shpoint = r'C:\Users\JZakrzewski\Rockwell Automation, Inc\EDM - AP MM Service Request Process\apmm.db'
# apmm_local = os.path.join(os.getcwd(), 'api', 'db', "apmm.db")


def con_db():
    con = sqlite3.connect(apmm_shpoint)
    # con = sqlite3.connect(apmm_local)
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    return con, cur


def close_db(con):
    con.commit()
    con.close()
    # shutil.copyfile(apmm_shpoint, apmm_local)
