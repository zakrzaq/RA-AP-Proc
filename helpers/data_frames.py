import os
import pandas as pd

from helpers.helpers import use_dotenv

use_dotenv()


def get_active():
    return pd.read_excel(os.environ['AP_LOG'],
                         sheet_name='Active Materials', dtype=str)


def get_selected_active():
    active = get_active()
    return active[['Date Added', 'target sorg', 'target plant', 'email prefix\n(from request form)', 'SAP MATNR\n(from request form)', 'Service Requested\n(from request form)', 'Location\n(from request form)', 'Catalog', 'Ser', 'MTART/GenItemCat', ' sorg1k dchain', ' sorg1k cs', 'sorg1k price', ' sorg4k dchain', ' sorg4k cs', 'PGC', 'target sorg price', 'target sorg dchain', 'target sorg DWERK', 'target sorg cs', 'target sorg pub', 'target plant status',
                   'target plant mrp type', 'DWERK Plant Status', 'DWERK Plant Code', "mif/soerf check", 'Sales Text', 'INDIA GST\nINHTS', 'INDIA GST\nmarc.stuec', 'INDIA GST taxm1', 'STATUS_CHINA_ENERGY_LBL', "Regulatory Cert\n(Z62 Class)", 'Regulatory Cert\n(Z62 Characteristic)', 'Z62 characteristic\n(assigned in SAP)', 'PCE Assessment\n(received)', 'Date of PCE review', 'MIF Submitted', 'SOERF Submitted', 'pricing request', 'PCE cert rev req\'d', 'status', 'sort order']]
