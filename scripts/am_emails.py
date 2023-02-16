def am_emails(server=False):
    import os
    import pandas as pd
    from datetime import date
    from markupsafe import Markup

    from helpers.helpers import (
        use_dotenv,
        ignore_warnings,
        await_char,
        use_logger,
        output_msg,
        format_request_date,
    )
    from helpers.datetime import today_ymd
    from helpers.data_frames import get_active
    import helpers.prompts as pr
    from state.output import output

    use_dotenv()
    use_logger()
    ignore_warnings()

    today_file = today_ymd("-")
    output.reset()
    active = get_active()

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
        # NOTE: OLD DATE FORMATTING | TO CLEAN UP LATER
        # need_price[["Date Added", "pricing request"]] = need_price[
        #     ["Date Added", "pricing request"]
        # ].apply(pd.to_datetime)
        # need_price["Date Added"] = need_price["Date Added"].dt.strftime("%m/%d/%Y")
        # need_price["pricing request"] = need_price["pricing request"].dt.strftime(
        #     "%m/%d/%Y"
        # )

        output.add(f"{pr.info}Needing price: {len(need_price)}")
        # PRICE REQUEST FILE
        need_price_list_file = os.path.join(
            os.environ["DIR_OUT"],
            f"AP pricing needed with active demand {today_file}.xlsx",
        )
        need_price.to_excel(need_price_list_file, index=False)

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
        # NOTE: OLD DATE FORMATTING | TO CLEAN UP LATER
        # need_pce[['Date Added', 'Date of PCE review', "PCE cert rev req'd"]] = need_pce[[
        #     'Date Added', 'Date of PCE review', "PCE cert rev req'd"]].apply(pd.to_datetime)
        # need_pce['Date Added'] = need_pce['Date Added'].dt.strftime('%m/%d/%Y')
        # need_pce['Date of PCE review'] = need_pce['Date of PCE review'].dt.strftime(
        #     '%m/%d/%Y')
        # need_pce["PCE cert rev req'd"] = need_pce["PCE cert rev req'd"].dt.strftime(
        #     '%m/%d/%Y')

        output.add(f"{pr.info}PCE requests: {len(active_wt_pce_req)}")
        # PCE REQUEST FILE - AM
        need_pce_file = os.path.join(
            os.environ["DIR_OUT"], f"{today_file} PCE ASSESSMENT REQUEST.xlsx"
        )
        need_pce.to_excel(need_pce_file, index=False)

    if server == False:
        await_char()
    else:
        return output.get_markup
