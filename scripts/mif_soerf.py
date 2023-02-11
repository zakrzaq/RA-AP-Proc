def mif_soerf(server=False):
    import pandas as pd
    import os
    from markupsafe import Markup

    from helpers.helpers import (
        use_dotenv,
        ignore_warnings,
        await_char,
        use_logger,
        output_msg,
    )
    from helpers.data_frames import get_selected_active
    from api.rtd.rtd_mif_soerf import rtd_mif_soerf
    from helpers.log import load_log, test_save, save_log
    from helpers.xlsm import populate_sap_data_sheet, extend_concats
    from helpers.datetime import today_dmy

    use_dotenv()
    use_logger()
    ignore_warnings()

    today_dmy = today_dmy()
    selected_active_view = get_selected_active()
    output = ""

    # MIF / SOERF needed
    output += output_msg("Generating materials needing extension")
    mif_soerf_view = selected_active_view[
        [
            "Date Added",
            "target sorg",
            "target plant",
            "email prefix\n(from request form)",
            "SAP MATNR\n(from request form)",
            "Service Requested\n(from request form)",
        ]
    ]

    mif_soerf = mif_soerf_view.loc[
        (
            (
                selected_active_view["status"].str.contains(
                    "cancel|complete", case=False
                )
                == False
            )
            | selected_active_view["status"].isna()
        )
        & (
            selected_active_view["Service Requested\n(from request form)"].isin(
                [
                    "Plant and sales org extension",
                    "Plant extension",
                    "Sales org extension",
                ]
            )
        )
        & (selected_active_view["mif/soerf check"].isin(["X"]))
        & (selected_active_view["MTART/GenItemCat"].isin(["ZTG", "ZFG"]))
    ]
    output += output_msg("Complete")

    # PREPARE REQUEST DATA
    output += output_msg("Preparing RTD input data")
    mif_soerf_data = []
    for index, row in mif_soerf.iterrows():
        item = []
        for x in row:
            item.append(x)
        mif_soerf_data.append(item)
    output += output_msg("Complete")

    # OBTAIN DATE FROM RTD DB
    output += output_msg("Downloading data from RTD")
    df_mif, df_log_mif, df_soerf, df_log_soerf, df_log_cancel = rtd_mif_soerf(
        mif_soerf_data
    )
    output += output_msg("Complete")

    # OUTPUT MIF & SOERF
    if not df_mif.empty:
        output += output_msg("Saving MIF to OUTPUT DIR")
        mif_xlsx = os.path.join(os.environ["DIR_OUT"], "AP_MIF.xlsx")
        df_mif.to_excel(mif_xlsx, index=False)
        output += output_msg("Complete")
    else:
        output += output_msg("NO MIFs TO GENERATE MIF FILE")

    if not df_soerf.empty:
        output += output_msg("Saving SOERF to OUTPUT DIR")
        soerf_xlsx = os.path.join(os.environ["DIR_OUT"], "AP_SOERF.xlsx")
        df_soerf.to_excel(soerf_xlsx, index=False)
        output += output_msg("Complete")
    else:
        output += output_msg("NO MIFs TO GENERATE MIF FILE")

    # HANDLE LOG INPUTS FOR MIF, SOERF & CANCEL
    output += output_msg("Loading load file to update mif & soerf data")
    log = load_log()

    if not df_log_mif.empty:
        output += output_msg("Processing mif data to log")
        ws_mif = log["mif"]
        mif_last_row = ws_mif.max_row + 1
        ws_mif[f"D{mif_last_row}"] = today_dmy
        populate_sap_data_sheet(df_log_mif, ws_mif, 0, mif_last_row)
        extend_concats(ws_mif, mif_last_row - 1, "C")
        extend_concats(ws_mif, mif_last_row, "d")
    else:
        output += output_msg("No mifs to process")

    if not df_log_soerf.empty:
        output += output_msg("Processing soerf data to log")
        ws_soerf = log["soerf"]
        soerf_last_row = ws_soerf.max_row + 1
        ws_soerf[f"E{soerf_last_row}"] = today_dmy
        populate_sap_data_sheet(df_log_soerf, ws_soerf, 0, soerf_last_row)
        extend_concats(ws_soerf, soerf_last_row - 1, "D")
        extend_concats(ws_soerf, soerf_last_row, "E")
        output += output_msg("Complete")
    else:
        output += output_msg("No soerfs to process")

    if not df_log_cancel.empty:
        output += output_msg("Saving cancelled extension to output folder")
        df_log_cancel.to_csv(
            os.path.join(os.environ["DIR_OUT"], "AP_CANCEL.txt"), index=False, sep="\t"
        )
        output += output_msg("Complete")
    else:
        output += output_msg("No cancelled extensions to process")

    # SAVE / END
    if server == False:
        test_save(log, "TEST_AP_LOG")
        df_log_mif.to_excel(
            os.path.join(os.environ["DIR_OUT"], "TEST_LOG_MIF.xlsx"), index=False
        )
        df_log_soerf.to_excel(
            os.path.join(os.environ["DIR_OUT"], "TEST_LOG_SOERF.xlsx"), index=False
        )
        await_char()
    else:
        return Markup(output)
