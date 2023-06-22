import time

class Timer:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        self.end_time = time.time()

    def get_elapsed_time(self):
        if self.start_time is None or self.end_time is None:
            return ""
        else:
            elapsed_time = self.end_time - self.start_time
            minutes = int(elapsed_time // 60)
            seconds = int(elapsed_time % 60)
            return f"{minutes}m {seconds}s"

timer = Timer()
