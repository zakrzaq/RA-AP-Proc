import pandas as pd
from openpyxl.formula.translate import Translator


def populate_sheet_series(df, sheet, col, row):
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


def populate_sap_data_sheet(df, sheet):
    df = df.fillna('')
    output = []

    for index, row in df.iterrows():
        output.append(row.values.tolist())

    start_row = 2
    start_col = 1 if df == gts else 2

    for rowy, row in enumerate(output, start=start_row):
        for colx, value in enumerate(row, start=start_col):
            sheet.cell(column=colx, row=rowy, value=value)


def extend_concats(sheet):
    if sheet != gts:
        last_row = sheet.max_row
        i = 100
        while i < last_row:
            i += 1
            formula = sheet['A2'].value
            sheet['A{}'.format(i)] = Translator(
                formula, origin="A2").translate_formula("A{}".format(i))
