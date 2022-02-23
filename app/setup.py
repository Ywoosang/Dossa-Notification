from app.config.config_db import engine
from sqlalchemy.orm import sessionmaker
from models.models import Category

Session = sessionmaker(bind=engine)
session = Session()

# 카테고리 초기화
session.add(Category(name="휠셋"))
session.add(Category(name="완성차"))
session.add(Category(name="부품"))
session.add(Category(name="구동계"))

session.commit()





