import threading
import time
import psutil
import os

class MemoryMonitor(threading.Thread):
    def __init__(self, interval=0.1):
        super().__init__()
        self.interval = interval
        self.process = psutil.Process(os.getpid())
        self.max_memory = 0
        self.running = True

    def run(self):
        while self.running:
            mem = self.process.memory_info().rss
            self.max_memory = max(self.max_memory, mem)
            time.sleep(self.interval)

    def stop(self):
        self.running = False
        self.join()
        return self.max_memory
