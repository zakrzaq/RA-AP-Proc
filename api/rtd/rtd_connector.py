import oracledb
import os

from rtd_config import username, password, RTD


def connect_rtd():
    try:
        con = oracledb.connect(
            user=username,
            password=password,
            dsn=RTD,
        )

        print("Successfully connected to Oracle Database")

        cur = con.cursor()
        return con, cur

    except oracledb.DatabaseError as e:
        print(e)
        return None


def close_rtd(con, cur):
    cur.close()
    con.close()
