import os
import platform

from scripts.sap_data import get_sap_data
import scripts.requests as requests
import scripts.mif_soerf as mif_soerf
import scripts.am_status as am_status
import scripts.am_emails as am_emails
import scripts.pm_status as pm_status
import scripts.pm_emails as pm_emails


import utility.check_mif_soerf as mif_soerf_check
import utility.clean_desktop as clean_desktop
import utility.check_daily_report as daily_report_check
import utility.sap_data as sap_data


def clear():
    if platform.system() == 'Windows':
        return os.system('cls')
    else:
        return os.system('clear')


clear()


def get_menu_choice():
    def print_menu():       # Your menu design here
        print(30 * "-", "AP MM EXTENSION PROCESS", 30 * "-")
        print("1)    Download SAP DATA")
        print("2)    Process SAP DATA")
        print(85 * "-")
        print("3)    Get current requests")
        print("4)    Generate MIF / SOERF requests")
        print("5)    Update Material Statuses pre MM")
        print("6)    Generate AM Price & PCE requests")
        print("7)    Update Material Statuses post MM Extension")
        print("8)    Generate PM CCC, Localization & GTS Requests")
        print(85 * "-")
        print("9)    UTILITY: _____")
        print("10)   UTILITY: Clean working folder & archive request files")
        print("11)   UTILITY: Check for MIF/SOERF submitted")
        print("12)   UTILITY: Check for daily report uploaded to Sharepoint Repository")
        print(85 * "-")
        print("U)    Update program")
        print("X)    Close program")
        print(85 * "=")

    loop = True
    int_choice = -1

    while loop:          # While loop which will keep going until loop = False
        print_menu()    # Displays menu
        choice = input("Choose procedure to run: ")
        print("\n")

        if choice == '1':
            get_sap_data()
            clear()
        elif choice == '2':
            sap_data.sap_data()
            clear()
        elif choice == '3':
            requests.requests()
            clear()
        elif choice == '4':
            mif_soerf.mif_soerf()
            clear()
        elif choice == '5':
            am_status.am_status()
            clear()
        elif choice == '6':
            am_emails.am_emails()
            clear()
        elif choice == '7':
            pm_status.pm_status()
            clear()
        elif choice == '8':
            pm_emails.pm_emails()
            clear()
        elif choice == '10':
            clean_desktop.clean_desktop()
            clear()
        elif choice == '11':
            mif_soerf_check.check_mif_soerf()
            clear()
        elif choice == '12':
            daily_report_check.check_daily_report()
            clear()
        elif (choice == 'u' or choice == 'U'):
            os.system("git pull")
            clear()
        elif (choice == 'x' or choice == 'X'):
            int_choice = -1
            print("Exiting...")
            loop = False
        else:
            # Any inputs other than values 1-4 we print an error message
            input("Wrong menu selection. Enter any key to try again...")
            clear()
    # return [int_choice, choice]


print(get_menu_choice())
