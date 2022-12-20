import os
import pandas as pd

from helpers.log import load_log, save_log, test_save
from helpers.xlsm import populate_sheet_series
from helpers.helpers import await_char
from helpers.data_frames import get_selected_active


def am_status():
    # LOAD LOG
    log = load_log()
    ws_active = log['Active Materials']

    selected_active_view = get_selected_active()

    # MATNRs PRICE NEEDED
    need_price = (selected_active_view['target sorg price'].isna()) & (~selected_active_view['SOERF Submitted'].isna()) & (
        (selected_active_view['status'].str.contains('cancel|complete|on hold|needs price;', case=False) == False) | (selected_active_view['status'].isnull()))

    selected_active_view.loc[need_price, 'status'] = selected_active_view['status'].astype(
        str) + "needs price;"

    price_requested = selected_active_view.loc[
        (selected_active_view['status'].str.contains(
            'needs price;') == True)
    ]
    print(f'Materials NEEDING PRICE in AP LOG: {len(price_requested)}')

    # MATNRs PCE NEEDED
    need_pce = (
        ((selected_active_view['status'].str.contains('cancel|complete', case=False) == False)) &
        ((selected_active_view['status'].str.contains('pending PCE review;') == False)) &
        (selected_active_view['Service Requested\n(from request form)']
            == 'Product Certification Review')
    ) | (
        (selected_active_view['MTART/GenItemCat'].isin(['ZFG', 'ZTG'])) &
        (~selected_active_view['Regulatory Cert\n(Z62 Characteristic)'].isna()) &
        (selected_active_view['Z62 characteristic\n(assigned in SAP)'].isna()) &
        ((selected_active_view['status'].str.contains('cancel|complete|on hold|pending PCE review;', case=False) == False)) &
        ((selected_active_view['status'].str.contains('pending PCE review;') == False)))

    selected_active_view.loc[need_pce, 'status'] = selected_active_view['status'].astype(
        str) + 'pending PCE review;'

    pce_requested = selected_active_view.loc[
        (selected_active_view['status'].str.contains(
            'pending PCE review;') == True)
    ]
    print(f'Materials needing PCE in log: {len(pce_requested)}')

    # STATUS TO TXT
    status_file = os.path.join(
        os.environ['DIR_DESKTOP'], 'AP status.txt')
    status_output = selected_active_view['status']
    status_output_str = ''

    if os.path.exists(status_file):
        os.remove(status_file)
        for ind in status_output.index:
            if type(status_output[ind]) == float:
                status_output_str = status_output_str + "" + "\n"
            else:
                status_output_str = status_output_str + \
                    str(status_output[ind]) + "\n"
        with open(status_file, 'w') as file:
            file.writelines(status_output_str)

    # TEST SAVE LOG
    populate_sheet_series(status_output, ws_active, 50, 2)
    test_save(log, "TEST_am_status")
    # ACTUAL
    await_char(
        "y", "Press Y to save to live LOG file or C to cancel.",  save_log, log)
