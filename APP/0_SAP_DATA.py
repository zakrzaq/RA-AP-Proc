### LIBS

import warnings
import pandas as pd
from openpyxl import load_workbook
from openpyxl.formula.translate import Translator

warnings.filterwarnings("ignore")

### VARIABLES

### OPEN LOG FILE NAD GENERATE SHEETS VARIABLES

# ACTUAL
log_file = 'W:\\AP MM Service Request Log.xlsm'
# TESTING
# log_file = 'W:\\AP MM Service Request Log_CLEANOUT.xlsm'
# log_file = 'W:\\AP MM Service Request Log_TESTING.xlsm'
# log_file = "W:\\VBA.xlsm"

log = load_workbook(filename=log_file, keep_vba=True)

ws_active=log['Active Materials']
ws_mara=log['mara']
ws_marc=log['marc']
ws_mvke=log['mvke']
ws_ausp=log['ausp']
ws_mlan=log['mlan']
ws_price=log['ZZ_MATPRC_HIST']
ws_gts=log['gts']
ws_text=log['sales text']
ws_list = [ws_mara, ws_marc, ws_mvke, ws_ausp, ws_mlan, ws_price, ws_gts, ws_text]

# # clean out data
for sheet in ws_list:
  sheet.delete_rows(100, ws_mara.max_row)

# load sap data to df
# mara = pd.read_excel(r'W:\ap_data\mara.XLSX')
# marc = pd.read_excel(r'W:\ap_data\marc.XLSX')
# mvke = pd.read_excel(r'W:\ap_data\mvke.XLSX')
# ausp = pd.read_excel(r'W:\ap_data\ausp.XLSX')
# mlan = pd.read_excel(r'W:\ap_data\mlan.XLSX')
# price = pd.read_excel(r'W:\ap_data\price.XLSX')
# gts = pd.read_excel(r'W:\ap_data\gts.XLSX')
# text = pd.read_excel(r'W:\ap_data\sales_text.xlsx')
# inputs_list = [mara, marc, mvke, ausp, mlan, price, gts, text]


# # output df to log
# def populate_sheet(df, sheet):
#   df = df.fillna('')
#   output = []

#   for index, row in df.iterrows():
#     output.append(row.values.tolist())

#   for rowy, row in enumerate(output, start = 2):
#     for colx, value in enumerate(row, start = 2):
#       sheet.cell(column = colx, row = rowy, value = value)

# populate_sheet(mara, ws_mara)
# populate_sheet(marc, ws_marc)
# populate_sheet(mvke, ws_mvke)
# populate_sheet(ausp, ws_ausp)
# populate_sheet(mlan, ws_mlan)
# populate_sheet(price, ws_price)
# populate_sheet(gts, ws_gts)
# populate_sheet(text, ws_text)


# # EXTEND CONCATS
# def extend_concats(sheet):
#   last_row = sheet.max_row
#   i = 100
#   while i < last_row:
#     i += 1
#     formula = sheet['A2'].value
#     sheet['A{}'.format(i)] = Translator(formula, origin="A2").translate_formula("A{}".format(i))

# for sheet in ws_list:
#   extend_concats(sheet)

# # save test
# # log.save(r'..\OUTPUTS\clean_data.xlsm')
# log.save(log_file)