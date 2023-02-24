def mif_soerf(server=False):
    import os
    from state.output import output

    from helpers.helpers import (
        use_dotenv,
        ignore_warnings,
        end_script,
        use_logger,
    )
    from helpers.data_frames import get_selected_active
    from api.rtd.rtd_mif_soerf import rtd_mif_soerf
    from helpers.log import load_log, save_log
    from helpers.xlsm import populate_sap_data_sheet, extend_concats, extend_values
    from helpers.datetime import today_dmy
    import helpers.prompts as pr
    from helpers.send_extensions import send_extensions

    use_dotenv()
    use_logger()
    ignore_warnings()

    today_dmy = today_dmy()
    output.reset()

    selected_active_view = get_selected_active()

    if not selected_active_view.empty:
        # MIF / SOERF needed
        output.add(f"{pr.info}Generating materials needing extension")
        mif_soerf_view = selected_active_view[
            [
                # "Date Added",
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
        output.add(f"{pr.done}Complete")

        # PREPARE REQUEST DATA
        output.add(f"{pr.info}Preparing RTD input data")
        mif_soerf_data = []
        for index, row in mif_soerf.iterrows():
            item = []
            for x in row:
                item.append(x)
            mif_soerf_data.append(item)
        output.add(f"{pr.done}Complete")

        # OBTAIN DATE FROM RTD DB
        output.add(f"{pr.info}Downloading data from RTD")
        df_mif, df_log_mif, df_soerf, df_log_soerf, df_log_cancel = rtd_mif_soerf(
            mif_soerf_data
        )
        output.add(f"{pr.done}Complete")

        # OUTPUT MIF & SOERF
        if not df_mif.empty:
            output.add(f"{pr.file}Saving MIF to OUTPUT DIR")
            mif_xlsx = os.path.join(os.environ["DIR_OUT"], "AP_MIF.xlsx")
            df_mif.to_excel(mif_xlsx, index=False)
            output.add(f"{pr.done}Complete")
        else:
            output.add(f"{pr.cncl}NO MIFs TO GENERATE MIF FILE")

        if not df_soerf.empty:
            output.add(f"{pr.info}Saving SOERF to OUTPUT DIR")
            soerf_xlsx = os.path.join(os.environ["DIR_OUT"], "AP_SOERF.xlsx")
            df_soerf.to_excel(soerf_xlsx, index=False)
            output.add(f"{pr.done}Complete")
        else:
            output.add(f"{pr.cncl}NO MIFs TO GENERATE MIF FILE")

        # HANDLE LOG INPUTS FOR MIF, SOERF & CANCEL
        output.add(f"{pr.info}Loading load file to update mif & soerf data")
        log = load_log()

        if not df_log_mif.empty:
            output.add(f"{pr.info}Processing mif data to log")
            ws_mif = log["mif"]
            mif_last_row = ws_mif.max_row + 1
            ws_mif[f"D{mif_last_row}"] = today_dmy
            populate_sap_data_sheet(df_log_mif, ws_mif, 1, mif_last_row)
            extend_concats(ws_mif, mif_last_row - 1, "C")
            extend_values(ws_mif, mif_last_row, "D")
        else:
            output.add(f"{pr.cncl}No mifs to process")

        if not df_log_soerf.empty:
            output.add(f"{pr.info}Processing soerf data to log")
            ws_soerf = log["soerf"]
            soerf_last_row = ws_soerf.max_row + 1
            ws_soerf[f"E{soerf_last_row}"] = today_dmy
            populate_sap_data_sheet(df_log_soerf, ws_soerf, 1, soerf_last_row)
            extend_concats(ws_soerf, soerf_last_row - 1, "D")
            extend_values(ws_soerf, soerf_last_row, "E")
            output.add(f"{pr.done}Complete")
        else:
            output.add(f"{pr.cncl}No soerfs to process")

        if not df_log_cancel.empty:
            output.add(f"{pr.file}Saving cancelled extension to output folder")
            df_log_cancel.to_csv(
                os.path.join(os.environ["DIR_OUT"], "AP_CANCEL.txt"),
                index=False,
                sep="\t",
            )
            output.add(f"{pr.done}Complete")
        else:
            output.add(f"{pr.cncl}No cancelled extensions to process")

        # SAVE / END
        if not df_log_mif.empty or not df_log_soerf.empty or not df_log_cancel.empty:
            save_log(log)

            # SEND EXTENSIONS TO EDM DRIVE
            send_extensions()

            if not server:
                df_log_mif.to_excel(
                    os.path.join(os.environ["DIR_OUT"], "TEST_LOG_MIF.xlsx"),
                    index=False,
                )
                df_log_soerf.to_excel(
                    os.path.join(os.environ["DIR_OUT"], "TEST_LOG_SOERF.xlsx"),
                    index=False,
                )

    return end_script(server)
