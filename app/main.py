import threading
from scheduler.scheduler import Scheduler

if __name__ == "__main__":
    thread = threading.Thread(target=Scheduler.schedule)
    thread.start()