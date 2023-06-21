from ahk import AHK
from ahk.directives import NoTrayIcon
import time
import os

from sap.open import get_sap
from utils.helpers import use_dotenv
from state.output import output
import utils.prompts as pr

ahk = AHK(directives=[NoTrayIcon])
ahk.set_detect_hidden_windows(True)
ahk.set_title_match_mode(("RegEx", "Slow"))

from utils.helpers import use_dotenv

use_dotenv()

def sqvi(table="PRICE", transaction="LIST_PRICE", copy_result=False):
    use_dotenv()
    out_file = os.path.join(os.environ["DIR_IN"], f"{table}.XLSX")

    try:
        get_sap()
        sap = ahk.win_wait("SAP Easy Access")
        sap.activate()
        if sap:
            output.add(f"{pr.info}Downloading {table} from SAP")
            if os.path.exists(out_file):
                os.remove(out_file)
            sap.activate()
            ahk.send_input("/osqvi {Enter}")
            ahk.win_wait_active("QuickViewer: Initial Screen")
            time.sleep(2)
            ahk.send_input(f"{transaction}")
            ahk.send_input("{F8}")
            ahk.win_wait_active("AP_LIST_PRICE")
            time.sleep(1)
            # select variant
            ahk.send("+{F5}")
            ahk.win_wait_active("ABAP: Variant Directory of Program")
            time.sleep(1)
            ahk.send("{down}")
            time.sleep(1)
            ahk.send("{up}")
            time.sleep(1)
            ahk.send("{F2}")
            time.sleep(1)
            # paste parts
            ahk.send("{Tab}")
            ahk.send("{Tab}")
            ahk.send("{Enter}")
            ahk.win_wait_active(f"Multiple Selection for Material Number")
            time.sleep(1)
            ahk.send("+{F12}")
            time.sleep(3)
            ahk.send("{F8}")
            time.sleep(3)
            # execute
            ahk.send("{F8}")
            ahk.win_wait_active("AP_LIST_PRICE")
            time.sleep(5)
            # save
    except:
        print('tits up')

sqvi()

