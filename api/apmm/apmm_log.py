import os
import pandas as pd
from api.apmm.apmm_connector import con_apmm, close_apmm
from helpers.data_frames import get_active

sql_dir = os.path.join(os.getcwd(), "api", "apmm", "sql")


def create_log():
    con, cur = con_apmm()
    if con:
        log = get_active()

        sel1 = log.iloc[:, :7]
        sel2 = log.iloc[:, 51:58]
        sel = pd.concat([sel1, sel2])

        with open(os.path.join(sql_dir, "create_log.sql")) as f:
            con.executescript(f.read())

        sel1.to_sql("log", con, if_exists="replace", index=False)
        con.commit()

        close_apmm(con)


def create_log_view():
    con, cur = con_apmm()

    if con:
        with open(os.path.join(sql_dir, "drop_log_view.sql")) as f:
            con.executescript(f.read())

        with open(os.path.join(sql_dir, "create_log_view.sql")) as f:
            con.execute(f.read())

    close_apmm(con)
