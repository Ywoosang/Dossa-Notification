import unittest
from unittest.mock import MagicMock
import os
import sys
import re
from typing import List
from sqlalchemy.orm.base import object_mapper

 

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from app.scrapper.scrapper import Scrapper
from app.models.models import Post

class ScrapperTest(unittest.TestCase):
    """
    Scrapper 클래스
    """
    @classmethod
    def setUpClass(cls) -> None:
        # When
        cls.posts: List[Post] = Scrapper.get_today_posts()
    
    def test_post_object(self):
        """
        반환된 Post 오브젝트는 sqlalchemy 모델 객체여야 한다.
        """
        # Then
        def is_mapped(obj):
            try:
                object_mapper(obj)
            except:
                return False
            return True

        for post in ScrapperTest.posts:
            self.assertTrue(is_mapped(post))

    def test_today_date(self):
        """
        게시글들은 제목, 링크, 가격을 가져야 한다.
        """
        # Then 
        for post in ScrapperTest.posts:
            # bool(None) == False
            self.assertTrue(post.title)
            self.assertTrue(post.link)
            self.assertTrue(post.price)
            self.assertTrue(post.date)

    def test_no_targets(self):
        """
        게시글들에 Target 이 등록되지 않아야 한다.
        """
        # Then 
        for post in ScrapperTest.posts:
            self.assertFalse(post.targets)

    def test_today_post(self):
        """
        게시글을 오늘 일자로 년/월/일 시:분:초 형식을 따라야 한다.

        ex)
        2022/2/19 13:45:05
        2022/2/20 01:11:10
        """
        for post in ScrapperTest.posts:
            self.assertRegex(post.date,r"^(?P<year>20\d{2})/(?P<month>[1-9]{1}|1[012])/(?P<day>[1-9]{1}|[1-2]{1}[0-9]{1}|3[01])\s(?P<hour>0[0-9]|1[0-9]|2[0-3]):(?P<minute>0[0-9]|[1-5]{1}[0-9]{1}):(?P<second>0[0-9]|[1-5]{1}[0-9]{1})$")
