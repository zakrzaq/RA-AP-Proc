import json

from api.apmm.apmm_connector import con_apmm, close_apmm


sql_queries = {"select_all": """SELECT * FROM full;"""}


def get_json_data(query):
    con, cur = con_apmm()
    if con and cur:
        cur.execute(sql_queries[query])
        data = cur.fetchall()
        col_names = [i[0] for i in cur.description]
        result = []
        for r in data:
            row = {}
            for index, value in enumerate(r):
                row[col_names[index]] = value
            result.append(row)

        return json.dumps(result, indent=4)
