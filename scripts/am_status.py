from markupsafe import Markup

from helpers.log import load_log, save_log, test_save
from helpers.xlsm import populate_sheet_series
from helpers.helpers import (
    await_char,
    use_dotenv,
    ignore_warnings,
    use_logger,
    output_msg,
    format_pce_price_dates,
)
from helpers.datetime import today_ymd
from helpers.data_frames import get_selected_active


def am_status(server=False):
    use_dotenv()
    use_logger()
    ignore_warnings()

    output = ""
    today = today_ymd()[-5:]

    # LOAD LOG
    try:
        log = load_log()
        ws_active = log["Active Materials"]
        selected_active_view = get_selected_active()
        if selected_active_view.empty:
            output += output_msg("Unable to obtaind data from LOG")
            return Markup(output)
        else:
            output += output_msg("LOG data loaded")
    except:
        if server == False:
            await_char(
                "y",
                "Unable to load AP LOG, please close the excel file and press Y to continue",
            )
        else:
            output += output_msg(
                "Unable to load AP LOG, please close the excel file.", "red"
            )
            return Markup(output)

    # MATNRs PRICE NEEDED
    need_price = (
        (selected_active_view["target sorg price"].isna())
        & (~selected_active_view["SOERF Submitted"].isna())
        & (selected_active_view["target sorg price"].isna())
        & (
            (
                selected_active_view["status"].str.contains(
                    "cancel|complete|on hold|needs price;", case=False
                )
                == False
            )
            | (selected_active_view["status"].isnull())
        )
    )

    selected_active_view.loc[need_price, "status"] = (
        selected_active_view["status"].astype(str).replace("nan", "") + "needs price;"
    )
    selected_active_view.loc[need_price, "pricing request"] = str(today)

    price_requested = selected_active_view.loc[
        (selected_active_view["status"].str.contains("needs price;") == True)
    ]
    output += output_msg(f"Materials NEEDING PRICE in AP LOG: {len(price_requested)}")

    # MATNRs PCE NEEDED
    done_status = "|".join(["cancel", "complete", "on hold", "pending PCE review"])
    prod_cert = (
        selected_active_view["Service Requested\n(from request form)"]
        == "Product Certification Review"
    ) & (
        (
            (
                selected_active_view["status"].str.contains(done_status, case=False)
                == False
            )
        )
        | (selected_active_view["status"].isna())
    )

    certs = "|".join(["BIS", "BSMI", "CCC", "KC", "RCM"])
    allowed_mtart = "|".join(["ZFG", "ZTG", "ZRS1", "ZRS4", "ZRS5"])
    need_pce = (
        (selected_active_view["Regulatory Cert\n(Z62 Class)"].str.contains(certs))
        & (selected_active_view["Z62 characteristic\n(assigned in SAP)"].isna())
        & (selected_active_view["MTART/GenItemCat"].str.contains(allowed_mtart))
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

    selected_active_view.loc[need_pce, "status"] = (
        selected_active_view["status"].astype(str).replace("nan", "")
        + "pending PCE review;"
    )
    selected_active_view.loc[need_pce, "PCE cert rev req'd"] = today

    selected_active_view.loc[prod_cert, "status"] = (
        selected_active_view["status"].astype(str).replace("nan", "")
        + "pending PCE review;"
    )

    selected_active_view.loc[prod_cert, "PCE cert rev req'd"] = str(today)

    pce_requested = selected_active_view.loc[
        (selected_active_view["status"].str.contains("pending PCE review;") == True)
    ]
    output += output_msg(f"Materials NEEDING PCE in AP LOG: {len(pce_requested)}")

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
    test_save(log, "TEST_am_status")
    # ACTUAL
    if server == False:
        await_char(
            "y", "Press Y to save to live LOG file or C to cancel.", save_log, log
        )
    else:
        save_log(log)
        output += output_msg("LOG file saved")
        return Markup(output)
