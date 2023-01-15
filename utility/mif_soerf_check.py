def mif_soerf_check(server=False):
    import os

    from helpers.helpers import await_char, output_msg
    import pandas as pd
    import dotenv
    from markupsafe import Markup

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    output = ""
    report_directory = os.environ["EDM_DRIVE"]

    mif_dir = os.path.join(report_directory, "MIFs awaiting processing")
    soerf_dir = os.path.join(report_directory, "SOERFs awaiting processing")
    mif_count = 0
    soerf_count = 0

    output += output_msg("\nMIFs submitted:", "bold")
    mifs_submitted = pd.DataFrame()
    for filename in os.listdir(mif_dir):
        mif_count += 1
        f = os.path.join(mif_dir, filename)
        if os.path.isfile(f):
            if "Jakub Zakrzewski" in f:
                output += output_msg("- " + filename)
                tmp_df = pd.read_excel(f)
                mifs_submitted = pd.concat([mifs_submitted, tmp_df])
    if mifs_submitted.empty:
        output += output_msg("No MIF have been submitted by you")
    else:
        mifs_submitted = mifs_submitted.iloc[:, [1, 2, 3, 4]]
        for index, row in mifs_submitted.iterrows():
            r = row.apply(str).values
            output += output_msg(", ".join(r))
        output += output_msg(
            f"\nYou have submitted {mifs_submitted.shape[0]} MIFs today."
        )
    output += output_msg(f"MIFs Requests in the submission folder: {mif_count} \n")

    tmp_df = pd.DataFrame()

    output += output_msg("SOERFs submitted:", "bold")
    soerfs_submitted = pd.DataFrame()
    for filename in os.listdir(soerf_dir):
        soerf_count += 1
        f = os.path.join(soerf_dir, filename)
        if os.path.isfile(f):
            if "Jakub Zakrzewski" in f:
                output += output_msg("- " + filename)
                tmp_df = pd.read_excel(f)
                soerfs_submitted = pd.concat([soerfs_submitted, tmp_df])
    if soerfs_submitted.empty:
        output += output_msg("No SOERF have been submitted by you")
    else:
        soerfs_submitted = soerfs_submitted.iloc[:, [1, 2, 3, 4]]
        for index, row in soerfs_submitted.iterrows():
            r = row.apply(str).values
            output += output_msg(", ".join(r))
        output += output_msg(
            f"\nYou have submitted {soerfs_submitted.shape[0]} SOERFs today."
        )
    output += output_msg(f"SOERFs Requests in the submission folder: {soerf_count} \n")

    if server == False:
        await_char("y")
    else:
        return Markup(output)
