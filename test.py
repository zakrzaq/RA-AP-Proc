# from sap.se16 import se16
# from sap.gts import gts
# from sap.ih09 import ih09
# from sap.sqvi import sqvi
# from sap.text import text

# tables = ["MARC", "MVKE", "AUSP", "MLAN"]

# text()
# ih09()
# for t in tables:
#     se16(t)
# sqvi()
# gts()

import os
from helpers.helpers import ignore_warnings, use_dotenv

import polars as pl
import pandas as pd

use_dotenv()

mara = pd.read_excel(os.path.join(os.environ["DIR_IN"], "MARA.XLSX"))
mara.to_csv(os.path.join(os.environ["DIR_IN"], "mara.csv"))
mara = pl.read_excel(os.path.join(os.environ["DIR_IN"], "MARA.XLSX"))

marc = pd.read_excel(os.path.join(os.environ["DIR_IN"], "MARC.XLSX"))
marc.to_csv(os.path.join(os.environ["DIR_IN"], "marc.csv"))
marc = pl.read_excel(os.path.join(os.environ["DIR_IN"], "MARC.XLSX"))

# mvke = pl.read_excel(os.path.join(os.environ["DIR_IN"], "MVKE.XLSX"))

# ausp = pl.read_excel(os.path.join(os.environ["DIR_IN"], "AUSP.XLSX"))

# mlan = pl.read_excel(os.path.join(os.environ["DIR_IN"], "MLAN.XLSX"))

# gts = pl.read_excel(os.path.join(os.environ["DIR_IN"], "GTS.XLSX"))

# price = pl.read_excel(os.path.join(os.environ["DIR_IN"], "PRICE.XLSX"))

# text = pl.read_excel(os.path.join(os.environ["DIR_IN"], "sales_text.XLS"))


# dfs = [mara, marc, mvke, ausp, mlan, gts, price, text]
# for df in dfs:
#     print(df.head())
