from ahk import AHK
from ahk.directives import NoTrayIcon
import subprocess
import time
from configs.sap import username, password, path
from state.output import output
import helpers.prompts as pr

ahk = AHK(directives=[NoTrayIcon])
ahk.set_detect_hidden_windows(True)
ahk.set_title_match_mode(("RegEx", "Slow"))


def open_sap():
    try:
        output.add(f"{pr.info}Openning SAP instance")
        subprocess.Popen(path)
        sap_logon = ahk.win_wait_active(title="SAP Logon Pad 750")
        time.sleep(5)
        sap_logon.send("{Enter}")
        sap_logon.minimize()
        # time.sleep(5)
        sap = ahk.win_wait_active(title="SAP")
        ahk.type(username)
        ahk.send_input("{Tab}")
        ahk.type(password)
        ahk.send_input("{Enter}")
        output.add(f"{pr.conn}SAP instance running")
    except TimeoutError:
        output.add(f"{pr.cncl}failed to launch SAP!")


def get_sap():
    win = ahk.find_window(title="SAP Easy Access")
    if win:
        return win
    else:
        open_sap()
