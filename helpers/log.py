import os
from openpyxl import load_workbook
import dotenv

from helpers.helpers import await_char
from state.output import output
import helpers.prompts as pr

dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def load_log():
    try:
        log_file = os.environ["AP_LOG"]
        output.add(f"{pr.done}LOG successfully loaded")
        return load_workbook(filename=log_file, keep_vba=True)
    except:
        output.add(f"{pr.cncl}LOG count not be loaded")
        return None


def save_log(log, server=True, name="TEST_output"):
    def save():
        output.add(f"{pr.file}LOG is being saved")
        log.save(os.environ["AP_LOG"])
        output.add(f"{pr.done}LOG successfully saved")

    def test_save():
        output.add(f"{pr.file}TEST LOG is being saved")
        log.save(os.path.join(os.environ["DIR_OUT"], f"{name}.xlsm"))
        output.add(f"{pr.done}TEST LOG successfully saved")

    if server:
        save()
    else:
        test_save()
        await_char("y", f"{pr.prmt}Save actual LOG file? Press Y to continue.", save())
