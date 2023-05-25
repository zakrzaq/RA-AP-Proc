def single_sap_data(table: str | None, server=False):
    import time
    import pandas as pd
    import os

    from helpers.helpers import use_dotenv, ignore_warnings, use_logger, end_script
    import helpers.prompts as pr
    from state.output import output

    use_dotenv()
    use_logger()
    ignore_warnings()

    output.reset()
    if table:
        file_name = table + ".xls" if table == "sales_text" else table + ".XLSX"
        script_name = table + ".ahk"
        file = os.path.join(os.environ["DIR_IN"], file_name)
        f_materials_list = os.path.join(os.environ["DIR_OUT"], "AP materials.txt")
        f_sap = os.path.join(os.environ["DIR_APP"], "sap", "sap.ahk")
        f_script = os.path.join(os.environ["DIR_APP"], "sap", script_name)
        sleep_time = 5

        # CLEAN ALL SAP DATA IN INPUT
        if os.path.isfile(file):
            os.remove(file)

        # OPEN SAP INSTANCE
        output.add(f"{pr.info}Opening SAP Instance")
        os.system(f"{f_sap}")
        time.sleep(sleep_time)

        # READ LIST OF MATERIALS
        output.add(f"{pr.info}Loading current material list")
        material_list = pd.read_csv(f_materials_list, header=None)
        output.add(f"{pr.ok}Material in list today: {len(material_list)}")
        material_list.to_clipboard(sep="\n", index=False)

        # RUN DATA SCRIPT
        output.add(f"{pr.file}Fetching {table} data")
        os.system(f"{f_script}")
        output.add(
            f"{pr.ok}{script_name}"
            if os.path.isfile(file)
            else f"{pr.cncl}{script_name}"
        )

    return end_script(server)
