def reconcile_pce(server=False):
    import os
    import pandas as pd
    import time

    from helpers.helpers import use_dotenv, ignore_warnings, use_logger, end_script
    from helpers.datetime import today_ymd, today_dmy
    from helpers.log import save_log, load_log
    from helpers.data_frames import get_active
    from helpers.xlsm import populate_sap_data_sheet, extend_concats
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
    for filename in os.listdir("C:\RA-Apps\AP-Proc\INPUTS"):
        file = os.path.join("C:\RA-Apps\AP-Proc\INPUTS", filename)
        if " ASSESSMENT REQUEST" in filename:
            output.add("\t" + file)
            df = pd.read_excel(file)
            pce_feedback = pd.concat([pce_feedback, df])
    output.add(f"{pr.done}Found {pce_feedback.shape[0]} materials to reconcile")

    # PCE FEEDBACK TO LOG
    log = load_log()
    if (pce_feedback.shape[0] > 0) and log:
        output.add("Processing PCE Reconciliation")
        ws_pce = log["pce"]
        last_row = ws_pce.max_row + 1

        for_log = pce_feedback.iloc[:, [4, 12, 13, 18]]
        for_log = for_log[for_log["new PCE assessment"].notna()]

        populate_sap_data_sheet(for_log, ws_pce, 2, last_row)
        # insert dates
        # TODO: fix date format to excel
        new_last = ws_pce.max_row
        for i in range(last_row, new_last + 1, 1):
            ws_pce[f"F{i}"].value = ws_today
        # CONCAT
        extend_concats(ws_pce, last_row - 1, "A")
        # SAVE
        save_log(log)
    else:
        output.add(
            f"{pr.cncl}Unable to load the LOG to update PCE or no materials to reconcile"
        )

    # PCE FEEDBACK TO SAP
    output.add(f"{pr.info}Z62 updates in SAP")
    if pce_feedback.empty:
        output.add(f"{pr.cncl}No PCE feedback to process")
    else:
        output.add(f"{pr.info}Preparing PCE SAP Update")
        for_upd = pce_feedback.iloc[:, [4, 12, 13, 18]]
        for_upd = for_log[for_log["new PCE assessment"].notna()]
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
        for_upd.to_csv(upd_file, header=None, index=False, sep="\t")
        output.add(f"Processing PCE SAP Update for {for_upd.shape[0]}")
        os.system(f"{f_sap}")
        time.sleep(7)
        os.system(f"{f_upd_class}")
        output.add(f"Finished PCE Z62 SAP Update")

    return end_script(server)
