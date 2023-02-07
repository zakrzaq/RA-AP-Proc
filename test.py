def clean_desktop(server=False):
    import os
    import shutil
    from markupsafe import Markup

    from helpers.helpers import await_char, output_msg

    output = ""
    report_directory = os.environ["EDM_APMM"]
    output_directory = os.environ["DIR_OUT"]
    input_directory = os.environ["DIR_IN"]
    process_dirs = [output_directory, input_directory]

    dir_pce_feedback = os.path.join(report_directory, "PCE FEEDBACK")
    dir_pce_requests = os.path.join(report_directory, "PCE REQUESTS")
    dir_pricing = os.path.join(report_directory, "PRICING REQUESTS")
    dir_inhts = os.path.join(report_directory, "CGT requests")
    dir_local = os.path.join(report_directory, "india localization")
    dir_ap_req_archive = os.path.join(
        os.environ["DIR_DESKTOP"], "AP Process", "AP Requests"
    )

    # archive desktop folder to shared edm drive
    for dir in process_dirs:
        output += output_msg(f"Folder processed: {dir}", "bold")
        for filename in os.listdir(dir):
            f = os.path.join(dir, filename)
            if os.path.isfile(f):
                # pce requests
                if " ASSESSMENT REQUEST.xlsx" in f:
                    print(f)
                    # output += output_msg("- " + filename)
                    # dest = os.path.join(dir_pce_requests, filename)
                    # if os.path.exists(dest):
                    #     os.remove(dest)
                    # shutil.copy2(f, dir_pce_requests)
                    # os.remove(os.path.join(output_directory, f))
                # pce feedback
                if " ASSESSMENT REQUEST" in f:
                    print(f)
                    # output += output_msg("- " + filename)
                    # dest = os.path.join(dir_pce_feedback, filename)
                    # if os.path.exists(dest):
                    #     os.remove(dest)
                    # shutil.copy2(f, dir_pce_feedback)
                    # os.remove(os.path.join(output_directory, f))


clean_desktop()
