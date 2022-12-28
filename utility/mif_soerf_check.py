def mif_soerf_check():
    import os

    from helpers.helpers import await_char
    import pandas as pd
    import dotenv

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    report_directory = os.environ["EDM_DRIVE"]

    mif_dir = os.path.join(report_directory, 'MIFs awaiting processing')
    soerf_dir = os.path.join(report_directory, 'SOERFs awaiting processing')
    mif_count = 0
    soerf_count = 0

    print('\nMIFs submitted:')
    mifs_submitted = pd.DataFrame()
    for filename in os.listdir(mif_dir):
        mif_count += 1
        f = os.path.join(mif_dir, filename)
        if os.path.isfile(f):
            if 'Jakub Zakrzewski' in f:
                print('- ' + filename)
                tmp_df = pd.read_excel(f)
                mifs_submitted = pd.concat([mifs_submitted, tmp_df])
    if mifs_submitted.empty:
        print('No MIF have been submitted by you')
    else:
        mifs_submitted = mifs_submitted.iloc[:, [1, 2, 3, 4]]
        for index, row in mifs_submitted.iterrows():
            r = row.apply(str).values
            print(", ".join(r))
        print(f'\nYou have submitted {mifs_submitted.shape[0]} MIFs today.')
    print(f'MIFs Requests in the submission folder: {mif_count} \n')

    tmp_df = pd.DataFrame()

    print('SOERFs submitted:')
    soerfs_submitted = pd.DataFrame()
    for filename in os.listdir(soerf_dir):
        soerf_count += 1
        f = os.path.join(soerf_dir, filename)
        if os.path.isfile(f):
            if 'Jakub Zakrzewski' in f:
                print('- ' + filename)
                tmp_df = pd.read_excel(f)
                soerfs_submitted = pd.concat([soerfs_submitted, tmp_df])
    if soerfs_submitted.empty:
        print('No SOERF have been submitted by you')
    else:
        soerfs_submitted = soerfs_submitted.iloc[:, [1, 2, 3, 4]]
        for index, row in soerfs_submitted.iterrows():
            r = row.apply(str).values
            print(", ".join(r))
        print(
            f'\nYou have submitted {soerfs_submitted.shape[0]} SOERFs today.')
    print(f'SOERFs Requests in the submission folder: {soerf_count} \n')

    await_char("y")