from ahk import AHK
from ahk.directives import NoTrayIcon
import subprocess
import time
from configs.sap import username, password, path
from state.output import output
import utils.prompts as pr

ahk = AHK(directives=[NoTrayIcon])
ahk.set_detect_hidden_windows(True)
ahk.set_title_match_mode(("RegEx", "Slow"))


def open_sap():
    try:
        output.add(f"{pr.info}Openning SAP instance")
        if ahk.win_get(title="SAP Logon Pad 750"):
            sap_logon = ahk.win_get(title="SAP Logon Pad 750")
            sap_logon.activate()  # type: ignore
        else:
            subprocess.Popen(path)
            sap_logon = ahk.win_wait(title="SAP Logon Pad 750")
            sap_logon.activate()
        if sap_logon:
            time.sleep(5)
            sap_logon.send("{Enter}")
            sap_logon.minimize()
            # time.sleep(5)
            sap = ahk.win_wait_active(title="SAP")
            sap.activate()
            ahk.type(username)
            ahk.send_input("{Tab}")
            ahk.type(password)
            ahk.send_input("{Enter}")
            win = ahk.win_wait_active(title="SAP Easy Access")
            output.add(f"{pr.conn}SAP instance running")
            return win
    except TimeoutError:
        output.add(f"{pr.cncl}failed to launch SAP!")


def get_sap():
    win = ahk.find_window(title="SAP Easy Access")
    if win:
        return win
    else:
        return open_sap()
