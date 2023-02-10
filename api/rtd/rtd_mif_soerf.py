def rtd_mif_soerf():
    import os
    import pandas as pd
    import openpyxl

    from api.rtd.rtd_connector import connect_rtd, close_rtd
    from helpers.helpers import use_dotenv, use_logger, ignore_warnings
    from api.rtd.rts_sample_data import matnrs as ext_reqs

    use_dotenv()
    use_logger()
    ignore_warnings()

    con, cur = connect_rtd()

    def script(requests):
        # CLEAR TABLE
        cur.execute("TRUNCATE TABLE AP_MM_SERVICE")

        # INSERT NEW
        for req in requests:
            cur.execute(
                "insert into AP_MM_SERVICE values (:plant, :sorg, :req, :nr, :serv)",
                [req[0], req[1], req[2], req[3], req[4]],
            )
        cur.execute("COMMIT")

        # PREAPRE
        with open(os.path.join("sql", "prepare.sql"), "r") as f:
            prep = f.read()
        with open(os.path.join("sql", "prepare2.sql"), "r") as f:
            prep2 = f.read()
        cur.execute(prep)
        cur.execute("COMMIT")
        prep2_list = prep2.split(";")
        for q in prep2_list:
            q.replace(";", "")
            cur.execute(q)
        cur.execute("COMMIT")

        # MIF
        with open(os.path.join("sql", "mif.sql"), "r") as f:
            mif_sql = f.read()

        df = pd.read_sql_query(mif_sql, con)
        mif_xlsx = os.path.join(os.environ["DIR_OUT"], "TEST_MIF.xlsx")
        mif_xls = os.path.join(os.environ["DIR_OUT"], "TEST_MIF.xls")
        df.to_excel(mif_xlsx, index=False)
        # wb = openpyxl.load_workbook(mif_xlsx)
        # wb.save(mif_xls)

        log_mif = df[["MATERIAL", "PLANT"]]
        log_mif.to_excel(
            os.path.join(os.environ["DIR_OUT"], "TEST_LOG_MIF.xlsx"), index=False
        )

        # SOERF
        with open(os.path.join("sql", "soerf.sql"), "r") as f:
            soerf_sql = f.read()

        df = pd.read_sql_query(soerf_sql, con)
        soerf_xlsx = os.path.join(os.environ["DIR_OUT"], "TEST_SOERF.xlsx")
        soerf_xls = os.path.join(os.environ["DIR_OUT"], "TEST_SOERF.xls")
        df.to_excel(soerf_xlsx, index=False)
        # wb = openpyxl.load_workbook(soerf_xlsx)
        # wb.save(soerf_xls)

        log_soerf = df[["MATERIAL", "CATALOG_NO", "SALES_ORG"]]
        log_soerf.to_excel(
            os.path.join(os.environ["DIR_OUT"], "TEST_LOG_SOERF.xlsx"), index=False
        )

        # CACNEL
        with open(os.path.join("sql", "cancel.sql"), "r") as f:
            cancel_sql = f.read()

        df = pd.read_sql_query(cancel_sql, con)
        cancel_xlsx = os.path.join(os.environ["DIR_OUT"], "TEST_CANCEL.xlsx")
        df.to_excel(cancel_xlsx, index=False)

    script(ext_reqs)

    close_rtd(con, cur)
