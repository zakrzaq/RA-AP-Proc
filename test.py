import os
import pandas as pd
import time

from helpers.helpers import use_dotenv, ignore_warnings, use_logger, end_script
from helpers.datetime import today_ymd, today_dmy
from helpers.log import save_log, load_log
from helpers.data_frames import get_active
from helpers.xlsm import populate_sap_data_sheet, extend_concats, get_first_empty_row
import helpers.prompts as pr
from state.output import output

use_dotenv()
use_logger()
ignore_warnings()

today = today_ymd("-")
ws_today = today_dmy()
f_sap = os.path.join(os.environ["DIR_APP"], "sap", "sap.ahk")
f_org_source = os.path.join(os.environ["DIR_APP"], "sap", "org_source.ahk")
f_upd_class = os.path.join(os.environ["DIR_APP"], "sap", "upd_class.ahk")
upd_file = os.path.join(os.environ["DIR_OUT"], "UPDATES TO Z62.txt")
output.reset()


output.add(f"{pr.info}PCE Reconciliation")
pce_feedback = pd.DataFrame()
for filename in os.listdir("C:\RA-Apps\AP-Proc\INPUTS"):
    file = os.path.join("C:\RA-Apps\AP-Proc\INPUTS", filename)
    if " ASSESSMENT REQUEST" in filename:
        output.add(f"{pr.file}{filename}")
        df = pd.read_excel(file)
        pce_feedback = pd.concat([pce_feedback, df])
output.add(f"{pr.done}Found {pce_feedback.shape[0]} materials to reconcile")

# PCE FEEDBACK TO LOG
log = load_log()
ws_archived_pce = log["archived PCE"]

output.add(f"{pr.info}Processing PCE Reconciliation")
ws_pce = log["pce"]
last_row = ws_archived_pce.max_row + 1
print(last_row)

for_log = pce_feedback.iloc[:, [4, 12, 13, 18]]
for_log = for_log[for_log["new PCE assessment"].notna()]
for_log.insert(
    0,
    "concat",
    for_log["Regulatory Cert\n(Z62 Characteristic)"]
    + for_log["SAP MATNR\n(from request form)"],
)
for_log["date"] = ws_today
for_log["assesor"] = None
for_log = pd.DataFrame(for_log)
print(for_log.shape)

log_pce_df = get_active("pce")
columns = list(log_pce_df.columns)
print(columns)
print(log_pce_df.shape)
for_log.columns = columns
for_log = for_log.drop_duplicates(subset=["concat"], keep="last")
updated_pce_df = pd.concat([log_pce_df, for_log])
updated_pce_df.reset_index()
print(updated_pce_df.shape)
dupplicated_df = updated_pce_df.loc[
    updated_pce_df.duplicated(subset=["concat"], keep="last")
]
updated_pce_df = updated_pce_df.drop_duplicates(subset=["concat"], keep="last")
print(dupplicated_df.shape)


# updated_pce_df.to_excel(os.path.join(os.environ["DIR_OUT"], "TEST_PCE_reconcile.xlsx"))
# dupplicated_df.to_excel(os.path.join(os.environ["DIR_OUT"], "TEST_PCE_removed.xlsx"))
