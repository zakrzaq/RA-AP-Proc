def clean_desktop():
    import os
    import shutil

    from helpers.helpers import await_char

    report_directory = os.environ['EDM_APMM']
    output_directory = os.environ['DIR_OUT']
    input_directory = os.environ['DIR_IN']
    process_dirs = [output_directory, input_directory]

    dir_pce_feedback = os.path.join(report_directory, 'PCE FEEDBACK')
    dir_pce_requests = os.path.join(report_directory, 'PCE REQUESTS')
    dir_pricing = os.path.join(report_directory, 'PRICING REQUESTS')
    dir_inhts = os.path.join(report_directory, 'CGT requests')
    dir_local = os.path.join(report_directory, 'india localization')
    dir_ap_req_archive = os.path.join(
        os.environ['DIR_DESKTOP'], 'AP Process', 'AP Requests')

    # archive desktop folder to shared edm drive
    try:
        for dir in process_dirs:
            print(dir)
            for filename in os.listdir(dir):
                f = os.path.join(dir, filename)
                if os.path.isfile(f):
                    # pce requests
                    if ' ASSESSMENT REQUEST.xlsx' in f:
                        print("\t" + filename)
                        shutil.move(f, dir_pce_requests)
                    # pce feedback
                    if ' ASSESSMENT REQUEST' in f:
                        print("\t" + filename)
                        shutil.move(f, dir_pce_feedback)
                    # pricing requests
                    if 'AP pricing needed with active demand' in f:
                        print("\t" + filename)
                        shutil.move(f, dir_pricing)
                    # inhts requests
                    if 'INHTS request ' in f:
                        print("\t" + filename)
                        shutil.move(f, dir_inhts)
                    # localization requests
                    if 'India localization required' in f:
                        print("\t" + filename)
                        shutil.move(f, dir_local)
                    # AP requests
                    if ('AP_Material_Master_Service_Request_Form' in f) or ('_AP form ') in f or ('AP form ' in f) or ('ap form ' in f):
                        print("\t" + filename)
                        shutil.move(f, dir_ap_req_archive)
                    # TODO: uncomment when sap_data is ready
                    # if ('mara' in f) or ('marc' in f) or ('mvke' in f) or ('ausp' in f) or ('mlan' in f) or ('price' in f) or ('gts' in f) or ('sales_text' in f):
                    #     print(f)
    except:
        print('Something went wrong :/ \nRun me again, please!')
        await_char()

    await_char()
