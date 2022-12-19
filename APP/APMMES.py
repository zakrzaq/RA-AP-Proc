import os
import platform

import utility.check_mif_soerf as mif_soerf
import utility.check_daily_report as daily_report
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
        print("X). Close AP MM EXTENSION PROCESS")
        print(85 * "=")

    loop = True
    int_choice = -1

    while loop:          # While loop which will keep going until loop = False
        print_menu()    # Displays menu
        choice = input("Choose procedure to run: ")

        if choice == '1':
            clear()
        elif choice == '2':
            choice = ''
            while len(choice) == 0:
                choice = input("What is your name: ")
            int_choice = 2
            clear()
        elif choice == '3':
            choice = ''
            while len(choice) == 0:
                choice = input("What is your age: ")
            int_choice = 3
            clear()
            # loop = False
        elif choice == '4':
            choice = ''
            while len(choice) == 0:
                choice = input("What is your sex: ")
            int_choice = 4
            clear()
            # loop = False
        elif choice == '5':
            int_choice = -1
            print("Exiting..")
            loop = False  # This will make the while loop to end
        elif choice == '9':
            sap_data.sap_data()
            clear()
        elif choice == '11':
            mif_soerf.check_mif_soerf()
            clear()
        elif choice == '12':
            daily_report.check_daily_report()
            clear()
        elif choice == 'x':
            int_choice = -1
            print("Exiting...")
            loop = False
        elif choice == 'X':
            int_choice = -1
            print("Exiting...")
            loop = False
        else:
            # Any inputs other than values 1-4 we print an error message
            input("Wrong menu selection. Enter any key to try again...")
            clear()
    # return [int_choice, choice]


print(get_menu_choice())
