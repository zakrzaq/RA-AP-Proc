import os
from helpers.helpers import use_dotenv

use_dotenv()

sap_data_files = {
    "mara": os.path.join(os.environ["DIR_IN"], "MARA.XLSX"),
    "marc": os.path.join(os.environ["DIR_IN"], "MARC.XLSX"),
    "mvke": os.path.join(os.environ["DIR_IN"], "MVKE.XLSX"),
    "ausp": os.path.join(os.environ["DIR_IN"], "AUSP.XLSX"),
    "mlan": os.path.join(os.environ["DIR_IN"], "MLAN.XLSX"),
    "gts": os.path.join(os.environ["DIR_IN"], "GTS.XLSX"),
    "price": os.path.join(os.environ["DIR_IN"], "PRICE.XLSX"),
    "text": os.path.join(os.environ["DIR_IN"], "sales_text.XLS"),
}
