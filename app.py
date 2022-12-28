from flask import Flask, render_template

from scripts.sap_data import get_sap_data
from scripts.proc_sap_data import proc_sap_data
from scripts.requests import requests
from scripts.mif_soerf import mif_soerf
from scripts.am_status import am_status
from scripts.am_emails import am_emails
from scripts.pm_status import pm_status
from scripts.pm_emails import pm_emails

from utility.mif_soerf_check import mif_soerf_check
from utility.clean_desktop import clean_desktop
from utility.check_daily_report import check_daily_report

server = True

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/ms_check")
def mf_check():
    mif_soerf_check(server)
    return render_template('ms_check.html')
