from flask import Flask, render_template

import scripts.requests as requests
import scripts.mif_soerf as mif_soerf
import scripts.am_status as am_status
import scripts.am_emails as am_emails
import scripts.pm_status as pm_status
import scripts.pm_emails as pm_emails

from utility.check_mif_soerf import check_mif_soerf
import utility.clean_desktop as clean_desktop
import utility.check_daily_report as daily_report_check
import utility.sap_data as sap_data

server = True

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/ms_check")
def mf_check():
    check_mif_soerf(server)
    return render_template('ms_check.html')
