import os, pandas as pd, time

from utils.helpers import use_dotenv, ignore_warnings, use_logger, end_script
from utils.datetime import today_ymd, today_dmy
from utils.data_frames import get_active
from utils.workbook import (
    populate_sap_data_sheet,
)
import utils.prompts as pr
from state.output import output
from state.log import log
from state.time import timer

def reconcile_pce(server=False):
    timer.start()
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

    # ORIGINAL SOURCE
    output.add(f"{pr.info}Processing ORG SOURCE")
    mifs = get_active("mif")
    if not mifs.empty:
        mifs["date"] = mifs["date"].map(lambda x: str(x)[:-9])
        mifs_today = mifs[mifs["date"] == today]
        mifs_list = mifs_today["MATERIAL"]
        mifs_list.to_clipboard(sep=",", index=False, header=None)
        os.system(f"{f_sap}")
        time.sleep(7)
        output.add(f"{pr.info}Running ORG Source AHK")
        os.system(f"{f_org_source}")
        output.add(f"{pr.done}Finished ORG Source")

    # FIND PCE REQUEST
    output.add(f"{pr.info}PCE Reconciliation")
    pce_feedback = pd.DataFrame()
    for filename in os.listdir(r"C:\RA-Apps\AP-Proc\INPUTS"):
        file = os.path.join(r"C:\RA-Apps\AP-Proc\INPUTS", filename)
        if " ASSESSMENT REQUEST" in filename:
            output.add(f"{pr.file}{filename}")
            df = pd.read_excel(file)
            pce_feedback = pd.concat([pce_feedback, df])
    output.add(f"{pr.done}Found {pce_feedback.shape[0]} materials to reconcile")

    # PCE FEEDBACK TO LOG
    log.load()
    if (pce_feedback.shape[0] > 0) and log:
        output.add(f"{pr.info}Processing PCE Reconciliation")
        ws_pce = log.ws_pce
        ws_archived_pce = log.ws_pce_arch
        last_row = ws_pce.max_row + 1

        # reconciled parts
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

        # new combined list
        log_pce_df = get_active("pce")
        columns = list(log_pce_df.columns)
        for_log.columns = columns
        for_log = for_log.drop_duplicates(subset=["concat"], keep="last")
        updated_pce_df = pd.concat([log_pce_df, for_log])
        updated_pce_df.reset_index()
        duplicated_df = updated_pce_df.loc[
            updated_pce_df.duplicated(subset=["concat"], keep="last")
        ]
        output.add(f"{pr.info}Assessments to archive: {duplicated_df.shape[0]}")
        updated_pce_df = updated_pce_df.drop_duplicates(subset=["concat"], keep="last")

        populate_sap_data_sheet(updated_pce_df, ws_pce, 1, 2)
        last_row = ws_archived_pce.max_row + 1
        populate_sap_data_sheet(
            duplicated_df,
            ws_archived_pce,
            1,
            last_row,
        )

        # TODO: fix date format to excel
        # SAVE
        log.save()
        # log.save(os.path.join(os.environ["DIR_OUT"], "TEST_new_PCE.xlsm"))
        # PCE FEEDBACK TO SAP
        output.add(f"{pr.info}Z62 updates in SAP")
        if pce_feedback.empty:
            output.add(f"{pr.cncl}No PCE feedback to process")
        else:
            output.add(f"{pr.info}Preparing PCE SAP Update")
        for_upd = pce_feedback.iloc[:, [4, 12, 13, 18]]
        # for_upd = for_log[for_log["new PCE assessment"].notna()]
        for_upd["SAP Table"] = "MARA"
        for_upd["Class"] = "Z62"
        for_upd["Blank 1"] = ""
        for_upd["Blank 2"] = ""
        for_upd = for_upd[
            [
                "SAP Table",
                "SAP MATNR\n(from request form)",
                "Class",
                "Regulatory Cert\n(Z62 Class)",
                "Blank 1",
                "Blank 2",
                "Regulatory Cert\n(Z62 Characteristic)",
                "new PCE assessment",
            ]
        ]
        for_upd.to_csv(upd_file, header=False, index=False, sep="\t")
        output.add(f"{pr.info}Processing PCE SAP Update for {for_upd.shape[0]} parts")
        os.system(f"{f_sap}")
        time.sleep(7)
        os.system(f"{f_upd_class}")
        output.add(f"{pr.done}Finished PCE Z62 SAP Update")
    else:
        output.add(
            f"{pr.cncl}Unable to load the LOG to update PCE or no materials to reconcile"
        )

    timer.stop()
    output.add(f"{pr.ok}Script completed: {timer.get_elapsed_time()}")
    return end_script(server)
