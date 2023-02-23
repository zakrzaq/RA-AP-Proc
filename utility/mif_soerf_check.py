def mif_soerf_check(server=False):
    import os
    import pandas as pd

    from helpers.helpers import end_script, use_dotenv
    from state.output import output
    import helpers.prompts as pr

    use_dotenv()
    output.reset()

    report_directory = os.environ["EDM_DRIVE"]

    mif_dir = os.path.join(report_directory, "MIFs awaiting processing")
    soerf_dir = os.path.join(report_directory, "SOERFs awaiting processing")
    mif_count = 0
    soerf_count = 0

    output.add(f"{pr.ok}MIFs submitted:", ["code-line", "bold"])
    mifs_submitted = pd.DataFrame()
    for filename in os.listdir(mif_dir):
        mif_count += 1
        f = os.path.join(mif_dir, filename)
        if os.path.isfile(f):
            if "Jakub Zakrzewski" in f:
                output.add(f"{pr.file}{filename}")
                tmp_df = pd.read_excel(f)
                mifs_submitted = pd.concat([mifs_submitted, tmp_df])
    if mifs_submitted.empty:
        output.add(f"{pr.cn}No MIF have been submitted by you")
    else:
        mifs_submitted = mifs_submitted.iloc[:, [1, 2, 3, 4]]
        for index, row in mifs_submitted.iterrows():
            r = row.apply(str).values
            output.add(f"{pr.prmt}{r}")
        output.add(f"{pr.done}You have submitted {mifs_submitted.shape[0]} MIFs today.")
    output.add(f"{pr.info}MIFs Requests in the submission folder: {mif_count} \n")

    tmp_df = pd.DataFrame()

    output.add(f"SOERFs submitted:", ["code-line", "bold"])
    soerfs_submitted = pd.DataFrame()
    for filename in os.listdir(soerf_dir):
        soerf_count += 1
        f = os.path.join(soerf_dir, filename)
        if os.path.isfile(f):
            if "Jakub Zakrzewski" in f:
                output.add(f"{pr.file}{filename}")
                tmp_df = pd.read_excel(f)
                soerfs_submitted = pd.concat([soerfs_submitted, tmp_df])
    if soerfs_submitted.empty:
        output.add(f"{pr.cn}No SOERF have been submitted by you")
    else:
        soerfs_submitted = soerfs_submitted.iloc[:, [1, 2, 3, 4]]
        for index, row in soerfs_submitted.iterrows():
            r = row.apply(str).values
            output.add(f"{pr.prmt}{r}")
        output.add(
            f"{pr.done}You have submitted {soerfs_submitted.shape[0]} SOERFs today."
        )
    output.add(f"{pr.info}SOERFs Requests in the submission folder: {soerf_count} \n")

    return end_script(server)
