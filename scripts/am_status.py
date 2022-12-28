import os
import pandas as pd

from helpers.log import load_log, save_log, test_save
from helpers.xlsm import populate_sheet_series
from helpers.helpers import await_char, use_dotenv, ignore_warnings
from helpers.data_frames import get_selected_active

use_dotenv()
ignore_warnings()


def am_status():
    # LOAD LOG
    log = load_log()
    ws_active = log['Active Materials']

    selected_active_view = get_selected_active()

    # MATNRs PRICE NEEDED
    need_price = (selected_active_view['target sorg price'].isna()) & (~selected_active_view['SOERF Submitted'].isna()) & (
        (selected_active_view['status'].str.contains('cancel|complete|on hold|needs price;', case=False) == False) | (selected_active_view['status'].isnull()))

    selected_active_view.loc[need_price, 'status'] = selected_active_view['status'].astype(
        str).replace("nan", "") + "needs price;"

    price_requested = selected_active_view.loc[
        (selected_active_view['status'].str.contains(
            'needs price;') == True)
    ]
    print(f'Materials NEEDING PRICE in AP LOG: {len(price_requested)}')

    # MATNRs PCE NEEDED
    need_pce = (
        # TODO: needs to be in separate section
        #     (selected_active_view['status'].str.contains(
        #         'cancel|complete|on hold|pending PCE review', case=False) == False)
        #     (selected_active_view['Service Requested\n(from request form)']
        #      == 'Product Certification Review')
        # ) | (
        (selected_active_view['Regulatory Cert\n(Z62 Class)'].isin(
            ['BIS', 'BSMI', 'CCC', 'KC', 'RCM'])) &
        (selected_active_view['Z62 characteristic\n(assigned in SAP)'].isna()) &
        (selected_active_view['MTART/GenItemCat'].isin(['ZFG',
         'ZTG', 'ZRS1', 'ZRS4', 'ZRS5'])) &
        (selected_active_view['status'].str.contains(
            'cancel|complete|on hold|pending PCE review', case=False) == False)
    )

    # test = selected_active_view.loc[need_pce, ['status',
    #                                            'Z62 characteristic\n(assigned in SAP)']]
    # print(test)
    # print(len(test))

    selected_active_view.loc[need_pce, 'status'] = selected_active_view['status'].astype(
        str).replace("nan", "") + 'pending PCE review;'

    pce_requested = selected_active_view.loc[
        (selected_active_view['status'].str.contains(
            'pending PCE review;') == True)
    ]
    print(f'Materials needing PCE in log: {len(pce_requested)}')

    # STATUS OUTPUT
    status_output = selected_active_view['status']
    status_output_str = ''

    for ind in status_output.index:
        if type(status_output[ind]) == float:
            status_output_str = status_output_str + "" + "\n"
        else:
            status_output_str = status_output_str + \
                str(status_output[ind]) + "\n"

    # TEST SAVE LOG
    populate_sheet_series(status_output, ws_active, 50, 2)
    test_save(log, "TEST_am_status")
    # ACTUAL
    await_char(
        "y", "Press Y to save to live LOG file or C to cancel.",  save_log, log)
