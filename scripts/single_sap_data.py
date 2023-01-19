def single_sap_data(table: str, server=False):
    import time
    import pandas as pd
    import os
    from markupsafe import Markup

    from helpers.helpers import use_dotenv, ignore_warnings, use_logger, output_msg
    from helpers.helpers import await_char

    use_dotenv()
    use_logger()
    ignore_warnings()

    output = ""
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
    os.system(f"{f_sap}")
    time.sleep(sleep_time)

    # READ LIST OF MATERIALS
    material_list = pd.read_csv(f_materials_list, header=None)
    output += output_msg(f"Material in list today: {len(material_list)}")
    material_list.to_clipboard(sep="\n", index=False)

    # RUN DATA SCRIPT
    output += output_msg(f"Fetching {table} data")
    os.system(f"{f_script}")
    output += output_msg(f"{script_name} data file exists: {os.path.isfile(file)}")

    if server:
        return Markup(output)
    else:
        await_char("y", f"SAP {script_name} data downloaded, press Y to continue")
