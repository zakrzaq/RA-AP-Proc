import os
from openpyxl import load_workbook
import dotenv
from state.output import output

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def load_log():
    try:
        log_file = os.environ["AP_LOG"]
        output.add("LOG successfully loaded")
        return load_workbook(filename=log_file, keep_vba=True)
    except:
        output.add("LOG count not be loaded")
        return None


def save_log(log):
    print("saving live AP LOG...")
    log.save(os.environ["AP_LOG"])
    print("AP LOG saved")


def test_save(log, name="TEST_output", server=False):
    if server == False:
        print("saving to OUTPUT folder...")
        log.save(os.path.join(os.environ["DIR_OUT"], f"{name}.xlsm"))
        print("test file saved")
