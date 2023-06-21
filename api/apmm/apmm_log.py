import pandas as pd
from api.apmm.apmm_connector import con_apmm, close_apmm
from utils.data_frames import get_active
from utils.helpers import get_dictionary_value
from data.files import apmm_dev_sql


def create_log():
    con = con_apmm()[0]
    if con:
        log = get_active()

        sel1 = log.iloc[:, :7]
        sel2 = log.iloc[:, 51:58]
        sel = pd.concat([sel1, sel2])

        with open(
            get_dictionary_value(apmm_dev_sql, "name", "create_log", "path")
        ) as f:
            con.executescript(f.read())

        sel.to_sql("log", con, if_exists="replace", index=False)
        con.commit()

        close_apmm(con)


def create_log_view():
    con = con_apmm()[0]

    if con:
        with open(
            get_dictionary_value(apmm_dev_sql, "name", "drop_log_view", "path")
        ) as f:
            con.executescript(f.read())

        with open(
            get_dictionary_value(apmm_dev_sql, "name", "create_log_view", "path")
        ) as f:
            con.execute(f.read())

    close_apmm(con)
