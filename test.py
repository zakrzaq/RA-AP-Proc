from state.time import timer
from time import sleep

timer.start()
sleep(5.2)
timer.stop()
print(timer.get_elapsed_time())

