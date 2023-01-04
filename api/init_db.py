from helpers.helpers import output_msg


def init_db():
    # import os
    # import pandas as pd

    from helpers.db import con_db, close_db

    con, cur = con_db()

    # sql_dir = os.path.join(os.getcwd(), 'api', 'sql')
    # with open(os.path.join(sql_dir, 'create_mara.sql')) as f:
    #     con.executescript(f.read())
    # mara_f = os.path.join(os.getcwd(), 'INPUTS', 'mara.XLSX')
    # mara = pd.read_excel(mara_f)
    # mara.to_sql('mara', con, if_exists='replace', index=False)

    mara = cur.execute("SELECT * FROM mara").fetchall()
    for row in mara:
        print(row[0:4])
    marc = cur.execute("SELECT * FROM marc").fetchall()
    for row in marc:
        print(row[0:4])
    mvke = cur.execute("SELECT * FROM mvke").fetchall()
    for row in mvke:
        print(row[0:4])
    ausp = cur.execute("SELECT * FROM ausp").fetchall()
    for row in ausp:
        print(row[0:4])
    mlan = cur.execute("SELECT * FROM mlan").fetchall()
    for row in mlan:
        print(row[0:4])
    gts = cur.execute("SELECT * FROM gts").fetchall()
    for row in gts:
        print(row[0:4])
    price = cur.execute("SELECT * FROM price").fetchall()
    for row in price:
        print(row[0:4])
    sales_text = cur.execute("SELECT * FROM sales_text").fetchall()
    for row in sales_text:
        print(row[0:4])

    close_db(con)
