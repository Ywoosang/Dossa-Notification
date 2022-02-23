from models.models import Post
from auth.auth import Auth
import requests
import json
import os
import sys

# 상위 패키지 정보를 추가
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))


class Messenger:
    """카카오톡 메신저 전송 

    관심 키워드가 포함된 도로앤싸이클 신규 게시글을 전송
    애플리케이션에서 에러가 발생한 경우 해당 에러를 전송 
    """
     
    request_count = 0

    @classmethod
    def kakao_talk_post(cls, post: Post) -> None:
        """게시글 관련 카카오톡 메시지를 전송한다.

        Args:
            post : 메시지로 보낼 게시글 내용을 담고 있는 Post 객체
        """
        token = Auth.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "object_type": "text",
            "text": f"{post.title}\n 가격: {post.price}\n 작성일: {post.date}\n 확인하기: {post.link}",
            "link": {
                "web_url": "http://corearoadbike.com/board/board.php?g_id=recycle02&t_id=Menu01Top6&no=1025612",
                "mobile_web_url": "http://corearoadbike.com/board/board.php?g_id=recycle02&t_id=Menu01Top6&no=1025612"
            },
            "button_title": "게시물 확인"
        }
        data = {
            "template_object":  json.dumps(body, ensure_ascii=False)
        }

        response = requests.post(
            "https://kapi.kakao.com/v2/api/talk/memo/default/send", headers=headers, data=data)
        try:
            response.raise_for_status()
            print(f"{post} 전송 완료")
            cls.request_count = 0
            if response.json()["result_code"] != 0:
                raise Exception("MESSAGE SEND FAILED")
        except Exception as e:
            print(e)
            if response.status_code == 401:
                Auth.update__token()
                if cls.request_count < 3:
                    cls.kakao_talk(post)
                # 호출수가 3 회 이상이라면 문제 발생한것
                else:
                    sys.exit()

    @classmethod
    def kakao_talk_error(cls, e: Exception) -> None:
        """에러 관련 카카오톡 메시지를 전송한다.

        Args:
            e : 메시지로 보낼 게시글 내용을 담고 있는 error 객체
            
        """
        token = Auth.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        body = {
            "object_type": "text",
            "text": f"에러 발생: {e}",
            "link": {
            },
            "button_title": "에러 확인"
        }
        data = {
            "template_object":  json.dumps(body, ensure_ascii=False)
        }

        response = requests.post(
            "https://kapi.kakao.com/v2/api/talk/memo/default/send", headers=headers, data=data)
        try:
            response.raise_for_status()
            cls.request_count = 0
            if response.json()["result_code"] != 0:
                raise Exception("MESSAGE SEND FAILED")
        except Exception as e:
            print(e)
            if response.status_code == 401:
                Auth.update__token()
                if cls.request_count < 3:
                    cls.kakao_talk(e)
                # 호출수가 3 회 이상이라면 문제 발생한것
                else:
                    sys.exit()
