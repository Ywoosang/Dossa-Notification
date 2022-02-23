from sqlalchemy import create_engine
import os

# echo = True 로 콘솔에서 쿼리 로그를 확인 가능
# DB 에 바로 연결하는 것이 아님. 메모리에 인식시키는 상황
BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
conection_string = "sqlite:///" + os.path.join(BASE_DIR, 'dossa.db') + "?check_same_thread=False"
engine = create_engine(conection_string, echo=False)