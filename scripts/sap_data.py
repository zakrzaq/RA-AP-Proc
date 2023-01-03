

def get_sap_data(server=False):
    import time
    import pandas as pd
    import os
    from flask import Markup

    from helpers.helpers import await_char, use_dotenv, ignore_warnings, use_logger, output_msg

    use_dotenv()
    use_logger()
    ignore_warnings()

    output = ''

    # from helpers.helpers import use_dotenv, await_char

    # use_dotenv()

    # f_materials_list = os.path.join(
    #     os.environ['DIR_DESKTOP'], 'AP materials.txt')
    # f_sap = os.path.join(os.environ['DIR_APP'], 'sap', 'sap.ahk')

    # CLEAN ALL SAP DATA IN INPUT
    sap_files = ['mara', 'marc', 'mvke', 'ausp',
                 'mlan', 'price', 'gts', 'sales_text']
    for filename in os.listdir(os.environ['DIR_IN']):
        file = os.path.join(os.environ['DIR_IN'], filename)
        if any(x in filename for x in sap_files):
            os.remove(file)

    f_materials_list = os.path.join(
        os.environ['DIR_DESKTOP'], 'AP materials.txt')
    f_sap = os.path.join(os.environ['DIR_APP'], 'sap', 'sap.ahk')
    f_sales_text = os.path.join(os.environ['DIR_APP'], 'sap', 'sales_text.ahk')

    # OPEN SAP INSTANCE
    os.system(f'{f_sap}')
    time.sleep(5)

    # READ LIST OF MATERIALS
    material_list = pd.read_csv(f_materials_list, header=None)
    output += output_msg(server,
                         f'Material in list today: {len(material_list)}')
    material_list.to_clipboard(sep='\n', index=False)

    # RUN ALL DATA SCRIPTS
    omitted_scripts = ['sap.ahk', 'sales_text.ahk',
                       'org_source.ahk', 'upd_class.ahk']
    scripts_List = []
    for filename in os.listdir(os.path.join(os.environ['DIR_APP'], 'sap')):
        if filename not in omitted_scripts:
            file = os.path.join(os.environ['DIR_APP'], 'sap', filename)
            scripts_List.append(file)

    sleep_time = 4
    os.system(f'{f_sales_text}')
    time.sleep(sleep_time)
    for script in scripts_List:
        output += output_msg(server, script)
        os.system(f'{script}')
        time.sleep(sleep_time)
