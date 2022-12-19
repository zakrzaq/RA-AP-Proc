import os
import platform

import scripts.requests as requests
import scripts.mif_soerf as mif_soerf
import scripts.am_emails as am_emails
import scripts.pm_status as pm_status
import scripts.pm_emails as pm_emails


import utility.check_mif_soerf as mif_soerf_check
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
        print("1).    Get current requests")
        print("2).    Generate MIF / SOERF requests")
        print("3).    Generate AM Price & PCE requests")
        print("4).    Update Material Statuses post MM Extension")
        print("5).    Generate PM CCC, Localization & GTS Requests")
        print("6).    ")
        print("7).    ")
        print("8).    ")
        print(85 * "-")
        print("9).    UTILITY: Bring SAP Data")
        print("10).   UTILITY: ")
        print("11).   UTILITY: Check for MIF/SOERF submitted")
        print("12).   UTILITY: Check for daily report uploaded to Sharepoint Repository")
        print(85 * "-")
        print("X).    Close AP MM EXTENSION PROCESS")
        print(85 * "=")

    loop = True
    int_choice = -1

    while loop:          # While loop which will keep going until loop = False
        print_menu()    # Displays menu
        choice = input("Choose procedure to run: ")

        if choice == '1':
            requests.requests()
            clear()
        elif choice == '2':
            mif_soerf.mif_soerf()
            clear()
        elif choice == '3':
            am_emails.am_emails()
            clear()
        elif choice == '4':
            pm_status.pm_status()
            clear()
        elif choice == '5':
            pm_emails.pm_emails()
            clear()
        elif choice == '9':
            sap_data.sap_data()
            clear()
        elif choice == '11':
            mif_soerf_check.check_mif_soerf()
            clear()
        elif choice == '12':
            daily_report_check.check_daily_report()
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
