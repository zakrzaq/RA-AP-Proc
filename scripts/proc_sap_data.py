def proc_sap_data():
    import pandas as pd
    import os

    from helpers.helpers import await_char, use_dotenv, ignore_warnings, use_logger
    from helpers.log import load_log, save_log, test_save
    from helpers.xlsm import populate_sap_data_sheet, extend_concats

    use_dotenv()
    use_logger()
    ignore_warnings()

    # OPEN LOG FILE NAD GENERATE SHEETS VARIABLES
    print("Reading log file")
    log = load_log()

    ws_mara = log['mara']
    ws_marc = log['marc']
    ws_mvke = log['mvke']
    ws_ausp = log['ausp']
    ws_mlan = log['mlan']
    ws_price = log['ZZ_MATPRC_HIST']
    ws_gts = log['gts']
    ws_text = log['sales text']
    # ws_list = [ws_mara, ws_marc, ws_mvke, ws_ausp,
    #            ws_mlan, ws_price, ws_gts, ws_text]

    # # clean out data
    print("Truncating data")
    ws_mara.delete_rows(100, ws_mara.max_row)
    ws_marc.delete_rows(100, ws_mara.max_row)
    ws_mvke.delete_rows(100, ws_mara.max_row)
    ws_ausp.delete_rows(100, ws_mara.max_row)
    ws_mlan.delete_rows(100, ws_mara.max_row)
    ws_price.delete_rows(100, ws_mara.max_row)
    ws_gts.delete_rows(100, ws_mara.max_row)
    ws_text.delete_rows(100, ws_mara.max_row)

    # DEFINE DATA FILES
    mara = marc = mvke = ausp = mlan = price = gts = text = pd.DataFrame()

    fl_mara = os.path.join(os.environ['DIR_IN'], 'mara.XLSX')
    fl_marc = os.path.join(os.environ['DIR_IN'],  'marc.XLSX')
    fl_mvke = os.path.join(os.environ['DIR_IN'],  'mvke.XLSX')
    fl_ausp = os.path.join(os.environ['DIR_IN'], 'ausp.XLSX')
    fl_mlan = os.path.join(os.environ['DIR_IN'], 'mlan.XLSX')
    fl_price = os.path.join(os.environ['DIR_IN'], 'price.XLSX')
    fl_gts = os.path.join(os.environ['DIR_IN'], 'gts.XLSX')
    fl_text = os.path.join(os.environ['DIR_IN'], 'sales_text.xls')

    # load sap data to df
    print("Loading new SAP data")
    if os.path.exists(fl_mara):
        mara = pd.read_excel(fl_mara)
    if os.path.exists(fl_marc):
        marc = pd.read_excel(fl_marc)
    if os.path.exists(fl_mvke):
        mvke = pd.read_excel(fl_mvke)
    if os.path.exists(fl_ausp):
        ausp = pd.read_excel(fl_ausp)
    if os.path.exists(fl_mlan):
        mlan = pd.read_excel(fl_mlan)
    if os.path.exists(fl_price):
        price = pd.read_excel(fl_price)
    if os.path.exists(fl_gts):
        gts = pd.read_excel(fl_gts)
    if os.path.exists(fl_text):
        text = pd.read_csv(fl_text, sep='\t', encoding="utf-16")

    inputs_list = [mara, marc, mvke, ausp, mlan, price, gts, text]

    # FORMAT DATA
    # TODO: price[Valid to] is a long date and needs to be format different
    # just now it returning blank rows
    mvke['VMSTD'] = pd.to_datetime(
        mvke['VMSTD'], errors='coerce').dt.strftime('%d-%m-%Y')
    price['Valid to'] = pd.to_datetime(
        price['Valid to'], errors='coerce').dt.strftime('%d-%m-%Y')
    price['Valid From'] = pd.to_datetime(
        price['Valid From'], errors='coerce').dt.strftime('%d-%m-%Y')

    # FUNCTIONS
    inputs_not_empty = 0
    for input in inputs_list:
        if not input.empty:
            print(input.head(1))
            inputs_not_empty += 1

    if inputs_not_empty == 8:
        print("Populate new data")
        populate_sap_data_sheet(mara, ws_mara,)
        populate_sap_data_sheet(marc, ws_marc)
        populate_sap_data_sheet(mvke, ws_mvke)
        populate_sap_data_sheet(ausp, ws_ausp)
        populate_sap_data_sheet(mlan, ws_mlan)
        populate_sap_data_sheet(price, ws_price)
        populate_sap_data_sheet(gts, ws_gts, 1, 2)
        populate_sap_data_sheet(text, ws_text)

        extend_concats(ws_mara)
        extend_concats(ws_marc)
        extend_concats(ws_mvke)
        extend_concats(ws_ausp)
        extend_concats(ws_mlan)
        extend_concats(ws_price)
        extend_concats(ws_text)

        # save test log
        print("Save results")
        test_save(log, "TEST_sap_data")
        # save ACTUAL log
        await_char(
            "y", "Press Y to save to live LOG file or C to cancel.",  save_log, log)

    else:
        print(f'Missing SAP data - {inputs_not_empty}')
        await_char("y")
