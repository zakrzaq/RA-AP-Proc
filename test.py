from state.time import timer
from utils.submissions import send_extensions

timer.start()

send_extensions()


timer.stop()
print(timer.get_elapsed_time())
