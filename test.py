import os
import pandas as pd

from helpers.helpers import use_dotenv
from api.apmm.apmm_connector import con_apmm, close_apmm

use_dotenv()

files = {
    "data": os.path.join(os.environ["DIR_OUT"], "TEST_sap_load.xlsx"),
    "ap_log": os.environ["AP_LOG"],
}

table = "log"
sheet = "log"

df = pd.DataFrame()
df = pd.read_excel(files["data"])
# df = pd.read_excel(files["ap_log"], sheet)

if not df.empty:
    print(list(df.columns))
    print(df.dtypes)

match table:
    case "mif":
        columns = ["matnr", "dwerk", "concat", "date"]
        df.columns = columns
        df = df.drop(columns=["concat"])
        df["matnr"] = df["matnr"].astype("str")
        df["dwerk"] = df["dwerk"].map(lambda x: str(x)[:-2])
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    case "soerf":
        columns = ["matnr", "cat_no", "vkorg", "concat", "date"]
        df.columns = columns
        df = df.drop(columns=["concat"])
        df["matnr"] = df["matnr"].astype("str")
        df["cat_no"] = df["cat_no"].astype("str")
        df["vkorg"] = df["vkorg"].map(lambda x: str(x)[:-2])
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    case "pce":
        columns = [
            "concat",
            "matnr",
            "klart",
            "certification",
            "assesment",
            "date",
            "assesor",
        ]
        df.columns = columns
        df = df.drop(columns=["concat", "assesor"])
        df["matnr"] = df["matnr"].astype("str")
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    case "pce_archive":
        columns = [
            "concat",
            "matnr",
            "klart",
            "certification",
            "assesment",
            "date",
            "assesor",
        ]
        df.columns = columns
        df = df.drop(columns=["concat", "assesor"])
        df["matnr"] = df["matnr"].astype("str")
        df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.date
    case _:
        print("no table matched")

con, cur = con_apmm()
if con and not df.empty:
    df.to_sql(table, con=con, index=False)


from api.queries import get_json_data

print(get_json_data("select_all"))
