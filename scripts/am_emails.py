def am_emails(server=False, method='GET'):
    import os

    from utils.helpers import (
        use_dotenv,
        ignore_warnings,
        end_script,
        use_logger,
        format_request_date,
    )
    from utils.datetime import today_ymd
    from utils.data_frames import get_active
    from utils.submissions import send_email
    import utils.prompts as pr

    from state.output import output
    from state.email import email
    from state.time import timer

    from data.email_notifications import pce_email, price_email

    timer.start()
    use_dotenv()
    use_logger()
    ignore_warnings()

    today_file = today_ymd("-")
    output.reset()
    active = get_active()

    if not active.empty:
        # PRICE REQUEST ALL
        price_view = active[
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
                "MTART/GenItemCat",
                " sorg1k dchain",
                " sorg1k cs",
                "sorg1k price",
                " sorg4k dchain",
                " sorg4k cs",
                "PGC",
                "target sorg price",
                "target sorg dchain",
                "pricing request",
                "status",
            ]
        ]
        need_price = price_view.loc[
            (price_view["status"].str.contains("needs price;", case=True) == True)
        ]
        if need_price.empty:
            output.add(f"{pr.cncl}NO PRICE REQUESTS")
        else:
            need_price["Date Added"] = need_price["Date Added"].map(format_request_date)

            output.add(f"{pr.info}Needing price: {len(need_price)}")
            # PRICE REQUEST FILE
            need_price_list_file = os.path.join(
                os.environ["DIR_OUT"],
                f"AP pricing needed with active demand {today_file}.xlsx",
            )
            need_price.to_excel(need_price_list_file, index=False)

            # SEND EMAIL
            if os.path.isfile(need_price_list_file):
                email.set(price_email)
                send_email(need_price_list_file)

        # PCE REQUEST
        active_wt_pce_req = active.loc[
            (active["status"].str.contains("pending PCE review;", case=True) == True)
            & (~active["Regulatory Cert\n(Z62 Class)"].isin(["CCC"]))
        ]
        if active_wt_pce_req.empty:
            output.add(f"{pr.cncl}NO PCE REQUESTS")
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
            need_pce["Date Added"] = need_pce["Date Added"].map(format_request_date)
            # remove duplicates
            need_pce.drop_duplicates(
                subset=["SAP MATNR\n(from request form)", "target sorg"], keep="last"
            )

            output.add(f"{pr.info}PCE requests: {len(active_wt_pce_req)}")
            # PCE REQUEST FILE - AM
            need_pce_file = os.path.join(
                os.environ["DIR_OUT"], f"{today_file} PCE ASSESSMENT REQUEST.xlsx"
            )
            need_pce.to_excel(need_pce_file, index=False)

            # SEND EMAIL
            if os.path.isfile(need_pce_file):
                email.set(pce_email)
                send_email(need_pce_file)

    timer.stop()
    output.add(f"{pr.ok}Script completed: {timer.get_elapsed_time()}")
    return end_script(server, method)
