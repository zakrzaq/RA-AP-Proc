def check_daily_report(server=False):
    import os
    import sys
    fpath = os.path.join(os.path.dirname(__file__), 'utility')
    sys.path.append(fpath)

    import platform
    from flask import Markup
    from datetime import date
    from helpers.helpers import output_msg, await_char

    output = ''
    report_found = False

    if platform.system() == "Linux":
        report_directory = "/mnt/x/"
    else:
        report_directory = r"C:\Users\JZakrzewski\Rockwell Automation, Inc\Engineering Data Management - Material Master Service Request Updates"

    ap_materials_list = (
        r"C:\Users\jzakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\ap_materials.txt"
    )

    today = date.today().strftime("%m-%d-%Y")
    output += output_msg(
                         f"Daily AP Process update for:  {today}", "bold")

    for filename in os.listdir(report_directory):
        f = os.path.join(report_directory, filename)
        if os.path.isfile(f):
            if today in f:
                output += output_msg(f"\t{filename}")
                report_found = True

    if report_found != True:
        output += output_msg(
                             'No report found for today in Sharepoint repository')

    if os.path.exists(ap_materials_list):
        os.remove(ap_materials_list)
        output += output_msg("Materials list file removed")

    if server:
        return Markup(output)
    else:
        await_char()
