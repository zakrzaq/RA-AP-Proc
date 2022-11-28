import warnings
from openpyxl import load_workbook
import pandas as pd
import os
import keyboard
from helpers import populate_sheet_series
import dotenv
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)
warnings.filterwarnings("ignore")

active = pd.read_excel(os.environ['AP_LOG'],
                       sheet_name='Active Materials', dtype=str)
print(active.tail(2))

# VIEW LIKE ACTIVE SHEET IN EXCEL
selected_active_view = active[['Date Added', 'target sorg', 'target plant', 'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'Catalog', 'Ser', 'MTART/GenItemCat', ' sorg1k dchain', ' sorg1k cs', 'sorg1k price', ' sorg4k dchain', ' sorg4k cs', 'PGC', 'target sorg price', 'target sorg dchain', 'target sorg DWERK', 'target sorg cs', 'target sorg pub', 'target plant status',
                               'target plant mrp type', 'DWERK Plant Status', 'DWERK Plant Code', "mif/soerf check", 'Sales Text', 'INDIA GST\nINHTS', 'INDIA GST\nmarc.stuec', 'INDIA GST taxm1', 'STATUS_CHINA_ENERGY_LBL', "Regulatory Cert\n(Z62 Class)", 'Regulatory Cert\n(Z62 Characteristic)', 'Z62 characteristic\n(assigned in SAP)', 'PCE Assessment\n(received)', 'Date of PCE review', 'MIF Submitted', 'SOERF Submitted', 'pricing request', 'PCE cert rev req\'d', 'status', 'sort order']]

# MIF / SOERF needed
mif_soerf_view = active[['Date Added', 'target sorg', 'target plant',
                         'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'status']]

mif_soerf = mif_soerf_view.loc[
    ((selected_active_view['status'].str.contains('cancel|complete', case=False) == False) | selected_active_view['status'].isna()) &
    (selected_active_view["Service Requested\n(from request form)"].isin(['Plant and sales org extension', 'Plant extension', 'Sales org extension'])) &
    (selected_active_view["mif/soerf check"].isin(['X'])) &
    (selected_active_view['MTART/GenItemCat'].isin(['ZTG', 'ZFG']))
]

mif_soerf['sql'] = 'insert into AP_MM_SERVICE values(\'' + mif_soerf['target sorg'] + '\', \'' + mif_soerf['target plant'] + '\', \'' + mif_soerf['email prefix\n(from request form)'] + \
    '\', \'' + mif_soerf['SAP MATNR\n(from request form)'] + '\', \'' + \
    mif_soerf["Service Requested\n(from request form)"] + '\');'


# OUTPUT TO SQL FILE
output = mif_soerf['sql']
output_str = ""
for ind in output.index:
    output_str = output_str + output[ind] + "\n"

# print(output_str)
# TODO: MOVE THIS TO .ENV
with open(r"C:\Users\JZakrzewski\dev\RA-SCRIPTS\SQL\AP PROC\COMBINED MIF SOERF AP 11-08-2021 JZ.sql") as file:
    lines = file.readlines()
    lines[5] = output_str
with open(os.path.join(os.environ['HOME_DIR'], 'AP_MIF_SOERF.sql'), 'w') as file:
    file.writelines(lines)

print('Materials added to SQL query:')
print(len(mif_soerf))


# AM RUN STATUSES:
print('Press Y to generate AM material status updates')
while True:
    if keyboard.is_pressed("y"):
        # LOAD LOG
        # log_file = os.environ['AP_LOG']
        log_file = r'C:\Users\JZakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\New AP Process\RESOURCES\AP_LOG_TEST.xlsm'
        log = load_workbook(filename=log_file, keep_vba=True)
        ws_active = log['Active Materials']

        # MATNRs PRICE NEEDED
        need_price = (selected_active_view['target sorg price'].isna()) & (~selected_active_view['SOERF Submitted'].isna()) & (
            (selected_active_view['status'].str.contains('cancel|complete|on hold|needs price;', case=False) == False) | (selected_active_view['status'].isnull()))

        selected_active_view.loc[need_price, 'status'] = selected_active_view['status'].astype(
            str) + "needs price;"

        price_requested = selected_active_view.loc[
            (selected_active_view['status'].str.contains(
                'needs price;') == True)
        ]
        print('\nMaterials NEEDING PRICE in AP LOG: {}'.format(len(price_requested)))

        # MATNRs PCE NEEDED
        need_pce = (
            ((selected_active_view['status'].str.contains('cancel|complete', case=False) == False)) &
            ((selected_active_view['status'].str.contains('pending PCE review;') == False)) &
            (selected_active_view['Service Requested\n(from request form)']
             == 'Product Certification Review')
        ) | (
            (selected_active_view['MTART/GenItemCat'].isin(['ZFG', 'ZTG'])) &
            (~selected_active_view['Regulatory Cert\n(Z62 Characteristic)'].isna()) &
            (selected_active_view['Z62 characteristic\n(assigned in SAP)'].isna()) &
            ((selected_active_view['status'].str.contains('cancel|complete|on hold|pending PCE review;', case=False) == False)) &
            ((selected_active_view['status'].str.contains('pending PCE review;') == False)))

        selected_active_view.loc[need_pce, 'status'] = selected_active_view['status'].astype(
            str) + 'pending PCE review;'

        pce_requested = selected_active_view.loc[
            (selected_active_view['status'].str.contains(
                'pending PCE review;') == True)
        ]
        print('\nMaterials needing PCE in log: {}'.format(len(pce_requested)))

        # save statuses
        status_file = os.path.join(os.environ['HOME_DIR'], 'AP status.txt')
        status_output = selected_active_view['status']
        status_output_str = ''

        if os.path.exists(status_file):
            os.remove(status_file)
        for ind in status_output.index:
            if type(status_output[ind]) == float:
                status_output_str = status_output_str + "" + "\n"
            else:
                status_output_str = status_output_str + \
                    str(status_output[ind]) + "\n"
        with open(status_file, 'w') as file:
            file.writelines(status_output_str)

        print('Press Y to save status updates to AP LOG')
        while True:
            if keyboard.is_pressed("y"):
                # INTERATE OVER STATUS LIENS AND UPDATE IN AP LOG
                populate_sheet_series(status_output, ws_active, 50, 2)
                log.save(os.path.join(
                    os.environ['TMP_OUT_DIR'], 'test_am_status.xlsm'))
                break

        break
