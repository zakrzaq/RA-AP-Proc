import os
import platform

from utility.check_daily_report import check_daily_report
from utility.clean_desktop import clean_desktop
from utility.mif_soerf_check import mif_soerf_check

from scripts.pm_emails import pm_emails
from scripts.pm_status import pm_status
from scripts.am_emails import am_emails
from scripts.am_status import am_status
from scripts.mif_soerf import mif_soerf
from scripts.requests import requests
from scripts.reconcile_pce import reconcile_pce
from scripts.proc_sap_data import proc_sap_data
from scripts.sap_data import get_sap_data


import os
import platform
from helpers.helpers import use_logger

use_logger()


def clear():
    if platform.system() == 'Windows':
        return os.system('cls')
    else:
        return os.system('clear')


clear()


server = False


def get_menu_choice():
    def print_menu():       # Your menu design here
        print(30 * "-", "AP MM EXTENSION PROCESS", 30 * "-")
        print("1)    Get current requests")
        print("2)    Generate MIF / SOERF requests")
        print("3)    Update Material Statuses pre MM")
        print("4)    Generate AM Price & PCE requests")
        print("5)    Reconcile PCE / Update ORG Source")
        print("5)    Update Material Statuses post MM Extension")
        print("6)    Generate PM CCC, Localization & GTS Requests")
        print(85 * "-")
        print("8)    DATA: Download SAP Data")
        print("9)    DATA: Bring SAP Data")
        print(85 * "-")
        print("10)   UTILITY: Clean working folder & archive request files")
        print("11)   UTILITY: Check for MIF/SOERF submitted")
        print("12)   UTILITY: Check for daily report uploaded to Sharepoint Repository")
        print("13)   UTILITY: Open SAP Instance")
        print(85 * "-")
        print("U)    Update program")
        print("X)    Close program")
        print(85 * "=")

    loop = True

    while loop:          # While loop which will keep going until loop = False
        print_menu()    # Displays menu
        choice = input("Choose procedure to run: ")
        print("\n")

        if choice == '1':
            requests()
            clear()
        elif choice == '2':
            mif_soerf()
            clear()
        elif choice == '3':
            am_status()
            clear()
        elif choice == '4':
            am_emails()
            clear()
        elif choice == '5':
            reconcile_pce()
            clear()
        elif choice == '6':
            pm_status()
            clear()
        elif choice == '7':
            pm_emails()
            clear()
        elif choice == '8':
            get_sap_data()
            clear()
        elif choice == '9':
            proc_sap_data()
            clear()
        elif choice == '10':
            clean_desktop()
            clear()
        elif choice == '11':
            mif_soerf_check()
            clear()
        elif choice == '12':
            check_daily_report()
            clear()
        elif choice == '13':
            os.system(r'C:\RA-Apps\AP-Proc\sap\sap.ahk')
            clear()
        elif (choice == 'u' or choice == 'U'):
            os.system("git pull")
            clear()
        elif (choice == 'x' or choice == 'X'):
            print("Exiting...")
            loop = False
        else:
            # Any inputs other than values 1-4 we print an error message
            input("Wrong menu selection. Enter any key to try again...")
            clear()
    # return [int_choice, choice]


print(get_menu_choice())
