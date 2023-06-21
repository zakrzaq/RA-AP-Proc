def single_sap_data(table: str | None, server=False):
    import time, pandas as pd, os
    start = time.time()

    from utils.helpers import use_dotenv, ignore_warnings, use_logger, end_script
    import utils.prompts as pr
    from state.output import output
    from sap import ih09, se16, gts, sqvi, text, open

    use_dotenv()
    use_logger()
    ignore_warnings()
    output.reset()

    f_materials_list = os.path.join(os.environ["DIR_OUT"], "AP materials.txt")

    # READ LIST OF MATERIALS
    output.add(f"{pr.info}Loading current material list")
    material_list = pd.read_csv(f_materials_list, header=None)
    output.add(f"{pr.info}Material in list today: {len(material_list)}")
    material_list.to_clipboard(sep="\n", index=False)

    if table:
        open.get_sap()
        time.sleep(3)

        match table:
            case "mara":
                ih09.ih09("MARA", True)
            case "marc":
                se16.se16("MARC", True)
            case "mvke":
                se16.se16("MVKE", True)
            case "ausp":
                se16.se16("AUSP", True)
            case "mlan":
                se16.se16("MLAN", True)
            case "gts":
                gts.gts("GTS", True)
            case "price":
                sqvi.sqvi(copy_result=True)
            case "text":
                text.text()
            case _:
                output.add(
                    f"{pr.cncl}Wrong table name provided: mara | marc | mvke | ausp | mlan | gts | price | text"
                )

    end = time.time()
    output.add(f"{pr.ok}Script completed: {round(end - start, 2)}")
    return end_script(server)
