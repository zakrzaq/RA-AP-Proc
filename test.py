import pandas as pd
import os

from helpers.helpers import (
    use_dotenv,
    ignore_warnings,
    use_logger,
    end_script,
)
from helpers.log import load_log, save_log
from helpers.xlsm import populate_sap_data_sheet, extend_concats
import helpers.prompts as pr
from state.output import output
from api.apmm.apmm_connector import con_apmm
from api.apmm.apmm_log import create_log, create_log_view


def test(server=False):

    use_dotenv()
    use_logger()
    ignore_warnings()

    output.reset()
    sql_dir = os.path.join(os.getcwd(), "api", "apmm", "sql")

    con, cur = con_apmm()

    mara = marc = mvke = ausp = mlan = price = gts = text = pd.DataFrame()

    fl_mara = os.path.join(os.environ["DIR_IN"], "mara.XLSX")
    fl_marc = os.path.join(os.environ["DIR_IN"], "marc.XLSX")
    fl_mvke = os.path.join(os.environ["DIR_IN"], "mvke.XLSX")
    fl_ausp = os.path.join(os.environ["DIR_IN"], "ausp.XLSX")
    fl_mlan = os.path.join(os.environ["DIR_IN"], "mlan.XLSX")
    fl_price = os.path.join(os.environ["DIR_IN"], "price.XLSX")
    fl_gts = os.path.join(os.environ["DIR_IN"], "gts.XLSX")
    fl_text = os.path.join(os.environ["DIR_IN"], "sales_text.xls")

    # load sap data to df
    output.add(f"{pr.info}Loading new SAP data")
    if os.path.exists(fl_mara):
        mara = pd.read_excel(fl_mara)
    if os.path.exists(fl_marc):
        marc = pd.read_excel(fl_marc)
    if os.path.exists(fl_mvke):
        mvke = pd.read_excel(fl_mvke)
    if os.path.exists(fl_ausp):
        ausp = pd.read_excel(fl_ausp)
    if os.path.exists(fl_mlan):
        mlan = pd.read_excel(fl_mlan)
    if os.path.exists(fl_price):
        price = pd.read_excel(fl_price)
    if os.path.exists(fl_gts):
        gts = pd.read_excel(fl_gts)
    if os.path.exists(fl_text):
        text = pd.read_csv(fl_text, sep="\t", encoding="utf-16")

    if con:
        output.add(f"{pr.conn}Uploading to APMM")
        # try:
        mara.to_sql("mara", con, if_exists="replace", index=False)
        marc.to_sql("mara", con, if_exists="replace", index=False)
        mvke.to_sql("mara", con, if_exists="replace", index=False)
        ausp.to_sql("mara", con, if_exists="replace", index=False)
        mlan.to_sql("mara", con, if_exists="replace", index=False)
        gts.to_sql("mara", con, if_exists="replace", index=False)
        price.to_sql("mara", con, if_exists="replace", index=False)
        text.to_sql("mara", con, if_exists="replace", index=False)
        create_log()
        create_log_view()
        output.add(f"{pr.done}APMM updated")

        # except:
        #     output.add(f"{pr.cncl}APMM failed to update")


# test()
create_log()
