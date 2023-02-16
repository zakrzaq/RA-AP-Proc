import oracledb

from rtd_config import username, password, RTD

import helpers.prompts as pr
from state.output import output


def connect_rtd():
    try:
        con = oracledb.connect(
            user=username,
            password=password,
            dsn=RTD,
        )

        output.add(f"{pr.conn}Successfully connected to Oracle RTD Database")

        cur = con.cursor()
        return con, cur

    except oracledb.DatabaseError as e:
        output.add(f"{pr.conn}RTD disconnected")
        return None


def close_rtd(con, cur):
    cur.close()
    con.close()
