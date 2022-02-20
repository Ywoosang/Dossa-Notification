from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column, Integer, String, ForeignKey
import os
import sys

# 상위 패키지 정보를 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.config.config_db import engine

# 상속 클래스들을 자동으로 인지하고 매핑
Base = declarative_base()

class Category(Base):
    __tablename__ = "category"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    targets = relationship("Target", back_populates="category")
    posts = relationship("Post", back_populates="category")

    def __init__(self, name: str):
        self.name = name
 
    def __repr__(self):
        return f"Category {self.name}"

# 다대다 테이블
to_purchase = Table("to_perchase",
                    # defining tables using the old Table syntax, the metadata must be explicitly specified
                    Base.metadata,
                    Column("post_id", ForeignKey("post.id"),primary_key=True),
                    Column("target_id", ForeignKey("target.id"),primary_key=True)
                    )

class Target(Base):
    __tablename__ = "target"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = Column(Integer, primary_key=True)
    keyword = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship("Category", back_populates="targets")
    posts = relationship("Post", secondary=to_purchase, back_populates="targets")

    def __init__(self, keyword: str,category_id: int):
        self.keyword = keyword
        self.category_id = category_id

    def __repr__(self):
        return f"Target {self.keyword} {self.category}"

class Post(Base):
    __tablename__ = "post"
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    # 컬럼 타입이 숫자이고 기본키일때 자동으로 auto increment 가 설정
    id = Column(Integer, primary_key=True)
    # nullable 기본값은 Ture
    title = Column(String, nullable=False)
    price = Column(String, nullable=False)
    date = Column(String, nullable=False)
    link = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship("Category", back_populates="posts")
    # 다대다 연관
    targets = relationship("Target",secondary=to_purchase, back_populates="posts",cascade="all, delete")

    def __init__(self, title: str, price: str, date: str, link:str, category: Category):
        self.title = title
        self.price = price
        self.date = date
        self.link = link
        self.category = category
        self.targets = []

    def __repr__(self):
        return f"Post {self.title} {self.price} {self.date} {self.category} {self.targets}"
 
# 테이블 스키마 생성
# Base.metadata.create_all(engine)