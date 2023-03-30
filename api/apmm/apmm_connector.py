import sqlite3

import helpers.prompts as pr
from state.output import output

apmm_shpoint = r"C:\Users\JZakrzewski\Rockwell Automation, Inc\EDM - AP MM Service Request Process\apmm.db"


def con_apmm():
    try:
        con = sqlite3.connect(apmm_shpoint)
        con.row_factory = sqlite3.Row
        output.add(f"{pr.conn}Successfully connected to APMM Database")
        cur = con.cursor()
        return con, cur
    except:
        output.add(f"{pr.cncl}APMM connection failed")
        return None, None


def close_apmm(con):
    con.commit()
    con.close()
