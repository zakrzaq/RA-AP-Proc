

def get_sap_data():
    import time
    import os
    import pandas as pd

    # from helpers.helpers import use_dotenv, await_char

    # use_dotenv()

    # f_materials_list = os.path.join(
    #     os.environ['DIR_DESKTOP'], 'AP materials.txt')
    # f_sap = os.path.join(os.environ['DIR_APP'], 'sap', 'sap.ahk')

    # CLEAN ALL SAP DATA IN INPUT
    sap_files = ['mara', 'marc', 'mvke', 'ausp',
                 'mlan', 'price', 'gts', 'sales_text']
    for filename in os.listdir(r'C:\RA-Apps\AP-Proc\INPUTS'):
        file = os.path.join(r'C:\RA-Apps\AP-Proc\INPUTS', filename)
        if any(x in filename for x in sap_files):
            os.remove(file)

    f_materials_list = r'C:\Users\JZakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\AP materials.txt'
    f_sap = r'C:\RA-Apps\AP-Proc\sap\sap.ahk'
    f_sales_text = r'C:\RA-Apps\AP-Proc\sap\sales_text.ahk'

    # OPEN SAP INSTANCE
    os.system(f'{f_sap}')
    time.sleep(5)

    # READ LIST OF MATERIALS
    material_list = pd.read_csv(f_materials_list, header=None)
    print(f'Material in list today: {len(material_list)}')
    material_list.to_clipboard(sep='\n', index=False)

    # RUN ALL DATA SCRIPTS
    omitted_scripts = ['sap.ahk', 'sales_text.ahk']
    scripts_List = []
    for filename in os.listdir(r'C:\RA-Apps\AP-Proc\sap'):
        if filename not in omitted_scripts:
            file = os.path.join(r'C:\RA-Apps\AP-Proc\sap', filename)
            scripts_List.append(file)

    os.system(f'{f_sales_text}')
    time.sleep(3)
    for script in scripts_List:
        print(script)
        os.system(f'{script}')
        sleep_time = 3
        time.sleep(sleep_time)


get_sap_data()
