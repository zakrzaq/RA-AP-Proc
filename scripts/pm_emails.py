def pm_emails():
    import os
    import pandas as pd
    from datetime import date

    from helpers.helpers import ignore_warnings, await_char, use_dotenv, use_logger
    from helpers.data_frames import get_active

    use_dotenv()
    use_logger()
    ignore_warnings()

    today = date.today().strftime("%m-%d-%Y")

    active = get_active()

    # PCE REQUEST
    active_wt_pce_req = active.loc[
        (active['status'].str.contains('pending PCE review;', case=True) == True) &
        (active['Regulatory Cert\n(Z62 Class)'].isin(['CCC']))
    ]
    if active_wt_pce_req.empty:
        print('NO CCC REQUESTS')
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

        print(f'CCC requests: {len(active_wt_pce_req)}')
        # PCE REQUEST FILE - AM
        need_pce_file = os.path.join(
            os.environ['DIR_OUT'], f"{today} CCC ASSESSMENT REQUEST.xlsx")
        need_pce.to_excel(need_pce_file,  index=False)

    # GTS REQUESTS
    active_wt_gts_req = active.loc[
        (active['status'].str.contains('GST data needed;', case=True) == True)
    ]
    if active_wt_gts_req.empty:
        print('NO GTS REQUESTS')
    else:
        need_gts = active_wt_gts_req[['Date Added', 'target sorg', 'email prefix\n(from request form)', 'SAP MATNR\n(from request form)',
                                      'description', 'Catalog', 'Ser', 'MTART/GenItemCat', 'target sorg DWERK', 'DWERK Plant Code', 'INDIA GST\nINHTS']]
        need_gts['Date Added'] = need_gts['Date Added'].apply(
            lambda x: (x[0:10]))
        need_gts['Date Added'] = need_gts['Date Added'].apply(pd.to_datetime)
        need_gts['Date Added'] = need_gts['Date Added'].dt.strftime('%m/%d/%Y')

        print(f'GTS requests: {len(active_wt_gts_req)}')
        # GTS REQUEST FILE
        need_gts_file = os.path.join(
            os.environ['DIR_OUT'], f"INHTS request {today}.xlsx")
        need_gts.to_excel(need_gts_file,  index=False)

    # ### LOCAL REQUESTS
    active_wt_local_req = active.loc[
        (active['status'].str.contains(
            'Localization required;', case=True) == True)
    ]
    if active_wt_local_req.empty:
        print('NO LOCALIZATION REQUESTS')
    else:
        need_local = active_wt_local_req[['Date Added', 'target sorg', 'target plant', 'SAP MATNR\n(from request form)', 'description', 'Catalog', 'Ser', 'MTART/GenItemCat', ' sorg1k dchain', ' sorg1k cs', 'sorg1k price', ' sorg4k dchain', ' sorg4k cs', 'PGC', 'target sorg price', 'target sorg dchain',
                                          'target sorg DWERK', 'target sorg cs', 'target sorg pub', 'target plant status', 'target plant mrp type', 'DWERK Plant Status', 'DWERK Plant Code', 'mif/soerf check', 'Sales Text', 'INDIA GST\nINHTS', 'INDIA GST\nmarc.stuec', 'INDIA GST taxm1', 'MIF Submitted', 'SOERF Submitted']]
        need_local[['Date Added', 'MIF Submitted', 'SOERF Submitted']] = need_local[[
            'Date Added', 'MIF Submitted', 'SOERF Submitted']].apply(pd.to_datetime)
        need_local['Date Added'] = need_local['Date Added'].apply(
            pd.to_datetime).dt.strftime('%m/%d/%Y')
        need_local['MIF Submitted'] = need_local['MIF Submitted'].dt.strftime(
            '%m/%d')
        need_local['SOERF Submitted'] = need_local['SOERF Submitted'].dt.strftime(
            '%m/%d')

        print(f'LOCALIZATION requests: {len(active_wt_local_req)}')
        # GTS REQUEST FILE
        need_local_file = os.path.join(
            os.environ['DIR_OUT'], f"India localization required {today}.xlsx")
        need_local.to_excel(need_local_file,  index=False)

    await_char()
