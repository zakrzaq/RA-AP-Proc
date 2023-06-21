from state.log import log
from utils.workbook import get_first_empty_row

log.load()
print("Loaded? ", log.loaded)
last_row = get_first_empty_row(log.ws_mif, "A")
print(last_row)
