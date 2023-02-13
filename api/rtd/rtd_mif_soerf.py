def rtd_mif_soerf(requests):
    import os
    import pandas as pd

    from api.rtd.rtd_connector import connect_rtd, close_rtd
    from helpers.helpers import use_dotenv, use_logger, ignore_warnings

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
    with open(os.path.join("sql", "prepare.sql"), "r") as f:
        prep = f.read()
    cur.execute(prep)
    cur.execute("COMMIT")
    with open(os.path.join("sql", "delete1.sql"), "r") as f:
        del1 = f.read()
    cur.execute(del1)
    with open(os.path.join("sql", "delete2.sql"), "r") as f:
        del2 = f.read()
    cur.execute(del2)
    with open(os.path.join("sql", "delete3.sql"), "r") as f:
        del3 = f.read()
    cur.execute(del3)
    cur.execute("COMMIT")

    # MIF
    with open(os.path.join("sql", "mif.sql"), "r") as f:
        mif_sql = f.read()
    df_mif = pd.read_sql_query(mif_sql, con)
    df_log_mif = df_mif[["MATERIAL", "PLANT"]]

    # SOERF
    with open(os.path.join("sql", "soerf.sql"), "r") as f:
        soerf_sql = f.read()
    df_soerf = pd.read_sql_query(soerf_sql, con)
    df_log_soerf = df_soerf[["MATERIAL", "CATALOG_NO", "SALES_ORG"]]

    # CANCEL
    with open(os.path.join("sql", "cancel.sql"), "r") as f:
        cancel_sql = f.read()
    df_log_cancel = pd.read_sql_query(cancel_sql, con)

    close_rtd(con, cur)

    return df_mif, df_log_mif, df_soerf, df_log_soerf, df_log_cancel
