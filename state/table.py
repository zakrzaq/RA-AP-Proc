import pandas as pd

from helpers.data_frames import get_single_sap, df_to_list
from helpers.log import load_log


class Table:
    def __init__(self, table):
        self.table = table
        self.df: pd.DataFrame = get_single_sap(table)

    def __getitem__(self):
        return self.df
        # return f"{self.table.upper()}: {self.df.shape}"

    def data(self):
        return self.df

    def load(self):
        self.df = get_single_sap(self.table)

    def array(self) -> list:
        return df_to_list(self.df)


tbl_mara = Table("MARA")
tbl_marc = Table("MARC")
tbl_mvke = Table("MVKE")
tbl_ausp = Table("AUSP")
tbl_mlan = Table("MLAN")
tbl_price = Table("PRICE")
tbl_gts = Table("GTS")
tbl_text = Table("SALES_TEXT")

tables = [
    tbl_text,
    tbl_mara,
    tbl_marc,
    tbl_mvke,
    tbl_ausp,
    tbl_mlan,
    tbl_price,
    tbl_gts,
]
