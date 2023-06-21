from ahk import AHK
from ahk.directives import NoTrayIcon
import time
import os

from sap.open import get_sap
from utils.helpers import use_dotenv
from utils.data_frames import get_single_sap
from state.output import output
import utils.prompts as pr

ahk = AHK(directives=[NoTrayIcon])
ahk.set_detect_hidden_windows(True)
ahk.set_title_match_mode(("RegEx", "Slow"))


def ih09(table="MARA", copy_result=False):
    use_dotenv()
    out_file = os.path.join(os.environ["DIR_IN"], f"{table}.XLSX")

    try:
        sap = get_sap()
        if sap:
            output.add(f"{pr.info}Downloading {table} from SAP")
            if os.path.exists(out_file):
                os.remove(out_file)
            sap.activate()
            ahk.send_input("/oih09 {Enter}")
            ahk.win_wait_active("Display Material: Material Selection")
            time.sleep(1)
            # paste parts
            ahk.send("{Tab}")
            ahk.send("{Tab}")
            ahk.send("{Enter}")
            ahk.win_wait_active("Multiple Selection for Material")
            ahk.send("+{F4}")
            time.sleep(1)
            ahk.send("+{F12}")
            time.sleep(3)
            ahk.send("{F8}")
            time.sleep(3)
            # execute
            ahk.send("{F8}")
            ahk.win_wait_active("Display Material: Material List")
            time.sleep(4)
            # save
            # NOTE: old save // issues
            # ahk.send("^+{F7}")
            # ahk.win_wait_active("Save As")
            # time.sleep(2)
            # ahk.send("+{tab} {tab}")
            # time.sleep(2)
            # ahk.send(f"{out_file}")
            # ahk.send("{Enter}")
            # time.sleep(2)
            #  NOTE: new save
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
            # close excel results
            excel = ahk.win_wait_active(f"{table}.XLSX - Excel")
            if ahk.win_exists(f"{table}.XLSX - Excel"):
                ahk.send("^w")
                time.sleep(1)
                excel.minimize()
            # close sap results
            sap_results = ahk.win_wait_active(f"Display Material: Material List")
            if sap_results.exist:
                sap_results.close()

            if copy_result:
                df = get_single_sap(table)
                df.to_clipboard(index=False)

            output.add(f"{pr.ok}{table} data downloaded")

    except TimeoutError:
        output.add(f"{pr.cncl}failed to launch SAP!")
