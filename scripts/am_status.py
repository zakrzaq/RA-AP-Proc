import os
import pandas as pd
from flask import Markup

from helpers.log import load_log, save_log, test_save
from helpers.xlsm import populate_sheet_series
from helpers.helpers import await_char, use_dotenv, ignore_warnings, use_logger, output_msg
from helpers.data_frames import get_selected_active


def am_status(server=False):
    use_dotenv()
    use_logger()
    ignore_warnings()

    output = ''

    # LOAD LOG
    try:
        log = load_log()
        ws_active = log['Active Materials']
        selected_active_view = get_selected_active()
    except:
        if server == False:
            await_char(
                "y", "Unable to load AP LOG, please close the excel file and press Y to continue")
        else:
            output += output_msg(server,
                                 'Unable to load AP LOG, please close the excel file.', 'red')
            return Markup(output)

    # MATNRs PRICE NEEDED
    need_price = (selected_active_view['target sorg price'].isna()) & (~selected_active_view['SOERF Submitted'].isna()) & (
        (selected_active_view['status'].str.contains('cancel|complete|on hold|needs price;', case=False) == False) | (selected_active_view['status'].isnull()))

    selected_active_view.loc[need_price, 'status'] = selected_active_view['status'].astype(
        str).replace("nan", "") + "needs price;"

    price_requested = selected_active_view.loc[
        (selected_active_view['status'].str.contains(
            'needs price;') == True)
    ]
    output += output_msg(server,
                         f'Materials NEEDING PRICE in AP LOG: {len(price_requested)}')

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
    output += output_msg(server,
                         f'Materials NEEDING PCE in AP LOG: {len(pce_requested)}')

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
    if server == False:
        await_char(
            "y", "Press Y to save to live LOG file or C to cancel.",  save_log, log)
    else:
        save_log(log)
        output += output_msg(server, 'LOG file saved')
        return Markup(output)
