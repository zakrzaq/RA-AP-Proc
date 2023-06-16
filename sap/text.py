from ahk import AHK
from ahk.directives import NoTrayIcon
import time
import os
from sap.open import get_sap
from helpers.helpers import use_dotenv
from state.output import output
import helpers.prompts as pr

ahk = AHK(directives=[NoTrayIcon])
# ahk.set_detect_hidden_windows(True)
# ahk.set_title_match_mode(("RegEx", "Slow"))


def text(table="SALES_TEXT"):
    use_dotenv()
    out_file = os.path.join(os.environ["DIR_IN"], f"{table}.XLSX")

    try:
        sap = get_sap()
        if sap:
            output.add(f"{pr.info}Downloading {table} from SAP")
            if os.path.exists(out_file):
                os.remove(out_file)
            sap.activate()
            ahk.send_input("/oZ_COM_SALETXT_LD_EXT {Enter}")
            ahk.win_wait_active("Material Sales Text Load/Extract")
            time.sleep(1)
            # select variant
            ahk.send("+{F5}")
            ahk.win_wait_active("Find Variant")
            time.sleep(1)
            ahk.send("{F8}")
            time.sleep(1)
            # paste parts
            ahk.send("{Tab}")
            ahk.send("{Tab}")
            ahk.send("{Tab}")
            ahk.send("{Tab}")
            ahk.send("{Tab}")
            ahk.send("{Enter}")
            ahk.win_wait_active("Multiple Selection for Material Number")
            time.sleep(1)
            ahk.send("+{F12}")
            time.sleep(3)
            ahk.send("{F8}")
            time.sleep(3)
            # execute
            ahk.send("{F8}")

            output.add(f"{pr.ok}{table} data download in progress")

    except TimeoutError:
        output.add(f"{pr.cncl}failed to launch SAP!")
