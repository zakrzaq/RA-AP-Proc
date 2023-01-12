def reconcile_pce(server=False):
    import os
    import pandas as pd
    import time
    from markupsafe import Markup

    from helpers.helpers import await_char, use_dotenv, ignore_warnings, use_logger, output_msg
    from helpers.datetime import today_ymd, today_dmy
    from helpers.log import save_log, load_log, test_save
    from helpers.data_frames import get_active
    from helpers.xlsm import populate_sap_data_sheet, extend_concats

    use_dotenv()
    use_logger()
    ignore_warnings()

    today = today_ymd("-")
    ws_today = today_dmy()
    f_sap = os.path.join(os.environ['DIR_APP'], 'sap', 'sap.ahk')
    f_org_source = os.path.join(os.environ['DIR_APP'], 'sap', 'org_source.ahk')
    f_upd_class = os.path.join(os.environ['DIR_APP'], 'sap', 'upd_class.ahk')
    upd_file = os.path.join(
        os.environ['DIR_OUT'], 'UPDATES TO Z62.txt')
    output = ''

    # ORGINAL SOURCE
    output += output_msg('Preparing ORG Source')
    mifs = get_active('mif')
    mifs['date'] = mifs['date'].map(lambda x: str(x)[:-9])
    mifs_today = mifs[mifs['date'] == today]
    mifs_list = mifs_today['MATERIAL']
    mifs_list.to_clipboard(sep=',', index=False, header=None)
    os.system(f'{f_sap}')
    time.sleep(7)
    output += output_msg('Running ORG Source AHK')
    os.system(f'{f_org_source}')
    output += output_msg('Finished ORG Source')

    # FIND PCE REQUEST
    output += output_msg('Preparing PCE Reconciliation')
    pce_feedback = pd.DataFrame()
    for filename in os.listdir('C:\RA-Apps\AP-Proc\INPUTS'):
        file = os.path.join('C:\RA-Apps\AP-Proc\INPUTS', filename)
        if ' ASSESSMENT REQUEST' in filename:
            output += output_msg("\t" + file)
            df = pd.read_excel(file)
            pce_feedback = pd.concat([pce_feedback, df])

    # PCE FEEDBACK TO LOG
    try:
        output += output_msg('Processing PCE Reconciliation')
        log = load_log()
        ws_pce = log['pce']
        last_row = ws_pce.max_row + 1

        for_log = pce_feedback.iloc[:, [4, 12, 13, 18]]
        for_log = for_log[for_log['New PCE Assessment'].notna()]

        populate_sap_data_sheet(for_log, ws_pce, 2, last_row)
        # insert dates
        # TODO: fix date format to excel
        new_last = ws_pce.max_row
        for i in range(last_row, new_last + 1, 1):
            ws_pce[f'F{i}'].value = ws_today
        # CONCAT
        extend_concats(ws_pce, last_row - 1, "A")

        # TEST SAVE
        test_save(log, 'TEST_pce_reconcile')
        # ACTUAL
        # TODO: update the ap log
        if server == False:
            await_char(
                "y", "Press Y to save to live LOG file or C to cancel.",  save_log, log)
        else:
            save_log(log)
            output += output_msg('LOG file saved')
            return Markup(output)
    except:
        output += output_msg('Unable to load the LOG to update PCE')

    # PCE FEDDBACK TO UPDATE FILE
    output += output_msg('Preparing PCE SAP Update')
    for_upd = pce_feedback.iloc[:, [4, 12, 13, 18]]
    for_upd = for_log[for_log['New PCE Assessment'].notna()]
    for_upd["SAP Table"] = "MARA"
    for_upd["Class"] = "Z62"
    for_upd["Blank 1"] = ""
    for_upd["Blank 2"] = ""
    for_upd = for_upd[['SAP Table', 'SAP MATNR\n(from request form)', 'Class', 'Regulatory Cert\n(Z62 Class)', 'Blank 1',
                       'Blank 2', 'Regulatory Cert\n(Z62 Characteristic)', 'New PCE Assessment']]
    for_upd.to_csv(upd_file, header=None, index=False, sep='\t')
    os.system(f'{f_sap}')
    time.sleep(7)
    output += output_msg('Processing PCE SAP Update')
    os.system(f'{f_upd_class}')
    output += output_msg('Finished PCE SAP Update')
