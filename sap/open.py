from ahk import AHK
from ahk.directives import NoTrayIcon
import subprocess
import time
from configs.sap import username, password, path

ahk = AHK(directives=[NoTrayIcon])
# ahk.set_detect_hidden_windows(True)
# ahk.set_title_match_mode(("RegEx", "Slow"))


def open_sap():
    try:
        subprocess.Popen(path)
        sap_logon = ahk.win_wait_active(title="SAP Logon Pad 750")
        time.sleep(5)
        sap_logon.send("{Enter}")
        sap_logon.minimize()
        # time.sleep(5)
        sap = ahk.win_wait_active(title="SAP")
        print(sap)
        ahk.type(username)
        ahk.send_input("{Tab}")
        ahk.type(password)
        ahk.send_input("{Enter}")
    except TimeoutError:
        print("failed to launch SAP!")
