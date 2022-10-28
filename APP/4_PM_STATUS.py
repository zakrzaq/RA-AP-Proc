import os
import pandas as pd
import warnings
from datetime import date

warnings.filterwarnings("ignore")

today = date.today().strftime("%m-%d-%Y")

active = pd.read_excel('W:\AP MM Service Request Log.xlsm', sheet_name = 'Active Materials', dtype=str)
selected_active_view = active[['Date Added', 'target sorg', 'target plant', 'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'Catalog', 'Ser', 'MTART/GenItemCat', ' sorg1k dchain', ' sorg1k cs', 'sorg1k price', ' sorg4k dchain', ' sorg4k cs', 'PGC', 'target sorg price', 'target sorg dchain', 'target sorg DWERK', 'target sorg cs', 'target sorg pub', 'target plant status', 'target plant mrp type', 'DWERK Plant Status', 'DWERK Plant Code', "mif/soerf check", 'Sales Text', 'INDIA GST\nINHTS', 'INDIA GST\nmarc.stuec', 'INDIA GST taxm1', 'STATUS_CHINA_ENERGY_LBL', "Regulatory Cert\n(Z62 Class)", 'Regulatory Cert\n(Z62 Characteristic)', 'Z62 characteristic\n(assigned in SAP)', 'PCE Assessment\n(received)', 'Date of PCE review', 'MIF Submitted', 'SOERF Submitted', 'pricing request', 'PCE cert rev req\'d', 'status', 'sort order']]

#MATNRs GTS NEEDED
need_gts = ((selected_active_view['target sorg'].isin(['5008'])) & (selected_active_view['INDIA GST\nINHTS'].isna()) & (selected_active_view['INDIA GST\nmarc.stuec'].isna()) & (selected_active_view['status'].str.contains('cancel|complete|hold', case=False) == False) & (selected_active_view['status'].str.contains('GST data needed;') == False))
selected_active_view.loc[need_gts, 'status'] = selected_active_view['status'].astype(str) + "GST data needed;"

gts_requested = selected_active_view.loc[
  (selected_active_view['status'].str.contains('GST data needed;') == True)
]
print('\nMaterials needing GTS in log:')
print(len(gts_requested))

# MATNRs LOCAL NEEDED
need_local = ((selected_active_view['MTART/GenItemCat'].isin(['ZFG', 'ZTG', 'ZNFG', 'ZRS1', 'ZRS4'])) & (~selected_active_view['target plant'].isin(['5070'])) & (selected_active_view['target plant mrp type'].isin(['NA'])) & (selected_active_view['status'].str.contains('cancel|complete|hold', case=False) == False) & (selected_active_view['status'].str.contains('Localization required;') == False))
selected_active_view.loc[need_local, 'status'] = selected_active_view['status'].astype(str) + 'Localization required;'

local_requested = selected_active_view.loc[
  (selected_active_view['status'].str.contains('Localization required;') == True)
]
print('\nMaterials needing LOCALIZATION in log:')
print(len(local_requested))


# SAVE
status_file = r"C:\Users\jzakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\ap_status.txt"
status_output = selected_active_view['status']
status_output_str = ''

if os.path.exists(status_file): 
  os.remove(status_file)
for ind in status_output.index:
    status_output_str = status_output_str + str(status_output[ind]) + "\n"
with open(status_file, 'w') as file:
    file.writelines(status_output_str)