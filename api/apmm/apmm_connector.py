import sqlite3, os

import utils.prompts as pr
from state.output import output

apmm_shpoint = os.environ["AP_DB_DEV"]


def con_apmm():
    try:
        con = sqlite3.connect(apmm_shpoint)
        con.row_factory = sqlite3.Row
        output.add(f"{pr.conn}Successfully connected to APMM_DEV DB")
        cur = con.cursor()
        return con, cur
    except:
        output.add(f"{pr.cncl}APMM_DEV DB connection failed")
        return None, None


def close_apmm(con):
    con.commit()
    con.close()
