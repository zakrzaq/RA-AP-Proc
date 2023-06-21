import os
import time
import win32com.client as win32
from utils.helpers import use_dotenv, use_coinit
from utils.datetime import mif_date
from utils.helpers import use_coinit
import utils.prompts as pr

from state.email import email as email_state
from state.output import output

use_dotenv()
use_coinit()


def send_email(file=None):
    use_coinit()

    email = email_state.get()

    outlook = win32.Dispatch("Outlook.application")

    if outlook:
        mail = outlook.CreateItem(0)
        mail.To = email["to"]
        mail.cc = email["cc"]
        mail.Subject = email["subject"]
        mail.body = email["body"]
        if file != None:
            mail.Attachments.Add(file)
        mail.Send()

        email_state.reset()
        output.add(f"{pr.email}Email {email['subject']} sent")
    else:
        output.add(f"{pr.cncl}Failed to connect to Outlook")


def send_extensions() -> None:
    """Save OUTPUTS mif/soerf and saves to correct dirs in EDM drive"""

    def extension_xlsx_to_xls(file: str, new_file: str) -> None:
        """Saves mif/soerf XLSX from OUTPUT to XLS format to be used in MM extension

        Params:
        file: str, path to input XLSX files
        new_file: str, path to output XLS files"""

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

    user = os.environ["USER_NAME"]
    mif_in = os.path.join(os.environ["DIR_OUT"], "AP_MIF.xlsx")
    soerf_in = os.path.join(os.environ["DIR_OUT"], "AP_SOERF.xlsx")
    mif_out = os.path.join(
        os.environ["EDM_DRIVE"],
        "MIFs awaiting processing",
        f"{user} MIF_{mif_date()}_V38.xls",
    )
    soerf_out = os.path.join(
        os.environ["EDM_DRIVE"],
        "SOERFs awaiting processing",
        f"{user} SOERF_{mif_date()}_V12.xls",
    )

    extension_xlsx_to_xls(mif_in, mif_out)
    extension_xlsx_to_xls(soerf_in, soerf_out)
