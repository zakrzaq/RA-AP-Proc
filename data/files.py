import os
from utils.helpers import use_dotenv


use_dotenv()

sap_data_files = {
    "mara": os.path.join(os.environ["DIR_IN"], "MARA.XLSX"),
    "marc": os.path.join(os.environ["DIR_IN"], "MARC.XLSX"),
    "mvke": os.path.join(os.environ["DIR_IN"], "MVKE.XLSX"),
    "ausp": os.path.join(os.environ["DIR_IN"], "AUSP.XLSX"),
    "mlan": os.path.join(os.environ["DIR_IN"], "MLAN.XLSX"),
    "gts": os.path.join(os.environ["DIR_IN"], "GTS.XLSX"),
    "price": os.path.join(os.environ["DIR_IN"], "PRICE.XLSX"),
    "text": os.path.join(os.environ["DIR_IN"], "sales_text.XLS"),
}

process_files = [
    {"name": "dir_in", "path": os.environ["DIR_IN"], "type": "dir", "create": True},
    {"name": "dir_out", "path": os.environ["DIR_OUT"], "type": "dir", "create": True},
    {
        "name": "edm_drive",
        "path": os.environ["EDM_DRIVE"],
        "type": "dir",
        "create": False,
    },
    {"name": "dir_log", "path": os.environ["DIR_LOG"], "type": "dir", "create": True},
    {"name": "ap_log", "path": os.environ["AP_LOG"], "type": "file", "create": False},
    {
        "name": "f_log",
        "path": os.path.join(os.environ["DIR_LOG"], "log.txt"),
        "type": "file",
        "create": True,
    },
]

dir_rtd_sql = os.path.join("sql", "rtd")
rtd_sql = [
    {"name": "prepare", "path": os.path.join(dir_rtd_sql, "prepare.sql")},
    {"name": "delete1", "path": os.path.join(dir_rtd_sql, "delete1.sql")},
    {"name": "delete2", "path": os.path.join(dir_rtd_sql, "delete2.sql")},
    {"name": "delete3", "path": os.path.join(dir_rtd_sql, "delete3.sql")},
    {"name": "mif", "path": os.path.join(dir_rtd_sql, "mif.sql")},
    {"name": "soerf", "path": os.path.join(dir_rtd_sql, "soerf.sql")},
    {"name": "cancel", "path": os.path.join(dir_rtd_sql, "cancel.sql")},
]

dir_apmm_dev_sql = os.path.join("sql", "apmm", "dev")
apmm_dev_sql = [
    {"name": "create_log", "path": os.path.join(dir_rtd_sql, "create_log.sql")},
    {
        "name": "create_log_view",
        "path": os.path.join(dir_rtd_sql, "create_log_view.sql"),
    },
    {"name": "drop_log_view", "path": os.path.join(dir_rtd_sql, "drop_log_view.sql")},
]
