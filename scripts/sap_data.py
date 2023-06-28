import time, pandas as pd, os

start = time.time()

from utils.helpers import (
    use_dotenv,
    ignore_warnings,
    use_logger,
    end_script,
)
import utils.prompts as pr
from state.output import output
from state.time import timer
from sap import ih09, se16, gts, sqvi, text, open


def get_sap_data(server=False, method='GET', mode="all"):
    timer.start()
    use_dotenv()
    use_logger()
    ignore_warnings()
    output.reset()

    f_materials_list = os.path.join(os.environ["DIR_OUT"], "AP materials.txt")

    open.get_sap()
    time.sleep(3)

    # READ LIST OF MATERIALS
    material_list = pd.read_csv(f_materials_list, header=None)
    output.add(f"{pr.info}Material in list today: {len(material_list)}")
    material_list.to_clipboard(sep="\n", index=False)

    # RUN ALL DATA SCRIPTS
    output.add(f"{pr.info}Download {mode} SAP data")
    if mode == "all":
        text.text()
        ih09.ih09()
        tables = ["MARC", "MVKE", "AUSP", "MLAN"]
        for t in tables:
            se16.se16(t)
        sqvi.sqvi()
        gts.gts()
    elif mode == "refresh":
        text.text()
        se16.se16("MARC")
        se16.se16("MVKE")
        se16.se16("AUSP")

    timer.stop()
    output.add(f"{pr.ok}Script completed: {timer.get_elapsed_time()}")
    return end_script(server, method)
