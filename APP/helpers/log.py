import os
from openpyxl import load_workbook
import dotenv
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


def load_log():
    log_file = os.environ['AP_LOG']
    return load_workbook(filename=log_file, keep_vba=True)


def save_log(log):
    print('saving live AP LOG...')
    log.save(os.environ['AP_LOG'])
    print('AP LOG saved')


def test_save(log, name='TEST_output'):
    print('saving to OUTPUT folder...')
    log.save(os.path.join(os.environ['APP_DIR'],
                          'OUTPUTS', '{}.xlsm'.format(name)))
    print('test file saved')
