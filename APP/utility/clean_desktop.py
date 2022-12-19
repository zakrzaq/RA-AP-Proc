def clean_desktop():
    import os
    import platform
    import shutil
    from helpers.helpers import await_char

    if platform.system() == 'Linux':
        dir_temp = '/mnt/c/users/jzakrzewski/OneDrive - Rockwell Automation, Inc/Desktop'
        report_directory = '/mnt/z/Request Logs/APMM'
    else:
        dir_temp = 'C:\\Users\\jzakrzewski\\OneDrive - Rockwell Automation, Inc\\Desktop'
        report_directory = 'Z:\\Request Logs\\APMM'

    dir_pce_feedback = os.path.join(report_directory, 'PCE FEEDBACK')
    dir_pce_requests = os.path.join(report_directory, 'PCE REQUESTS')
    dir_pricing = os.path.join(report_directory, 'PRICING REQUESTS')
    dir_inhts = os.path.join(report_directory, 'CGT requests')
    dir_local = os.path.join(report_directory, 'india localization')
    dir_ap_req_archive = os.path.join(dir_temp, 'AP Process', 'AP Requests')

    # archive desktop folder to shared edm drive
    for filename in os.listdir(dir_temp):
        f = os.path.join(dir_temp, filename)
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
            # AP requests - A
            if 'AP_Material_Master_Service_Request_Form' in f:
                print("\t" + filename)
                os.remove(f)
            # AP requests - B
            if '_AP form ' in f:
                print("\t" + filename)
                os.remove(f)
            # AP requests - C
            if 'AP form ' in f:
                print("\t" + filename)
                os.remove(f)
            if 'ap form ' in f:
                print("\t" + filename)
                os.remove(f)

    await_char("y")
