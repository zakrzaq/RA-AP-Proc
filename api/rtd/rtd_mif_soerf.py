def rtd_mif_soerf(requests):
    import pandas as pd

    from api.rtd.rtd_connector import connect_rtd, close_rtd
    from utils.helpers import (
        use_dotenv,
        use_logger,
        ignore_warnings,
        get_dictionary_value,
    )
    from data.files import rtd_sql

    # from api.rtd.rts_sample_data import matnrs as requests  # SAMPLE DATA

    use_dotenv()
    use_logger()
    ignore_warnings()

    """
    SEQUENCE OF SQL EVENTS / FILES
    1. TRUNCATE TABLE
    2. INSERT STATEMENT
    3. COMMIT
    4. prepare.sql
    5. delete1/delete2/delete3.sql
    6. COMMIT
    7. mif.sql
    8. soerf.sql
    9. cancel.sql
    """

    # CONNECT RTD DB
    con, cur = connect_rtd()
    if con and cur:
        # CLEAR TABLE
        cur.execute("TRUNCATE TABLE AP_MM_SERVICE")

        # INSERT NEW
        for req in requests:
            cur.execute(
                "insert into AP_MM_SERVICE values (:plant, :sorg, :req, :nr, :serv)",
                [req[0], req[1], req[2], req[3], req[4]],
            )
        cur.execute("COMMIT")

        # PREPARE
        with open(get_dictionary_value(rtd_sql, "name", "prepare", "path"), "r") as f:
            prep = f.read()
        cur.execute(prep)
        cur.execute("COMMIT")
        with open(get_dictionary_value(rtd_sql, "name", "delete1", "path"), "r") as f:
            del1 = f.read()
        cur.execute(del1)
        with open(get_dictionary_value(rtd_sql, "name", "delete2", "path"), "r") as f:
            del2 = f.read()
        cur.execute(del2)
        with open(get_dictionary_value(rtd_sql, "name", "delete3", "path"), "r") as f:
            del3 = f.read()
        cur.execute(del3)
        cur.execute("COMMIT")

        # MIF
        with open(get_dictionary_value(rtd_sql, "name", "mif", "path"), "r") as f:
            mif_sql = f.read()
        df_mif = pd.read_sql_query(mif_sql, con)  # type: ignore
        df_log_mif = df_mif[["MATERIAL", "PLANT"]]

        # SOERF
        with open(get_dictionary_value(rtd_sql, "name", "soerf", "path"), "r") as f:
            soerf_sql = f.read()
        df_soerf = pd.read_sql_query(soerf_sql, con)  # type: ignore
        df_log_soerf = df_soerf[["MATERIAL", "CATALOG_NO", "SALES_ORG"]]

        # CANCEL
        with open(get_dictionary_value(rtd_sql, "name", "cancel", "path"), "r") as f:
            cancel_sql = f.read()
        df_log_cancel = pd.read_sql_query(cancel_sql, con)  # type: ignore

        close_rtd(con, cur)

        return df_mif, df_log_mif, df_soerf, df_log_soerf, df_log_cancel
