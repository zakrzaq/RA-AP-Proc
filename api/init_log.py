import os
import pandas as pd

sql_dir = os.path.join(os.getcwd(), 'api', 'sql')


def init_log():

    from helpers.db import con_db, close_db

    con, cur = con_db()

    log = pd.read_excel(os.path.join(os.getcwd(), 'log.xlsx'))

    with open(os.path.join(sql_dir, 'create_log.sql')) as f:
        con.executescript(f.read())
    log.to_sql('log', con, if_exists='replace', index=False)
    con.commit()

    with open(os.path.join(sql_dir, 'drop_log_view.sql')) as f:
        con.executescript(f.read())

    log_view = cur.execute(
        '''
        CREATE VIEW log_view
        AS
        SELECT 
            "Active", 
            "Date Added", 
            "target sorg",
            "target plant",
            "email prefix (from request form)",
            "SAP MATNR (from request form)",
            "Service Requested (from request form)",
            "Location (from request form)",
            price.Amount
        FROM log
        LEFT JOIN price ON
            log.[SAP MATNR (from request form)] = price.Material AND
            log.[target sorg] = price.[SOrg.]
        ''').fetchall()

    for row in log_view:
        print(row[0:15])

    close_db(con)
