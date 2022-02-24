from config.config_db import engine
from sqlalchemy.orm import sessionmaker
from models.models import Category, Target

# 세션 생성
Session = sessionmaker(bind=engine)
session = Session()

# 카테고리 초기화
session.add(Category(name="휠셋"))
session.add(Category(name="완성차"))
session.add(Category(name="부품"))
session.add(Category(name="구동계"))
session.add(Category(name="용품/기타"))


# 키워드 등록
session.add(Target(keyword="캄파", category_id="1"))
session.add(Target(keyword="보라원", category_id="1"))
session.add(Target(keyword="비앙키", category_id="2"))
session.add(Target(keyword="펄스락", category_id="2"))
session.add(Target(keyword="피직 시라노", category_id="3"))
session.add(Target(keyword="슈퍼레코드", category_id="4"))
session.add(Target(keyword="튜블러", category_id="5"))
session.add(Target(keyword="컨티넨탈", category_id="5"))


# 데이터베이스에 반영
session.commit()
