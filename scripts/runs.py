import pandas as pd
import os
import time

from scripts.requests import get_requests
from scripts.sap_data import get_sap_data
from scripts.mif_soerf import mif_soerf
from scripts.reconcile_pce import reconcile_pce
from scripts.am_status import am_status
from scripts.pm_status import pm_status
from scripts.am_emails import am_emails
from scripts.pm_emails import pm_emails

from helpers.ap_data import make_ap_data
from helpers.data_frames import get_active_requests
from helpers.ap_data import get_ext_cancelled
from helpers.xlsm import populate_sap_data_sheet, get_last_row
from helpers.log import load_log
from helpers.files import sap_data_files


def is_file(file_path):
    os.path.exists(file_path)


def am_run(server=False):
    server = server
    get_requests(server)
    get_sap_data(server)
    mif_soerf(server)
    current_data = get_active_requests()
    sea_hubs, kmats = get_ext_cancelled()
    load = current_data + sea_hubs
    log_data = make_ap_data(load)

    log = load_log()
    if log:
        ws_active = log["Active Materials"]
        df = pd.DataFrame(log_data)
        df = df.iloc[:, 1:]
        populate_sap_data_sheet(df, ws_active, start_col=2, start_row=2)
        # TODO! put data_load to Log File

        # am_status(server)
        # am_emails(server)


def pm_run(server=False):
    # reconcile_pce(server)
    get_sap_data(server, mode="refresh")
    # TODO: step pit out / wait for completion
    while (
        not is_file(sap_data_files["text"])
        or not is_file(sap_data_files["marc"])
        or not is_file(sap_data_files["mvke"])
        or not is_file(sap_data_files["ausp"])
    ):
        time.sleep(1)
    current_data = get_active_requests()
    log_data = make_ap_data(current_data)

    log = load_log()
    if log:
        ws_active = log["Active Materials"]
        df = pd.DataFrame(log_data)
        df = df.iloc[:, 1:]
        row = get_last_row(ws_active, "A")
        populate_sap_data_sheet(df, ws_active, start_col=2, start_row=row)

        pm_status(server)
        pm_emails(server)