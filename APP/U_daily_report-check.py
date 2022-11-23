import os
import platform
from datetime import date

if platform.system() == "Linux":
    report_directory = "/mnt/x/"
else:
    report_directory = r"C:\Users\JZakrzewski\Rockwell Automation, Inc\Engineering Data Management - Material Master Service Request Updates"

ap_materials_list = (
    r"C:\Users\jzakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\ap_materials.txt"
)

today = date.today().strftime("%m-%d-%Y")
print("Daily AP Process update for:  {0}\n".format(today))

for filename in os.listdir(report_directory):
    f = os.path.join(report_directory, filename)
    if os.path.isfile(f):
        if today in f:
            print("\t{0}\n".format(filename))

if os.path.exists(ap_materials_list):
    os.remove(ap_materials_list)
    print("Materials list file removed\n")

input("Press ENTER to continue.")
