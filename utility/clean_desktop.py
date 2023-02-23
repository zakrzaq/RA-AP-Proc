def clean_desktop(server=False):
    import os
    import shutil

    from helpers.helpers import end_script
    from state.output import output
    import helpers.prompts as pr

    output.reset()
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

    def handle_archive(f, output):
        try:
            filename = os.path.basename(f)
            dest = os.path.join(output, filename)
            if os.path.exists(dest):
                os.remove(dest)
            shutil.copy2(f, output)
            os.remove(os.path.join(output_directory, f))
            output.add(f"{pr.file}{filename}")
        except:
            output.add(f"{pr.cncl}{filename}")

    def handle_remove(f):
        filename = os.path.basename(f)
        try:
            os.remove(f)
            output.add(f"{pr.file}{filename}")
        except:
            output.add(f"{pr.cn}{filename}")

    # archive desktop folder to shared edm drive
    for dir in process_dirs:
        output.add(f"Folder processed: {dir}", ["code-line", "bold"])
        for filename in os.listdir(dir):
            f = os.path.join(dir, filename)
            if os.path.isfile(f):
                # pce requests
                if " ASSESSMENT REQUEST.xlsx" in f:
                    handle_archive(f, dir_pce_requests)
                # pce feedback
                if " ASSESSMENT REQUEST" in f:
                    handle_archive(f, dir_pce_feedback)
                # pricing requests
                if "AP pricing needed with active demand" in f:
                    handle_archive(f, dir_pricing)
                # inhts requests
                if "INHTS request " in f:
                    handle_archive(f, dir_inhts)
                # localization requests
                if "India localization required" in f:
                    handle_archive(f, dir_local)
                # AP requests
                if (
                    ("AP_Material_Master_Service_Request_Form" in f)
                    or ("_AP form ") in f
                    or ("AP form " in f)
                    or ("ap form " in f)
                ):
                    handle_archive(f, dir_ap_req_archive)
                if (
                    ("mara" in f)
                    or ("marc" in f)
                    or ("mvke" in f)
                    or ("ausp" in f)
                    or ("mlan" in f)
                    or ("price" in f)
                    or ("gts" in f)
                    or ("sales_text" in f)
                ):
                    handle_remove(f)
                if "UPDATES TO Z62" in f:
                    handle_remove(f)

    return end_script(server)
