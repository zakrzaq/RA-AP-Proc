def check_daily_report(server=False):
    import os
    import sys

    from helpers.data_frames import handle_eod_report
    from state.output import output

    fpath = os.path.join(os.path.dirname(__file__), "utility")
    sys.path.append(fpath)

    from datetime import date
    from helpers.helpers import await_char
    import helpers.prompts as pr

    output.reset()
    report_found = False

    report_directory = r"C:\Users\JZakrzewski\Rockwell Automation, Inc\Engineering Data Management - Material Master Service Request Updates"

    ap_materials_list = r"C:\Users\jzakrzewski\OneDrive - Rockwell Automation, Inc\Desktop\ap_materials.txt"

    today = date.today().strftime("%m-%d-%Y")
    output.add(f"{pr.info}Daily AP Process update for:  {today}", ["code-line", "bold"])

    for filename in os.listdir(report_directory):
        f = os.path.join(report_directory, filename)
        if os.path.isfile(f):
            if today in f:
                stats = handle_eod_report(f)
                output.add(f"\t{pr.ok}{filename}", ["code-line", "bold"])
                for k, v in stats.items():
                    key = k.capitalize().replace("_", " ")
                    output.add(f"{key}: {v}")
                report_found = True

    if report_found != True:
        output.add(f"{pr.cncl}No report found for today in Sharepoint repository")

    if os.path.exists(ap_materials_list):
        os.remove(ap_materials_list)
        output.add(f"{pr.file}Materials list file removed")

    if server:
        return output.get_markup()
    else:
        await_char()
