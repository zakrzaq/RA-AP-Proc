from flask import Blueprint, render_template, redirect, request

from scripts.pm_emails import pm_emails
from scripts.pm_status import pm_status
from scripts.am_emails import am_emails
from scripts.am_status import am_status
from scripts.mif_soerf import mif_soerf
from scripts.requests import get_requests
from scripts.reconcile_pce import reconcile_pce
from scripts.proc_sap_data import proc_sap_data
from scripts.sap_data import get_sap_data
from scripts.single_sap_data import single_sap_data
from sap.open import open_sap

from utility.check_daily_report import check_daily_report
from utility.clean_desktop import clean_desktop
from utility.mif_soerf_check import mif_soerf_check
server = True


client_routes = Blueprint('routes', __name__)

# HOME ROUTE


@client_routes.route("/")
def r_index():
    return render_template("index.html")


# UTILITY ROUTES


@client_routes.route("/check_daily_report")
def r_check_daily_report(script="Check for daily report uploaded to Sharepoint"):
    output = check_daily_report(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/clean_desktop")
def r_clean_desktop(script="Clean working folder & archive request files"):
    output = clean_desktop(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/mif_soerf_check")
def r_mif_soerf_check(script="Check for MIF/SOERF submitted"):
    output = mif_soerf_check(server)
    return render_template("index.html", script=script, output=output)


# DATA ROUTES


@client_routes.route("/get_sap_data")
def r_get_sap_data(script="Download SAP Data"):
    output = get_sap_data(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/proc_sap_data")
def r_proc_sap_data(script="Bring SAP Data"):
    output = proc_sap_data(server)
    return render_template("index.html", script=script, output=output)


# SCRIPT ROUTES
@client_routes.route("/requests")
def r_requests(script="Get current requests"):
    output = get_requests(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/mif_soerf")
def r_mif_soerf(script="Generate MIF / SOERF requests"):
    output = mif_soerf(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/am_status")
def r_am_status(script="Update Material Statuses pre MM"):
    output = am_status(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/am_emails")
def r_am_emails(script="Generate AM Price & PCE requests"):
    output = am_emails(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/reconcile_pce")
def r_reconcile_pce(script="Reconcile PCE / Update ORG Source"):
    output = reconcile_pce(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/pm_status")
def r_pm_status(script="Update Material Statuses post MM Extension"):
    output = pm_status(server)
    return render_template("index.html", script=script, output=output)


@client_routes.route("/pm_emails")
def r_pm_emails(script="Generate PM CCC, Localization & GTS Requests"):
    output = pm_emails(server)
    return render_template("index.html", script=script, output=output)


# SYS ROUTES
@client_routes.route("/update")
def r_update():
    os.system("git pull")
    return render_template("index.html")


@client_routes.route("/open_sap")
def r_open_sap():
    open_sap()
    return render_template("index.html")


@client_routes.route("/open_log")
def r_open_log():
    os.system(r"C:\RA-Apps\AP-Proc\sap\log.ahk")
    return redirect("/")


# SINGLE SAP DATA ROUTES
@client_routes.route("/single_sap")
def single_sap(script="Single Table SAP data"):
    table = request.args.get("table")
    print(table)
    output = single_sap_data(table, server)
    return render_template("index.html", script=script, output=output)

