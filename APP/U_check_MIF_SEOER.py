import os
import keyboard
import dotenv
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)

report_directory = os.environ["EDM_DRIVE"]

mif = os.path.join(report_directory, 'MIFs awaiting processing')
soerf = os.path.join(report_directory, 'SOERFs awaiting processing')
mif_count = 0
soerf_count = 0

print('\nMIFs submitted:')
for filename in os.listdir(mif):
    mif_count += 1
    f = os.path.join(mif, filename)
    if os.path.isfile(f):
        if 'Jakub Zakrzewski' in f:
            print('- ' + filename + '\n')
print('MIFs in the submission folder: {} \n'.format(mif_count))

print('SOERFs submitted:')
for filename in os.listdir(soerf):
    soerf_count += 1
    f = os.path.join(soerf, filename)
    if os.path.isfile(f):
        if 'Jakub Zakrzewski' in f:
            print('- ' + filename + '\n')
print('SOERFs in the submission folder: {} \n'.format(soerf_count))

print('Press Y to continue')
while True:
    if keyboard.is_pressed("y"):
        break
