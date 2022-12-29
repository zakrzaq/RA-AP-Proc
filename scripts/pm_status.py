def pm_status(server):
    import os
    import pandas as pd

    from helpers.helpers import await_char, ignore_warnings, use_dotenv, use_logger
    from helpers.log import save_log, test_save, load_log
    from helpers.xlsm import populate_sheet_series
    from helpers.data_frames import get_selected_active

    use_dotenv()
    use_logger()
    ignore_warnings()

    log = load_log()
    ws_active = log['Active Materials']

    selected_active_view = get_selected_active()

    # VERIFY PRICED
    selected_active_view.loc[
        (selected_active_view['status'].str.contains('needs price;')) &
        (~selected_active_view['target sorg price'].isna()),
        'status'
    ] = selected_active_view['status'].str.replace('needs price;', '')

    # VERIFY PCE
    selected_active_view.loc[
        (selected_active_view['status'].str.contains('pending PCE review;')) &
        (selected_active_view['Regulatory Cert\n(Z62 Class)'].isin(['BIS', 'BSMI', 'CCC', 'KC', 'RCM'])) &
        (selected_active_view['Z62 characteristic\n(assigned in SAP)'].notna())
    ] = selected_active_view['status'].str.replace('pending PCE review;', '')

    # VERIFY GTS
    selected_active_view.loc[
        (selected_active_view['status'].str.contains('GST data needed;')) &
        (
            (selected_active_view['INDIA GST\nINHTS'].notna()) |
            (selected_active_view['INDIA GST\nmarc.stuec'].notna())
        ),
        'status'
    ] = selected_active_view['status'].str.replace('GST data needed;', '')

    # VERIFY LOCAL
    selected_active_view.loc[
        (selected_active_view['status'].str.contains('Localization required;')) &
        (~selected_active_view['target plant mrp type'].isin(['ND'])),
        'status'
    ] = selected_active_view['status'].str.replace('Localization required;', '')

    # MATNRs GTS NEEDED
    need_gts = (
        (selected_active_view['target sorg'].isin(['5008'])) &
        (selected_active_view['INDIA GST\nINHTS'].isna()) &
        (selected_active_view['INDIA GST\nmarc.stuec'].isna()) &
        (selected_active_view['status'].str.contains('cancel|complete|hold', case=False) == False) &
        (selected_active_view['status'].str.contains(
            'GST data needed;') == False)
    )

    selected_active_view.loc[need_gts, 'status'] = selected_active_view['status'].astype(
        str) + "GST data needed;"

    gts_requested = selected_active_view.loc[
        (selected_active_view['status'].str.contains(
            'GST data needed;') == True)
    ]
    print('Materials needing GTS in log:')
    print(len(gts_requested))

    # MATNRs LOCAL NEEDED
    need_local = (
        (selected_active_view['MTART/GenItemCat'].isin(['ZFG', 'ZTG', 'ZNFG', 'ZRS1', 'ZRS4'])) &
        (~selected_active_view['target plant'].isin(['5070'])) &
        (selected_active_view['target plant mrp type'].isin(['NA'])) &
        (selected_active_view['status'].str.contains('cancel|complete|hold', case=False) == False) &
        (selected_active_view['status'].str.contains(
            'Localization required;') == False)
    )

    selected_active_view.loc[need_local, 'status'] = selected_active_view['status'].astype(
        str) + 'Localization required;'

    local_requested = selected_active_view.loc[
        (selected_active_view['status'].str.contains(
            'Localization required;') == True)
    ]
    print('Materials needing LOCALIZATION in log:')
    print(len(local_requested))

    # SAVE TXT
    # status_file = os.path.join(os.environ['DIR_DESKTOP'], 'AP_status.txt')
    status_output = selected_active_view['status']
    status_output_str = ''

    # if os.path.exists(status_file):
    #     os.remove(status_file)
    for ind in status_output.index:
        status_output_str = status_output_str + str(status_output[ind]) + "\n"
    # with open(status_file, 'w') as file:
    #     file.writelines(status_output_str)

    # TEST SAVE LOG
    populate_sheet_series(status_output, ws_active, 50, 2)
    test_save(log, "TEST_pm_status")
    # ACTUAL
    await_char(
        "y", "Press Y to save to live LOG file or C to cancel.",  save_log, log)
