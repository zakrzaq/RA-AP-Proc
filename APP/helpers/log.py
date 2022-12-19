import os
from openpyxl import load_workbook
import dotenv
dotenv_file = dotenv.find_dotenv()
dotenv.load_dotenv(dotenv_file)


log_file = os.environ['AP_LOG']

log = load_workbook(filename=log_file, keep_vba=True)


def save_log(log):
    print('saving live AP LOG...')
    log.save(os.environ['AP_LOG'])
    print('AP LOG saved')
