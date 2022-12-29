def reconcile_pce(server):
    import os
    import pandas as pd

    from helpers.helpers import await_char, use_dotenv, ignore_warnings, use_logger
    from helpers.datetime import today_ymd
    from helpers.log import save_log, load_log, test_save
    from helpers.data_frames import get_active

    use_dotenv()
    use_logger()
    ignore_warnings()

    today = today_ymd("-")
    upd_file = os.path.join(
        os.environ['DIR_OUT'], 'UPDATES TO Z62.txt')

    # ORGINAL SOURCE
    mifs = get_active('mif')

    # mifs_view = mifs[['MATERIAL']]
    mifs['date'] = mifs['date'].map(lambda x: str(x)[:-9])
    mifs_today = mifs[mifs['date'] == today]
    mifs_list = mifs_today['MATERIAL']
    mifs_list.to_clipboard(sep=',', index=False, header=None)

    # FIND PCE REQUEST
    pce_feedback = pd.DataFrame()
    for filename in os.listdir('C:\RA-Apps\AP-Proc\INPUTS'):
        file = os.path.join('C:\RA-Apps\AP-Proc\INPUTS', filename)
        if ' ASSESSMENT REQUEST' in filename:
            print("\t" + file)
            df = pd.read_excel(file)
            pce_feedback = pd.concat([pce_feedback, df])

    # PCE FEEDBACK TO LOG
    for_log = pce_feedback.iloc[:, [4, 12, 13, 18]]
    for_log = for_log[for_log['New PCE Assessment'].notna()]
    # TODO: update the ap log

    # PCE FEDDBACK TO UPDATE FILE
    for_upd = pce_feedback.iloc[:, [4, 12, 13, 18]]
    for_upd = for_log[for_log['New PCE Assessment'].notna()]
    for_upd["SAP Table"] = "MARA"
    for_upd["Class"] = "Z62"
    for_upd["Blank 1"] = ""
    for_upd["Blank 2"] = ""
    for_upd = for_upd[['SAP Table', 'SAP MATNR\n(from request form)', 'Class', 'Blank 1',
                       'Blank 2', 'Regulatory Cert\n(Z62 Characteristic)', 'New PCE Assessment']]
    for_upd.to_csv(upd_file, header=None, index=False, sep='\t')
