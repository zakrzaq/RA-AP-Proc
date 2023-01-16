def clean_desktop(server=False):
    import os
    import shutil
    from markupsafe import Markup

    from helpers.helpers import await_char, output_msg

    output = ''
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
    # try:
    for dir in process_dirs:
        output += output_msg(f'Folder processed: {dir}', 'bold')
        for filename in os.listdir(dir):
            f = os.path.join(dir, filename)
            if os.path.isfile(f):
                # pce requests
                if ' ASSESSMENT REQUEST.xlsx' in f:
                    output += output_msg("- " + filename)
                    dest = os.path.join(dir_pce_requests, filename)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(f, dir_pce_requests)
                    os.remove(os.path.join(output_directory, f))
                # pce feedback
                if ' ASSESSMENT REQUEST' in f:
                    output += output_msg("- " + filename)
                    dest = os.path.join(dir_pce_feedback, filename)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(f, dir_pce_feedback)
                    os.remove(os.path.join(output_directory, f))
                # pricing requests
                if 'AP pricing needed with active demand' in f:
                    output += output_msg("- " + filename)
                    dest = os.path.join(dir_pricing, filename)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(f, dir_pricing)
                    os.remove(os.path.join(output_directory, f))
                # inhts requests
                if 'INHTS request ' in f:
                    output += output_msg("- " + filename)
                    dest = os.path.join(dir_inhts, filename)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(f, dir_inhts)
                    os.remove(os.path.join(output_directory, f))
                # localization requests
                if 'India localization required' in f:
                    output += output_msg("- " + filename)
                    dest = os.path.join(dir_local, filename)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(f, dir_local)
                    os.remove(os.path.join(output_directory, f))
                # AP requests
                if ('AP_Material_Master_Service_Request_Form' in f) or ('_AP form ') in f or ('AP form ' in f) or ('ap form ' in f):
                    output += output_msg("- " + filename)
                    dest = os.path.join(dir_ap_req_archive, filename)
                    if os.path.exists(dest):
                        os.remove(dest)
                    shutil.copy2(f, dir_ap_req_archive)
                    os.remove(os.path.join(output_directory, f))
                if ('mara' in f) or ('marc' in f) or ('mvke' in f) or ('ausp' in f) or ('mlan' in f) or ('price' in f) or ('gts' in f) or ('sales_text' in f):
                    output += output_msg('- ' + f)
                    os.remove(f)
                if 'UPDATES TO Z62' in f:
                    output += output_msg('\t' + f)
                    os.remove(f)
    # except:
    #     output += output_msg(
    #                          'Something went wrong :/ \nRun me again, please!')
    #     if server == False:
    #         await_char()
    #     else:
    #         return output

    if server == False:
        await_char()
    else:
        print(output)
        return Markup(output)
