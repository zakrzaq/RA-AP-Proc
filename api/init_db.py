def init_db():
    import os
    import sqlite3
    import pandas as pd

    from helpers.db import con_db, close_db

    con, cur = con_db()

    sql_dir = os.path.join(os.getcwd(), 'api', 'sql')

    with open(os.path.join(sql_dir, 'create_mara.sql')) as f:
        con.executescript(f.read())

    cur = con.cursor()

    mara_f = os.path.join(os.getcwd(), 'INPUTS', 'mara.XLSX')
    mara = pd.read_excel(mara_f)

    mara.to_sql('mara', con, if_exists='replace', index=False)

    all = cur.execute("SELECT * FROM mara").fetchall()
    for r in all:
        print(r[0:5])

    close_db(con)
