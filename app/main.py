# 메인파일이 실행되고 나면 메인을 기준으로 절대경로가 잡힘
import sys
import os
import threading
# sys.path.append(os.path.dirname(__file__))
from scheduler.scheduler import Scheduler
if __name__ == "__main__":
    # 스레딩 이용
    print(dir())
    print(sys.path)
    thread = threading.Thread(target=Scheduler.schedule)
    thread.start()