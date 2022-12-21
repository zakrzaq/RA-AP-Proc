import pandas as pd
from openpyxl.formula.translate import Translator


def populate_sheet_series(df, sheet, col=2, row=1):
    df = df.fillna('')
    output = []
    start_row = row
    start_col = col

    if isinstance(df, pd.DataFrame):
        for index, row in df.iterrows():
            output.append(row.values.tolist())
        for rowy, row in enumerate(output, start=start_row):
            for colx, value in enumerate(row, start=start_col):
                sheet.cell(column=colx, row=rowy, value=value)
    else:
        output = df
        for row, value in enumerate(output, row):
            sheet.cell(row, col, value)


def populate_sap_data_sheet(df, sheet, start_col=2, start_row=1):
    df = df.fillna('')
    output = []

    for index, row in df.iterrows():
        output.append(row.values.tolist())

    for rowy, row in enumerate(output, start=start_row):
        for colx, value in enumerate(row, start=start_col):
            sheet.cell(column=colx, row=rowy, value=value)


def extend_concats(sheet):
    print(sheet)
    # last_row = sheet.max_row
    # i = 100
    # while i < last_row:
    #     i += 1
    #     formula = sheet['A2'].value
    #     sheet[f'A{i}'] = Translator(
    #         formula, origin="A2").translate_formula(f"A{i}")
