def get_requests(server=False):
    import pandas as pd
    import os
    from openpyxl.formula.translate import Translator

    from helpers.helpers import use_dotenv, ignore_warnings, use_logger, end_script
    from helpers.log import save_log, load_log
    import helpers.prompts as pr
    from state.output import output

    use_dotenv()
    use_logger()
    ignore_warnings()

    # VARIABLES
    ready_to_save = False
    output.reset()

    # OPEN LOG FILE NAD GENERATE SHEETS VARIABLES
    log = load_log()
    if log:
        ws_active = log["Active Materials"]
        # IMPORT REQUESTS FORM DESKTOP
        output.add(f"{pr.file}Reading request files")
        directory = os.environ["DIR_IN"]
        requests = pd.DataFrame()
        for filename in os.listdir(directory):
            if filename.endswith(".xlsm"):
                if "AP_Material_Master_Service_Request_Form" in filename:
                    file = os.path.join(directory, filename)
                    output.add(f"{pr.file}filename")
                    df = pd.read_excel(file, 2)
                    df = df.iloc[1:, :]
                    requests = pd.concat([requests, df])

        # cleanup data
        if not requests.empty:
            output.add(f"{pr.info}Cleaning the incoming data")
            requests["Unnamed: 3"] = requests["Unnamed: 3"].str.strip()
            requests["Unnamed: 2"] = requests["Unnamed: 2"].str.replace(
                "@rockwellautomation.com", ""
            )
            requests["Unnamed: 2"] = requests["Unnamed: 2"].str.replace(
                "@ra.rockwell.com", ""
            )
            requests["Unnamed: 2"] = requests["Unnamed: 2"].str.lower()
            requests.insert(0, "Date", pd.to_datetime("today").strftime("%d/%m/%Y"))

            # POPULATE REQUEST TO LOG
            output.add(f"{pr.info}Transferring to LOG")
            for cell in ws_active["B"]:
                if cell.value is None:
                    ws_active_firstrow = cell.row
                    break
            # TODO: set date format to excel column

            requests = requests.fillna("")
            requests_output = []
            for index, row in requests.iterrows():
                requests_output.append(row.values.tolist())

            for rowy, row in enumerate(requests_output, start=ws_active_firstrow):
                for colx, value in enumerate(row, start=1):
                    ws_active.cell(column=colx, row=rowy, value=value)

            for cell in ws_active["B"]:
                if cell.value is None:
                    ws_active_lastrow = cell.row
                    break

            # EXTEND FORMULAS By Col / Rows
            output.add(f"{pr.info}LOG data formatting")
            column_list = [
                "O",
                "P",
                "Q",
                "R",
                "S",
                "T",
                "U",
                "V",
                "W",
                "Y",
                "X",
                "Z",
                "AA",
                "AB",
                "AC",
                "AD",
                "AE",
                "AF",
                "AG",
                "AH",
                "AI",
                "AJ",
                "AK",
                "AL",
                "AM",
                "AN",
                "AO",
                "AP",
                "AQ",
                "AR",
                "AS",
                "AT",
                "AU",
                "AY",
                "AZ",
                "BA",
                "BB",
                "BC",
                "BD",
                "BE",
            ]
            ws_active_lastrow -= 1
            for x in column_list:
                i = ws_active_firstrow - 1
                while i < ws_active_lastrow:
                    i += 1
                    formula = ws_active[f"{x}2"].value
                    ws_active[f"{x}{i}"] = Translator(
                        formula, origin=f"{x}2"
                    ).translate_formula(f"{x}{i}")

            # FORMAT REQUESTS DATES
            output.add(f"{pr.info}Formatting request dates")
            for r in range(2, ws_active_lastrow):
                ws_active[f"A{r}"].number_format = "mm/dd/yy;@"

            # CREATE SORT
            output.add(f"{pr.info}Creating sort order")
            sort_count = ws_active_lastrow + 1
            i = 2
            while i < sort_count:
                if i == 1:
                    continue
                ws_active[f"BF{i}"].value = i - 1
                i += 1

            ready_to_save = True

        else:
            output.add(f"{pr.cncl}No request files found", ["code-line", "red"])

        if ready_to_save:
            save_log(log)

        # MAKE LIST OF MATERIALS IN AP LOG
        output.add(f"{pr.info}Saving material list")
        active_matnr_list_file = os.path.join(os.environ["DIR_OUT"], "AP materials.txt")

        if os.path.exists(active_matnr_list_file):
            os.remove(active_matnr_list_file)
            output.add(f"{pr.ok}material list redone")
        else:
            output.add(f"{pr.ok}material list created")

        active_matnr_list = ""
        with open(active_matnr_list_file, "w") as file:
            for row in ws_active:
                if row[4].value != None:
                    if type(row[4].value) is int:
                        numeric_matnr = (18 - len(str(row[4].value))) * "0" + str(
                            row[4].value
                        )
                        active_matnr_list += numeric_matnr + "\n"
                    elif "SAP MATNR" in row[4].value:
                        continue
                    else:
                        active_matnr_list += row[4].value + "\n"
            file.write(active_matnr_list)
            file.close()
            material_count = active_matnr_list.count("\n")
            output.add(f"{pr.file}Material list saved with {material_count} materials")

    return end_script(server)
