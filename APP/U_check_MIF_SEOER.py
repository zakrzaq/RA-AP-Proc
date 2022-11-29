import os
import keyboard
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
            print('- ' + filename + '\n')
            tmp_df = pd.read_excel(f)
            mifs_submitted = pd.concat([mifs_submitted, tmp_df])
mifs_submitted = mifs_submitted.iloc[:, [1, 2, 3, 4]]
for index, row in mifs_submitted.iterrows():
    r = row.apply(str).values
    print(", ".join(r))
print('\nYou have submitted {} MIFs today.'.format(mifs_submitted.shape[0]))
print('MIFs Requests in the submission folder: {} \n'.format(mif_count))

tmp_df = pd.DataFrame()

print('SOERFs submitted:')
soerfs_submitted = pd.DataFrame()
for filename in os.listdir(soerf_dir):
    soerf_count += 1
    f = os.path.join(soerf_dir, filename)
    if os.path.isfile(f):
        if 'Jakub Zakrzewski' in f:
            print('- ' + filename + '\n')
            tmp_df = pd.read_excel(f)
            soerfs_submitted = pd.concat([soerfs_submitted, tmp_df])
soerfs_submitted = soerfs_submitted.iloc[:, [1, 2, 3, 4]]
for index, row in soerfs_submitted.iterrows():
    r = row.apply(str).values
    print(", ".join(r))
print('\nYou have submitted {} SOERFs today.'.format(
    soerfs_submitted.shape[0]))
print('SOERFs Requests in the submission folder: {} \n'.format(soerf_count))

print('Press Y to continue')
while True:
    if keyboard.is_pressed("y"):
        break
