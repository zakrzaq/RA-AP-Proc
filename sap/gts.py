from ahk import AHK
from ahk.directives import NoTrayIcon
import time
import os
from sap.open import get_sap
from helpers.helpers import use_dotenv
from helpers.data_frames import get_single_sap
from state.output import output
import helpers.prompts as pr

ahk = AHK(directives=[NoTrayIcon])
ahk.set_detect_hidden_windows(True)
ahk.set_title_match_mode(("RegEx", "Slow"))


def gts(table="GTS", copy_result=False):
    use_dotenv()
    out_file = os.path.join(os.environ["DIR_IN"], f"{table}.XLSX")

    try:
        sap = get_sap()
        output.add(f"{pr.conn}Connected to SAP")
        if sap:
            output.add(f"Downloading {table} from SAP")
            if os.path.exists(out_file):
                os.remove(out_file)
            sap.activate()
            ahk.send_input("/oZ_SLO_EXPIMP_CLSSFCT {Enter}")
            ahk.win_wait_active("Export / Import Classification Report")
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
            ahk.send("{Enter}")
            ahk.win_wait_active("Multiple Selection for Part Number")
            time.sleep(1)
            ahk.send("+{F12}")
            time.sleep(3)
            ahk.send("{F8}")
            time.sleep(3)
            # execute
            ahk.send("{F8}")
            ahk.win_wait_active("Export / Import Classification Report")
            time.sleep(5)
            # save
            ahk.send("+{F10}")
            time.sleep(1)
            ahk.send("{up}")
            time.sleep(1)
            ahk.send("{Enter}")
            time.sleep(1)
            ahk.send("{Enter}")
            ahk.win_wait_active("Save As")
            time.sleep(2)
            ahk.send("+{tab} {tab}")
            time.sleep(2)
            ahk.send(f"{out_file}")
            ahk.send("{Enter}")
            time.sleep(2)
            # OLD
            # ahk.send("^{F2}")
            # time.sleep(2)
            # ahk.send("+{tab} {tab}")
            # time.sleep(2)
            # ahk.send(f"{out_file}")
            # ahk.send("{Enter}")
            time.sleep(2)
            # close excel results
            excel = ahk.win_wait_active(f"{table}.XLSX - Excel")
            if ahk.win_exists(f"{table}.XLSX - Excel"):
                ahk.send("^w")
                excel.minimize()
            # close sap results
            gts_results = ahk.win_wait_active("Export / Import Classification Report")
            if gts_results.exist:
                gts_results.close()

            if copy_result:
                df = get_single_sap(table)
                df.to_clipboard(index=False)

            output.add(f"{pr.ok}{table} data downloaded")

    except TimeoutError:
        output.add("failed to launch SAP!")

