import requests
from bs4 import BeautifulSoup
from sqlalchemy.orm import sessionmaker
from typing import Dict, List
from models.models import Post, Category
from utils.date import DateUtil
from utils.price import PriceUtil
from config.config_db import engine


class Scrapper:
    """도로앤싸이클 사이트로부터 게시글을 가져옴

    requests 라이브러리를 이용 도로앤싸이클 사이트의 해당 카테고리의 글들을 가져온다.
    http://corearoadbike.com/board/board.php?g_id=recycle02&t_id=Menu{category_code}Top6&page={page}
    """
    # key: 카테고리 일련번호, value: 카테고리명
    category_codes = {
        "30": "휠셋",
        "01": "완성차",
        "02": "부품",
        "31": "구동계"
    }

    @classmethod
    def get_today_posts(cls) -> Dict[str, List[Post]]:
        """ 특정 자전거 카테고리에서 지정한 키워드를 포함하는 페이지 게시글들을 반환한다.

        Args:

        Returns:
            List[Post] : 특정 키워드를 포함하는 Post 객체들 배열        
        """
        result = []
        print("start: 게시물 조회 시작")
        for category_code, category_name in cls.category_codes.items():
            page = 1
            is_today_post = True
            while is_today_post:
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
                }
                response = requests.get(
                    url=f'http://corearoadbike.com/board/board.php?g_id=recycle02&t_id=Menu{category_code}Top6&page={page}', headers=headers
                )
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    posts = soup.select('body > table.main_bg form > table')
                    # 페이지의 모든 글들에 대해 반복
                    for post in posts:
                        # 게시물 제목태그, 내용태그
                        title_tag = post.select_one('td.list_title_B')
                        link_tag = post.select_one('td.list_title_B a')
                        content_tag = post.select_one('td.list_content_B')
                        date_tag = post.select_one('.small_99')
                        if title_tag == None or content_tag == None:
                            continue

                        # 게시물 제목, 내용 추출
                        title = ''.join(
                            title_tag.get_text().split('\n')).strip()

                        # 게시물 링크 추출
                        link = "https://corearoadbike.com/board/" + \
                            link_tag["href"][2:]

                        # 게시물 가격 추출
                        price = PriceUtil.to_price(
                            content_tag.get_text().split('2. 사이즈')[0].strip())

                        # 게시물 작성 시간 추출
                        date = DateUtil.to_date(
                            date_tag.get_text().split('|')[1].strip())

                        # 이후 게시글부터 오늘자 게시글이 아닌 경우
                        if ':' not in date:
                            is_today_post = False
                            break

                        # 구매글과 판매글 중 판매글 정보만 선택해 결과 목록에 추가
                        if '판매' in title:
                            post = Post(title=title, price=price, date=date, link=link,
                                        category=Category(name=category_name))
                            
                            Session = sessionmaker(bind=engine)
                            session = Session()
                            is_exist = session.query(Post).filter(Post.title == post.title,Post.date == post.date).first()
                            # 조회 결과가 없다면 None
                            if is_exist:
                                return result

                            result.append(post)
                        else:
                            continue
                    page += 1
                else:
                    print("Error status:", response.status_code)

        print(f"end: 게시물 {len(result)}개 조회")
        return result