def proc_sap_data(server=False):
    import pandas as pd
    import os

    from helpers.helpers import (
        use_dotenv,
        ignore_warnings,
        use_logger,
        end_script,
    )
    from helpers.log import load_log, save_log
    from helpers.xlsm import populate_sap_data_sheet, extend_concats
    import helpers.prompts as pr
    from state.output import output
    from state.table import (
        tbl_text,
        tbl_mara,
        tbl_marc,
        tbl_mvke,
        tbl_ausp,
        tbl_mlan,
        tbl_price,
        tbl_gts,
        tables,
    )

    use_dotenv()
    use_logger()
    ignore_warnings()

    output.reset()

    log = load_log()
    if log:
        # ASSING WORKSHEETS
        ws_mara = log["mara"]
        ws_marc = log["marc"]
        ws_mvke = log["mvke"]
        ws_ausp = log["ausp"]
        ws_mlan = log["mlan"]
        ws_price = log["ZZ_MATPRC_HIST"]
        ws_gts = log["gts"]
        ws_text = log["sales text"]
        # ws_list = [ws_mara, ws_marc, ws_mvke, ws_ausp,
        #            ws_mlan, ws_price, ws_gts, ws_text]

        # # clean out data
        output.add(f"{pr.info}Truncating data")
        ws_mara.delete_rows(100, ws_mara.max_row)
        ws_marc.delete_rows(100, ws_mara.max_row)
        ws_mvke.delete_rows(100, ws_mara.max_row)
        ws_ausp.delete_rows(100, ws_mara.max_row)
        ws_mlan.delete_rows(100, ws_mara.max_row)
        ws_price.delete_rows(100, ws_mara.max_row)
        ws_gts.delete_rows(100, ws_mara.max_row)
        ws_text.delete_rows(100, ws_mara.max_row)

        # DEFINE DATA FILES
        for t in tables:
            t.load()
        mara = tbl_mara.data()
        marc = tbl_marc.data()
        mvke = tbl_mvke.data()
        ausp = tbl_ausp.data()
        mlan = tbl_mlan.data()
        price = tbl_price.data()
        gts = tbl_gts.data()
        text = tbl_text.data()

        inputs_list = [mara, marc, mvke, ausp, mlan, price, gts, text]

        # FUNCTIONS
        inputs_not_empty = 0
        for input in inputs_list:
            if not input.empty:
                inputs_not_empty += 1

        if inputs_not_empty == 8:
            # TODO: price[Valid to] is a long date and needs to be format different
            # just now it returning blank rows
            mvke["VMSTD"] = pd.to_datetime(mvke["VMSTD"], errors="coerce").dt.strftime(
                "%d-%m-%Y"
            )
            price["Valid to"] = pd.to_datetime(
                price["Valid to"], errors="coerce"
            ).dt.strftime("%d-%m-%Y")
            price["Valid From"] = pd.to_datetime(
                price["Valid From"], errors="coerce"
            ).dt.strftime("%d-%m-%Y")

            output.add(f"{pr.info}Populate new data")
            populate_sap_data_sheet(
                mara,
                ws_mara,
            )
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
            save_log(log)

        else:
            output.add(f"Missing {8 - inputs_not_empty} SAP data inputs")

    return end_script(server)
