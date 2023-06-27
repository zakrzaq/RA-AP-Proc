import os
import sys

from utility.check_daily_report import check_daily_report
from utility.clean_desktop import clean_desktop
from utility.mif_soerf_check import mif_soerf_check

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

from utils.helpers import use_logger, clear
from utils.startup import check_process_files

use_logger()
check_process_files()

if sys.argv[1] in ["test"]:
    server = False
if sys.argv[1] in ["prod", "server"]:
    server = True
else:
    server = False


table_names = ["mara", "marc", "mvke", "ausp", "mlan", "price", "gts", "sales_text"]

clear()


def get_menu_choice():
    def print_menu():  # Your menu design here
        print(20 * "-", "AP MM EXTENSION PROCESS", 20 * "-")
        print("1)    Get current requests")
        print("2)    Generate MIF / SOERF requests")
        print("3)    Update Material Statuses pre MM")
        print("4)    Generate AM Price & PCE requests")
        print(70 * "-")
        print("5)    Reconcile PCE / Update ORG Source")
        print("6)    Update Material Statuses post MM Extension")
        print("7)    Generate PM CCC, Localization & GTS Requests")
        print(70 * "-")
        print("8)    DATA: Download SAP Data")
        print("9)    DATA: Bring SAP Data")
        print(70 * "-")
        print("10)   UTILITY: Clean working folder & archive request files")
        print("11)   UTILITY: Check for MIF/SOERF submitted")
        print("12)   UTILITY: Check for daily report uploaded to Sharepoint Rep")
        print("13)   UTILITY: Open SAP Instance")
        print("14)   UTILITY: Open AP LOG file")
        print(70 * "-")
        print("tbl)  UTILITY: SAP data from table")
        print(70 * "-")
        print("U)    Update program")
        print("X)    Close program")
        print(70 * "=")

    loop = True

    while loop:  # While loop which will keep going until loop = False
        print_menu()  # Displays menu
        choice = input("Choose procedure to run: ")
        print("\n")

        if choice == "1":
            get_requests(server)
            clear()
        elif choice == "2":
            mif_soerf(server)
            clear()
        elif choice == "3":
            am_status(server)
            clear()
        elif choice == "4":
            am_emails(server)
            clear()
        elif choice == "5":
            reconcile_pce(server)
            clear()
        elif choice == "6":
            pm_status(server)
            clear()
        elif choice == "7":
            pm_emails(server)
            clear()
        elif choice == "8":
            get_sap_data(server)
            clear()
        elif choice == "9":
            proc_sap_data(server)
            clear()
        elif choice == "10":
            clean_desktop(server)
            clear()
        elif choice == "11":
            mif_soerf_check(server)
            clear()
        elif choice == "12":
            check_daily_report(server)
            clear()
        elif choice == "13":
            os.system(r"C:\RA-Apps\AP-Proc\sap\sap.ahk")
            clear()
        elif choice == "14":
            os.system(r"C:\RA-Apps\AP-Proc\sap\log.ahk")
            clear()
        elif choice == "u" or choice == "U":
            os.system("git pull")
            clear()
        elif choice == "u" or choice == "U":
            os.system("git pull")
            clear()
        elif choice == "x" or choice == "X":
            loop = False
            break
        elif choice in table_names:
            print(choice)
            single_sap_data(choice)
            clear()
        else:
            input("Wrong menu selection. Enter any key to try again...")
            clear()


print(get_menu_choice())
