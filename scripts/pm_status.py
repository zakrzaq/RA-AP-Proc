def pm_status(server=False):
    import os
    import pandas as pd
    from markupsafe import Markup

    from helpers.helpers import (
        await_char,
        ignore_warnings,
        use_dotenv,
        use_logger,
        output_msg,
        format_pce_price_dates,
    )
    from helpers.log import save_log, test_save, load_log
    from helpers.xlsm import populate_sheet_series
    from helpers.data_frames import get_selected_active

    use_dotenv()
    use_logger()
    ignore_warnings()

    log = load_log()
    ws_active = log["Active Materials"]
    selected_active_view = get_selected_active()
    output = ""

    # VERIFY PRICED
    been_priced = (selected_active_view["status"].str.contains("needs price;")) & (
        ~selected_active_view["target sorg price"].isna()
    )

    selected_active_view.loc[been_priced, "status"] = selected_active_view[
        "status"
    ].str.replace("needs price;", "")
    selected_active_view.loc[been_priced, "pricing request"] = "comp"

    # VERIFY PCE
    been_pce_revived = (
        (selected_active_view["status"].str.contains("pending PCE review;"))
        & (
            selected_active_view["Regulatory Cert\n(Z62 Class)"].isin(
                ["BIS", "BSMI", "CCC", "KC", "RCM"]
            )
        )
        & (selected_active_view["Z62 characteristic\n(assigned in SAP)"].notna())
    )

    selected_active_view.loc[been_pce_revived, "status"] = selected_active_view[
        "status"
    ].str.replace("pending PCE review;", "")
    selected_active_view.loc[been_pce_revived, "PCE cert rev req'd"] = "comp"

    # VERIFY GTS
    selected_active_view.loc[
        (selected_active_view["status"].str.contains("GST data needed;"))
        & (
            (selected_active_view["INDIA GST\nINHTS"].notna())
            | (selected_active_view["INDIA GST\nmarc.stuec"].notna())
        ),
        "status",
    ] = selected_active_view["status"].str.replace("GST data needed;", "")

    # VERIFY LOCAL
    been_localized = (
        selected_active_view["status"].str.contains("Localization required;")
    ) & (~selected_active_view["target plant mrp type"].isin(["ND", "X0"]))
    selected_active_view.loc[been_localized, "status"] = selected_active_view[
        "status"
    ].str.replace("Localization required;", "")

    # MATNRs GTS NEEDED
    done_status = "|".join(["cancel", "complete", "on hold", "GST data needed"])

    need_gts = (
        (selected_active_view["target sorg"].isin(["5008"]))
        & (selected_active_view["INDIA GST\nINHTS"].isna())
        & (selected_active_view["INDIA GST\nmarc.stuec"].isna())
        & (
            (
                (
                    selected_active_view["status"].str.contains(done_status, case=False)
                    == False
                )
            )
            | (selected_active_view["status"].isna())
        )
    )

    selected_active_view.loc[need_gts, "status"] = (
        selected_active_view["status"].astype(str).replace("nan", "")
        + "GST data needed;"
    )

    gts_requested = selected_active_view.loc[
        (selected_active_view["status"].str.contains("GST data needed;") == True)
    ]
    output += output_msg("Materials needing GTS in log:")
    output += output_msg(len(gts_requested))

    # MATNRs LOCAL NEEDED
    done_status = "|".join(["cancel", "complete", "on hold", "Localization required"])

    need_local = (
        (
            selected_active_view["MTART/GenItemCat"].isin(
                ["ZFG", "ZTG", "ZNFG", "ZRS1", "ZRS4"]
            )
        )
        & (selected_active_view["target plant"].isin(["5070"]))
        & (selected_active_view["target plant mrp type"].isin(["ND"]))
        & (
            (
                (
                    selected_active_view["status"].str.contains(done_status, case=False)
                    == False
                )
            )
            | (selected_active_view["status"].isna())
        )
    )

    selected_active_view.loc[need_local, "status"] = (
        selected_active_view["status"].astype(str).replace("nan", "")
        + "Localization required;"
    )

    local_requested = selected_active_view.loc[
        (selected_active_view["status"].str.contains("Localization required;") == True)
    ]
    output += output_msg("Materials needing LOCALIZATION in log:")
    output += output_msg(len(local_requested))

    # OUTPUTS
    status_output = selected_active_view["status"]

    pce_date_output = selected_active_view["PCE cert rev req'd"].map(
        format_pce_price_dates
    )
    price_date_output = selected_active_view["pricing request"].map(
        format_pce_price_dates
    )

    # TEST SAVE LOG
    populate_sheet_series(status_output, ws_active, 50, 2)
    populate_sheet_series(pce_date_output, ws_active, 49, 2)
    populate_sheet_series(price_date_output, ws_active, 48, 2)
    test_save(log, "TEST_pm_status")

    # ACTUAL
    if server == False:
        await_char(
            "y", "Press Y to save to live LOG file or C to cancel.", save_log, log
        )
    else:
        save_log(log)
        output += output_msg("LOG file saved")
        return Markup(output)
