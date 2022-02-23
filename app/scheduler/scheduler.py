from sqlalchemy.orm import sessionmaker
import time
from scrapper.scrapper import Scrapper
from models.models import Target
from config.config_db import engine
from messanger.messenger import Messenger


class Scheduler:
    """특정 시간마다 카카오톡 메시지를 전송하는 작업을 실행

    schedule 에서 5분마다 task 를 실행
    task 에서 카카오톡으로 관심 키워드가 포함된 게시글을 전송

    """
    @classmethod
    def task(cls, messanger: Messenger) -> None:
        """카카오톡으로 관심 키워드가 포함된 게시글을 전송

        Args:
            messenger: 카카오톡 메신저 전송 클래스

        Note:
            긁어온 페이지 게시글중 지정한 키워드가 포함된 게시글이 있는지 확인한다.
            지정한 키워드가 포함된 게시글이 있다면 해당 게시글이 데이터베이스에 존재하는지 판별한다.
            존재 하지 않는 게시글이라면 카카오톡으로 해당 게시글에 대한 정보를 전송한다.
        """
        posts = Scrapper.get_today_posts()
        for post in posts:
            Session = sessionmaker(bind=engine)
            session = Session()
            targets = session.query(Target).all()
            for target in targets:
                if target.keyword in post.title and post.category.name == target.category.name:
                    post.targets.append(target)

            if len(post.targets) != 0:
                messanger.kakao_talk_post(post)
                session.commit()
                session.close()

    @classmethod
    def schedule(cls) -> None:
        """지정한 시간마다 task 를 실행

        Args:

        Returns:
        """
        while True:
            cls.task(messanger=Messenger)
            time.sleep(30)
