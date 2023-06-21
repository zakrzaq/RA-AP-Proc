import time

from utils.helpers import elapsed_time
import utils.prompts as pr

class Timer:
    def __init__(self):
        self.start = 0.001
        self.end = 0.01

    def __repr__(self) -> str:
        return elapsed_time(self.end. self.start)

    def start(self) -> None:
        self.start = time.time()

    def stop(self) -> None:
        self.end = time.time()

    def result(self) -> str:
        return f"{pr.ok}Script completed: {elapsed_time(self.end, self.start)}"

timer = Timer()
