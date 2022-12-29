def reconcile_pce():
    import os
    import pandas as pd

    from helpers.helpers import await_char, use_dotenv, ignore_warnings, use_logger
    from helpers.log import save_log, load_log, test_save
    from helpers.data_frames import get_active

    use_dotenv()
    use_logger()
    ignore_warnings()

    print('pce recn')

    # FIND PCE REQUEST
    for filename in os.listdir('C:\RA-Apps\AP-Proc\INPUTS'):
        file = os.path.join('C:\RA-Apps\AP-Proc\INPUTS', filename)
        if ' ASSESSMENT REQUEST' in filename:
            print("\t" + file)

    # PROCESS PCE REQUESTS

    # LOAD LOG TO DF
    mifs = get_active('mif')

    # MATRIALS NEEDING ORG SOURCE
    mifs_view = mifs[['MATERIAL']]
    print(mifs.head(5))
