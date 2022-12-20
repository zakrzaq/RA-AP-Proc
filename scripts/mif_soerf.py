def mif_soerf():
    import pandas as pd
    import os

    from helpers.helpers import use_dotenv, ignore_warnings
    from helpers.data_frames import get_selected_active

    use_dotenv()
    ignore_warnings()

    selected_active_view = get_selected_active()

    # MIF / SOERF needed
    mif_soerf_view = selected_active_view[['Date Added', 'target sorg', 'target plant',
                                           'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'status']]

    mif_soerf = mif_soerf_view.loc[
        ((selected_active_view['status'].str.contains('cancel|complete', case=False) == False) | selected_active_view['status'].isna()) &
        (selected_active_view["Service Requested\n(from request form)"].isin(['Plant and sales org extension', 'Plant extension', 'Sales org extension'])) &
        (selected_active_view["mif/soerf check"].isin(['X'])) &
        (selected_active_view['MTART/GenItemCat'].isin(['ZTG', 'ZFG']))
    ]

    mif_soerf['sql'] = 'insert into AP_MM_SERVICE values(\'' + mif_soerf['target sorg'] + '\', \'' + mif_soerf['target plant'] + '\', \'' + mif_soerf['email prefix\n(from request form)'] + \
        '\', \'' + mif_soerf['SAP MATNR\n(from request form)'] + '\', \'' + \
        mif_soerf["Service Requested\n(from request form)"] + '\');'

    # OUTPUT TO SQL FILE
    output = mif_soerf['sql']
    output_str = ""
    for ind in output.index:
        output_str = output_str + output[ind] + "\n"

    # print(output_str)
    with open(os.path.join(os.environ['DIR_APP'], 'sql', 'full_mif_soerf.sql')) as file:
        lines = file.readlines()
        lines[5] = output_str
    with open(os.path.join(os.environ['DESKTOP_DIR'], 'AP_MIF_SOERF.sql'), 'w') as file:
        file.writelines(lines)

    print(f'Materials added to SQL query: {len(mif_soerf)}')
