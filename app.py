import os
from flask import Flask, render_template

from utility.check_daily_report import check_daily_report
from utility.clean_desktop import clean_desktop
from utility.mif_soerf_check import mif_soerf_check

from scripts.pm_emails import pm_emails
from scripts.pm_status import pm_status
from scripts.am_emails import am_emails
from scripts.am_status import am_status
from scripts.mif_soerf import mif_soerf
from scripts.requests import requests
from scripts.proc_sap_data import proc_sap_data
from scripts.sap_data import get_sap_data

server = True

app = Flask(__name__)

# HOME ROUTE


@app.route("/")
def r_index():
    return render_template('index.html')

# UTILITY ROUTES


@app.route("/check_daily_report")
def r_check_daily_report(script='Check for daily report uploaded to Sharepoint'):
    output = check_daily_report(server)
    return render_template('output.html', script=script, output=output)


@app.route("/clean_desktop")
def r_clean_desktop(script='Clean working folder & archive request files'):
    output = clean_desktop(server)
    return render_template('output.html', script=script, output=output)


@app.route("/mif_soerf_check")
def r_mif_soerf_check(script='Check for MIF/SOERF submitted'):
    output = mif_soerf_check(server)
    return render_template('output.html', script=script, output=output)


@app.route("/open_sap")
def r_open_sap():
    os.system(r'C:\RA-Apps\AP-Proc\sap\sap.ahk')
    return render_template('index.html')

# DATA ROUTES


@app.route("/get_sap_data")
def r_get_sap_data(script='Download SAP Data'):
    output = get_sap_data(server)
    return render_template('output.html', script=script, output=output)


@app.route("/proc_sap_data")
def r_proc_sap_data(script='Bring SAP Data'):
    output = proc_sap_data(server)
    return render_template('output.html', script=script, output=output)


# SCRIPT ROUTES
@app.route("/requests")
def r_requests(script='Get current requests'):
    output = requests(server)
    return render_template('output.html', script=script, output=output)


@app.route("/mif_soerf")
def r_mif_soerf(script='Generate MIF / SOERF requests'):
    output = mif_soerf(server)
    return render_template('output.html', script=script, output=output)


@app.route("/am_status")
def r_am_status(script='Update Material Statuses pre MM'):
    output = am_status(server)
    return render_template('output.html', script=script, output=output)


@app.route("/am_emails")
def r_am_emails(script='Generate AM Price & PCE requests'):
    output = am_emails(server)
    return render_template('output.html', script=script, output=output)


@app.route("/pm_status")
def r_pm_status(script='Update Material Statuses post MM Extension'):
    output = pm_status(server)
    return render_template('output.html', script=script, output=output)


@app.route("/pm_emails")
def r_pm_emails(script='Generate PM CCC, Localization & GTS Requests'):
    output = pm_emails(server)
    return render_template('output.html', script=script, output=output)


# SYS ROUTES
@app.route("/update")
def r_update():
    os.system('git pull')
    return render_template('index.html')
