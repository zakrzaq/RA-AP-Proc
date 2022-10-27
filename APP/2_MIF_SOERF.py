import pandas as pd
import warnings
warnings.filterwarnings("ignore")

active = pd.read_excel('W:\AP MM Service Request Log.xlsm', sheet_name = 'Active Materials', dtype=str)
# active.tail(2)

# VIEW LIKE ACTIVE SHEET IN EXCEL
selected_active_view = active[['Date Added', 'target sorg', 'target plant', 'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'Catalog', 'Ser', 'MTART/GenItemCat', ' sorg1k dchain', ' sorg1k cs', 'sorg1k price', ' sorg4k dchain', ' sorg4k cs', 'PGC', 'target sorg price', 'target sorg dchain', 'target sorg DWERK', 'target sorg cs', 'target sorg pub', 'target plant status', 'target plant mrp type', 'DWERK Plant Status', 'DWERK Plant Code', "mif/soerf check", 'Sales Text', 'INDIA GST\nINHTS', 'INDIA GST\nmarc.stuec', 'INDIA GST taxm1', 'STATUS_CHINA_ENERGY_LBL', "Regulatory Cert\n(Z62 Class)", 'Regulatory Cert\n(Z62 Characteristic)', 'Z62 characteristic\n(assigned in SAP)', 'PCE Assessment\n(received)', 'Date of PCE review', 'MIF Submitted', 'SOERF Submitted', 'pricing request', 'PCE cert rev req\'d', 'status', 'sort order']]

# MIF / SOERF needed
mif_soerf_view = active[['Date Added', 'target sorg', 'target plant',  'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'status']]

mif_soerf = mif_soerf_view.loc[
  ((selected_active_view['status'].str.contains('cancel|complete', case=False) == False) | selected_active_view['status'].isna()) &
  (selected_active_view["Service Requested\n(from request form)"].isin(['Plant and sales org extension', 'Plant extension', 'Sales org extension'])) & 
  (selected_active_view["mif/soerf check"].isin(['X'])) &
  (selected_active_view['MTART/GenItemCat'].isin(['ZTG', 'ZFG']))
]

mif_soerf['sql'] = 'insert into AP_MM_SERVICE values(\'' + mif_soerf['target sorg'] + '\', \'' + mif_soerf['target plant'] + '\', \'' + mif_soerf['email prefix\n(from request form)'] + '\', \'' + mif_soerf['SAP MATNR\n(from request form)'] + '\', \'' + mif_soerf["Service Requested\n(from request form)"] + '\');'


# OUTPUT TO SQL FILE
output = mif_soerf['sql']

output_str = ""

for ind in output.index:
    output_str = output_str + output[ind] + "\n"

# print(output_str)
with open(r"C:\Users\jzakrzewski\Documents\dev\RA-SCRIPTS\SQL\AP PROC\COMBINED MIF SOERF AP 11-08-2021 JZ.sql") as file:
    lines = file.readlines()
    lines[5] = output_str
with open(r"C:\Users\jzakrzewski\Documents\dev\RA-SCRIPTS\SQL\AP PROC\AP_MIF_SEORF_QUERY.sql", 'w') as file:
    file.writelines(lines)
    
print('Materials added to SQL query:')
print(len(mif_soerf))