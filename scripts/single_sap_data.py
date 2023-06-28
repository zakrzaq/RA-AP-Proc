import pandas as pd, os, time

from utils.helpers import use_dotenv, ignore_warnings, use_logger, end_script
import utils.prompts as pr
from state.output import output
from state.time import timer
from sap import ih09, se16, gts, sqvi, text, open


def single_sap_data(table: str | None, server=False, method='GET'):
    timer.start()
    use_dotenv()
    use_logger()
    ignore_warnings()
    output.reset()

    # READ LIST OF MATERIALS
    f_materials_list = os.path.join(os.environ["DIR_OUT"], "AP materials.txt")
    output.add(f"{pr.info}Loading current material list")
    material_list = pd.read_csv(f_materials_list, header=None)
    output.add(f"{pr.info}Material in list today: {len(material_list)}")
    material_list.to_clipboard(sep="\n", index=False)

    if table:
        open.get_sap()
        time.sleep(3)

        match table:
            case "mara":
                ih09.ih09("MARA", copy_result=True)
            case "marc":
                se16.se16("MARC", copy_result=True)
            case "mvke":
                se16.se16("MVKE", copy_result=True)
            case "ausp":
                se16.se16("AUSP", copy_result=True)
            case "mlan":
                se16.se16("MLAN", copy_result=True)
            case "gts":
                gts.gts("GTS", copy_result=True)
            case "price":
                sqvi.sqvi(copy_result=True)
            case "text":
                text.text()
            case _:
                output.add(
                    f"{pr.cncl}Wrong table name provided: mara | marc | mvke | ausp | mlan | gts | price | text"
                )

    timer.stop()
    output.add(f"{pr.ok}Script completed: {timer.get_elapsed_time()}")
    return end_script(server, method)
