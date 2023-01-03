def requests(server=False):
    import pandas as pd
    import os
    from openpyxl.formula.translate import Translator
    from flask import Markup

    from helpers.helpers import await_char, use_dotenv, ignore_warnings, use_logger, output_msg
    from helpers.log import save_log, load_log, test_save

    use_dotenv()
    use_logger()
    ignore_warnings()

    # VARIABLES
    ready_to_save = False
    output = ''

    # OPEN LOG FILE NAD GENERATE SHEETS VARIABLES
    output += output_msg(server, "Reading log file")
    try:
        log = load_log()
        ws_active = log['Active Materials']

        # IMPORT REQUESTS FORM DESKTOP
        output += output_msg(server, "Reading request files")
        directory = os.environ["DIR_IN"]
        requests = pd.DataFrame()

        for filename in os.listdir(directory):
            if filename.endswith(".xlsm"):
                if 'AP_Material_Master_Service_Request_Form' in filename:
                    file = os.path.join(directory, filename)
                    output += output_msg(server, "\t" + filename)
                    df = pd.read_excel(file, 2)
                    df = df.iloc[1:, :]
                    # output += output_msg(server, df)
                    requests = pd.concat([requests, df])

        # cleanup data
        output += output_msg(server, "Cleaning the data")
        if not requests.empty:
            requests['Unnamed: 3'] = requests['Unnamed: 3'].str.strip()
            requests['Unnamed: 2'] = requests['Unnamed: 2'].str.replace(
                '@rockwellautomation.com', '')
            requests['Unnamed: 2'] = requests['Unnamed: 2'].str.replace(
                '@ra.rockwell.com', '')
            requests['Unnamed: 2'] = requests['Unnamed: 2'].str.lower()
            requests.insert(0, 'Date', pd.to_datetime(
                'today').strftime("%m/%d/%Y"))

            # POPULATE REQUEST TO LOG
            output += output_msg(server, "Transferring to LOG")
            try:
                # last populated row
                for cell in ws_active['B']:
                    # print(cell.value)
                    if cell.value is None:
                        # print(cell.row)
                        ws_active_firstrow = cell.row
                        break

                requests = requests.fillna('')
                requests_output = []
                for index, row in requests.iterrows():
                    # print(row.values.tolist())
                    requests_output.append(row.values.tolist())
                # print(requests_output)

                for rowy, row in enumerate(requests_output, start=ws_active_firstrow):
                    for colx, value in enumerate(row, start=1):
                        ws_active.cell(column=colx, row=rowy, value=value)

                for cell in ws_active['B']:
                    if cell.value is None:
                        ws_active_lastrow = cell.row
                        break
            except:
                output += output_msg(server, 'could not populate data ')

            # EXTEND FORMULAS By Col / Rows
            output += output_msg(server, "Data formatting")
            try:
                column_list = ['O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'Y', 'X', 'Z', 'AA', 'AB', 'AC', 'AD', 'AE', 'AF', 'AG', 'AH',
                               'AI', 'AJ', 'AK', 'AL', 'AM', 'AN', 'AO', 'AP', 'AQ', 'AR', 'AS', 'AT', 'AU', 'AY', 'AZ', 'BA', 'BB', 'BC', 'BD', 'BE']
                ws_active_lastrow -= 1
                for x in column_list:
                    i = ws_active_firstrow - 1
                    while i < ws_active_lastrow:
                        i += 1
                        formula = ws_active[f'{x}2'].value
                        ws_active[f'{x}{i}'] = Translator(
                            formula, origin=f"{x}2").translate_formula(f"{x}{i}")
            except:
                output += output_msg(server, 'could not extend formulas')

            # CREATE SORT
            try:
                sort_count = ws_active_lastrow + 1
                # print(sort_count)
                i = 2
                while i < sort_count:
                    if i == 1:
                        continue
                    # print(i)
                    ws_active[f"BF{i}"].value = i - 1
                    i += 1
            except:
                output += output_msg(server, 'could not create sort order')

            ready_to_save = True

        else:
            output += output_msg(server, 'no request files found')

        if ready_to_save:
            # TESTING
            test_save(log, "TEST_requests")
            # ACTUAL
            if server == False:
                await_char(
                    "y", "Press Y to save to live LOG file or C to cancel.",  save_log, log)
            else:
                save_log(log)
                output += output_msg(server, 'LOG file saved')
                return Markup(output)

        # MAKE LIST OF MATERIALS IN AP LOG

        active_matnr_list_file = os.path.join(
            os.environ['DIR_DESKTOP'], 'AP materials.txt')

        if os.path.exists(active_matnr_list_file):
            os.remove(active_matnr_list_file)
            output += output_msg(server, 'material list redone')
        else:
            output += output_msg(server, 'material list not found')

        active_matnr_list = ''
        with open(active_matnr_list_file, "w") as file:
            for row in ws_active:
                if row[4].value != None:
                    if 'SAP MATNR' in row[4].value:
                        continue
                    elif row[4].value.isnumeric():
                        active_matnr_list += ('000000000000000000' +
                                              row[4].value + '\n')
                    else:
                        active_matnr_list += (row[4].value + '\n')
            # print(active_matnr_list)
            file.write(active_matnr_list)
            file.close()

        if server == False:
            await_char("y", "", "Routine completed. Press Y to continue")
        else:
            output += output_msg(server, 'Routine completed.')

    except:
        if server == False:
            await_char(
                "y", "Unable to load AP LOG, please close the excel file and press Y to continue")
        else:
            output += output_msg(server, 'Routine completed.')
