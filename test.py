from state.time import timer
from state.log import log
from utils.workbook import get_first_empty_row

timer.start()
log.load()
print('MIF max',log.ws_mif.max_row)
print('MIF get', get_first_empty_row(log.ws_mif, 'A'))
print(len(log.ws_mif['A']))

print('SOERF max', log.ws_soerf.max_row)
print('SOERF get', get_first_empty_row(log.ws_soerf, 'A'))
print(len(log.ws_soerf['A']))


timer.stop()
print(timer.get_elapsed_time())
