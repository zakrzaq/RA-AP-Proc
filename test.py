from helpers.log import *
from helpers.xlsm import *

log = load_log()
if log != None:
    ws_mif = log["mif"]
    print(ws_mif)
    mif_last_row = get_first_empty_row(ws_mif, "B")
    print(mif_last_row)
