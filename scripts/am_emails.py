def am_emails():
    import os
    import pandas as pd
    import warnings
    from datetime import date
    import dotenv
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    warnings.filterwarnings("ignore")

    today = date.today().strftime("%m-%d-%Y")

    active = pd.read_excel(os.environ['AP_LOG'],
                           sheet_name='Active Materials', dtype=str)
    # active.tail(2)

    # VIEW LIKE ACTIVE SHEET IN EXCEL
    # selected_active_view = active[['Date Added', 'target sorg', 'target plant', 'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'Catalog', 'Ser', 'MTART/GenItemCat', ' sorg1k dchain', ' sorg1k cs', 'sorg1k price', ' sorg4k dchain', ' sorg4k cs', 'PGC', 'target sorg price', 'target sorg dchain', 'target sorg DWERK', 'target sorg cs', 'target sorg pub', 'target plant status', 'target plant mrp type', 'DWERK Plant Status', 'DWERK Plant Code', "mif/soerf check", 'Sales Text', 'INDIA GST\nINHTS', 'INDIA GST\nmarc.stuec', 'INDIA GST taxm1', 'STATUS_CHINA_ENERGY_LBL', "Regulatory Cert\n(Z62 Class)", 'Regulatory Cert\n(Z62 Characteristic)', 'Z62 characteristic\n(assigned in SAP)', 'PCE Assessment\n(received)', 'Date of PCE review', 'MIF Submitted', 'SOERF Submitted', 'pricing request', 'PCE cert rev req\'d', 'status', 'sort order']]

    # MATNRs PRICE NEEDED
    # price_needed = selected_active_view.loc[
    #   (selected_active_view['target sorg price'].isna()) &
    #   (~selected_active_view['SOERF Submitted'].isna()) &
    #   ((selected_active_view['status'].str.contains('cancel|complete', case=False) == False))
    # ]
    # PRICE REQUEST ALL
    price_view = active[['Date Added', 'target sorg', 'target plant', "email prefix\n(from request form)", "SAP MATNR\n(from request form)", "Service Requested\n(from request form)", "Location\n(from request form)",
                        'description', 'Catalog', 'Ser', "MTART/GenItemCat", ' sorg1k dchain', ' sorg1k cs', 'sorg1k price', ' sorg4k dchain', ' sorg4k cs', 'PGC', 'target sorg price', 'target sorg dchain', 'pricing request', 'status']]
    need_price = price_view.loc[
        (price_view['status'].str.contains('needs price;', case=True) == True)
    ]
    if need_price.empty:
        print('NO PCE REQUESTS')
    else:
        need_price[['Date Added', 'pricing request']] = need_price[[
            'Date Added', 'pricing request']].apply(pd.to_datetime)
        need_price['Date Added'] = need_price['Date Added'].dt.strftime(
            '%m/%d/%Y')
        need_price['pricing request'] = need_price['pricing request'].dt.strftime(
            '%m/%d/%Y')

    print('Needing price: ')
    print(len(need_price))
    # PRICE REQUEST FILE
    need_price_list_file = os.path.join(
        os.environ["HOME_DIR"], "AP pricing needed with active demand {0}.xlsx".format(today))
    need_price.to_excel(need_price_list_file,  index=False)

    # MATNRs PCE NEEDED
    # pce_needed = selected_active_view[
    #   (((selected_active_view['status'].str.contains('cancel|complete', case=False) == False)) & (selected_active_view['Service Requested\n(from request form)'] == 'Product Certification Review'))  |
    #   ((selected_active_view['MTART/GenItemCat'].isin(['ZFG', 'ZTG'])) & (~selected_active_view['Regulatory Cert\n(Z62 Characteristic)'].isna()) & (selected_active_view['Z62 characteristic\n(assigned in SAP)'].isna()) & ((selected_active_view['status'].str.contains('cancel|complete', case=False) == False)))
    # ]
    # PCE REQUEST
    active_wt_pce_req = active.loc[
        (active['status'].str.contains('pending PCE review;', case=True) == True) &
        (~active['Regulatory Cert\n(Z62 Class)'].isin(['CCC']))
    ]
    if active_wt_pce_req.empty:
        print('NO PCE REQUESTS')
    else:
        need_pce = active_wt_pce_req[['Date Added', 'target sorg', 'target plant', "email prefix\n(from request form)", "SAP MATNR\n(from request form)", "Service Requested\n(from request form)", "Location\n(from request form)", 'description', 'Catalog',
                                      'Ser', 'target sorg DWERK', 'DWERK Plant Code', 'Regulatory Cert\n(Z62 Class)', 'Regulatory Cert\n(Z62 Characteristic)', 'Z62 characteristic\n(assigned in SAP)', 'PCE Assessment\n(received)', 'Date of PCE review', "PCE cert rev req'd"]]
        need_pce['New PCE Assessment'] = ""
        need_pce[['Date Added', 'Date of PCE review', "PCE cert rev req'd"]] = need_pce[[
            'Date Added', 'Date of PCE review', "PCE cert rev req'd"]].apply(pd.to_datetime)
        need_pce['Date Added'] = need_pce['Date Added'].dt.strftime('%m/%d/%Y')
        need_pce['Date of PCE review'] = need_pce['Date of PCE review'].dt.strftime(
            '%m/%d/%Y')
        need_pce["PCE cert rev req'd"] = need_pce["PCE cert rev req'd"].dt.strftime(
            '%m/%d/%Y')

    print('PCE requests:')
    print(len(active_wt_pce_req))
    # PCE REQUEST FILE - AM
    need_pce_file = os.path.join(
        os.environ["HOME_DIR"], "{0} PCE ASSESSMENT REQUEST.xlsx".format(today))
    need_pce.to_excel(need_pce_file,  index=False)
