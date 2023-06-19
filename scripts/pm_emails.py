def pm_emails(server=False):
    import os
    import pandas as pd
    from datetime import date

    from helpers.helpers import (
        ignore_warnings,
        end_script,
        use_dotenv,
        use_logger,
    )
    from helpers.data_frames import get_active
    import helpers.prompts as pr
    from state.output import output
    from state.email import email
    from helpers.emails import send_email
    from data.email_notifications import ccc_email, inhts_email, local_email

    use_dotenv()
    use_logger()
    ignore_warnings()

    today = date.today().strftime("%m-%d-%Y")
    active = get_active()
    output.reset()
    need_ccc_file = os.path.join(
        os.environ["DIR_OUT"], f"{today} CCC ASSESSMENT REQUEST.xlsx"
    )
    need_gts_file = os.path.join(os.environ["DIR_OUT"], f"INHTS request {today}.xlsx")
    need_local_file = os.path.join(
        os.environ["DIR_OUT"], f"India localization required {today}.xlsx"
    )

    if not active.empty:
        # PCE REQUEST
        active_wt_pce_req = active.loc[
            (active["status"].str.contains("pending PCE review;", case=True) == True)
            & (active["Regulatory Cert\n(Z62 Class)"].isin(["CCC"]))
        ]
        if active_wt_pce_req.empty:
            output.add(f"{pr.cncl}NO CCC REQUESTS")
        else:
            need_pce = active_wt_pce_req[
                [
                    "Date Added",
                    "target sorg",
                    "target plant",
                    "email prefix\n(from request form)",
                    "SAP MATNR\n(from request form)",
                    "Service Requested\n(from request form)",
                    "Location\n(from request form)",
                    "description",
                    "Catalog",
                    "Ser",
                    "target sorg DWERK",
                    "DWERK Plant Code",
                    "Regulatory Cert\n(Z62 Class)",
                    "Regulatory Cert\n(Z62 Characteristic)",
                    "Z62 characteristic\n(assigned in SAP)",
                    "PCE Assessment\n(received)",
                    "Date of PCE review",
                    "PCE cert rev req'd",
                ]
            ]
            need_pce["new PCE assessment"] = ""
            # remove duplicates
            need_pce.drop_duplicates(
                subset=["SAP MATNR\n(from request form)", "target sorg"], keep="last"
            )
            # need_pce[['Date Added', 'Date of PCE review', "PCE cert rev req'd"]] = need_pce[[
            #     'Date Added', 'Date of PCE review', "PCE cert rev req'd"]].apply(pd.to_datetime)
            # need_pce['Date Added'] = need_pce['Date Added'].dt.strftime('%m/%d/%Y')
            # need_pce['Date of PCE review'] = need_pce['Date of PCE review'].dt.strftime(
            #     '%m/%d/%Y')
            # need_pce["PCE cert rev req'd"] = need_pce["PCE cert rev req'd"].dt.strftime(
            #     '%m/%d/%Y')

            output.add(f"{pr.ok}CCC requests: {len(active_wt_pce_req)}")
            # PCE REQUEST FILE - AM
            need_pce.to_excel(need_ccc_file, index=False)

        # GTS REQUESTS
        active_wt_gts_req = active.loc[
            (active["status"].str.contains("GST data needed;", case=True) == True)
        ]
        if active_wt_gts_req.empty:
            output.add(f"{pr.cncl}NO GTS REQUESTS")
        else:
            need_gts = active_wt_gts_req[
                [
                    "Date Added",
                    "target sorg",
                    "email prefix\n(from request form)",
                    "SAP MATNR\n(from request form)",
                    "description",
                    "Catalog",
                    "Ser",
                    "MTART/GenItemCat",
                    "target sorg DWERK",
                    "DWERK Plant Code",
                    "INDIA GST\nINHTS",
                ]
            ]
            need_gts["Date Added"] = need_gts["Date Added"].apply(lambda x: (x[0:10]))
            need_gts["Date Added"] = need_gts["Date Added"].apply(pd.to_datetime)
            need_gts["Date Added"] = need_gts["Date Added"].dt.strftime("%m/%d/%Y")

            output.add(f"{pr.ok}GTS requests: {len(active_wt_gts_req)}")
            # GTS REQUEST FILE

            need_gts.to_excel(need_gts_file, index=False)

        # ### LOCAL REQUESTS
        active_wt_local_req = active.loc[
            (active["status"].str.contains("Localization required;", case=True) == True)
        ]
        if active_wt_local_req.empty:
            output.add(f"{pr.cncl}NO LOCALIZATION REQUESTS")
        else:
            need_local = active_wt_local_req[
                [
                    "Date Added",
                    "target sorg",
                    "target plant",
                    "SAP MATNR\n(from request form)",
                    "description",
                    "Catalog",
                    "Ser",
                    "MTART/GenItemCat",
                    " sorg1k dchain",
                    " sorg1k cs",
                    "sorg1k price",
                    " sorg4k dchain",
                    " sorg4k cs",
                    "PGC",
                    "target sorg price",
                    "target sorg dchain",
                    "target sorg DWERK",
                    "target sorg cs",
                    "target sorg pub",
                    "target plant status",
                    "target plant mrp type",
                    "DWERK Plant Status",
                    "DWERK Plant Code",
                    "mif/soerf check",
                    "Sales Text",
                    "INDIA GST\nINHTS",
                    "INDIA GST\nmarc.stuec",
                    "INDIA GST taxm1",
                    "MIF Submitted",
                    "SOERF Submitted",
                ]
            ]
            # need_local[['Date Added', 'MIF Submitted', 'SOERF Submitted']] = need_local[[
            #     'Date Added', 'MIF Submitted', 'SOERF Submitted']].apply(pd.to_datetime(errors='coerce'))
            need_local["Date Added"] = pd.to_datetime(
                need_local["Date Added"], errors="coerce"
            ).dt.strftime("%m/%d/%Y")
            need_local["MIF Submitted"] = pd.to_datetime(
                need_local["MIF Submitted"], errors="coerce"
            ).dt.strftime("%m/%d")
            need_local["SOERF Submitted"] = pd.to_datetime(
                need_local["SOERF Submitted"], errors="coerce"
            ).dt.strftime("%m/%d")

            output.add(f"{pr.ok}LOCALIZATION requests: {len(active_wt_local_req)}")
            # GTS REQUEST FILE
            need_local.to_excel(need_local_file, index=False)

            # SEND EMAILS
            if os.path.isfile(need_ccc_file):
                email.set(ccc_email)
                send_email(need_ccc_file)

            if os.path.isfile(need_gts_file):
                email.set(inhts_email)
                send_email(need_gts_file)

            if os.path.isfile(need_local_file):
                email.set(local_email)
                send_email(need_local_file)

    return end_script(server)
