import os
import time
import win32com.client as win32
from helpers.helpers import use_dotenv, use_coinit
from helpers.datetime import mif_date
import helpers.prompts as pr
from state.output import output

use_dotenv()
use_coinit()

user = os.environ["USER_NAME"]
mif_in = os.path.join(os.environ["DIR_OUT"], "AP_MIF.xlsx")
soerf_in = os.path.join(os.environ["DIR_OUT"], "AP_SOERF.xlsx")
mif_out = rf"\\usmkevfile002\dev-compinfo\EDM\Request Logs\Material Master Extension\MIFs awaiting processing\{user} MIF_{mif_date()}_V38.xls"
soerf_out = rf"\\usmkevfile002\dev-compinfo\EDM\Request Logs\Material Master Extension\SOERFs awaiting processing\{user} SOERF_{mif_date()}_V12.xls"


def extension_xlsx_to_xls(file, new_file):
    if ("AP_SOERF.xlsx" in file) or ("AP_MIF.xlsx" in file):
        xlApp = win32.Dispatch("Excel.Application")
        output.add(f"{pr.file}{file}")
        xlWb = xlApp.Workbooks.Open(file)
        xlWb.SaveAs(new_file, FileFormat=1)
        xlWb.Close()
        output.add(f"{pr.prmt}{new_file}")
        time.sleep(2)  # give Excel time to quit, otherwise files may be locked
        # os.unlink(file)
        xlApp.Quit()


def send_extensions():
    extension_xlsx_to_xls(mif_in, mif_out)
    extension_xlsx_to_xls(soerf_in, soerf_out)
