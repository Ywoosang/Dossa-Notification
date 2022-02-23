import requests
import json
import os
from typing import Dict
 
class Auth:
    client_id = "<client-id>"
    file_path = f"{os.path.abspath(os.path.dirname(__file__))}/token.json"

    @classmethod
    def save_token(cls,access_token: str):
        """액세스 토큰 정보를 받아 json 파일에 저장한다.

        Args:
            access_token (str) : 발급한 액세스 토큰

        Returns:
        """
        with open(cls.file_path, "r") as json_file:
            token_info = json.load(json_file)
            token_info["access_token"] = access_token

        with open(cls.file_path, "w") as outfile:
            json.dump(token_info,outfile,indent=4)

    @classmethod
    def get_access_token(cls) -> str:
        """json 파일로부터 액세스 토큰 정보 읽어 반환한다.

        Args:
           
        Returns:
            str : 액세스 토큰
        """
        with open(cls.file_path, "r") as json_file:
            token_info = json.load(json_file)
            return token_info["access_token"]

    @classmethod
    def get_refresh_token(cls):
        """json 파일로부터 리프레시 토큰 정보 읽어 반환한다.

        Args:
           
        Returns:
            str : 리프레시 토큰
        """
        with open(cls.file_path, "r") as json_file:
            token_info = json.load(json_file)
            return token_info["refresh_token"]

    @classmethod
    def get_token_info(cls) -> Dict[str,str]:
        """액세스 토큰의 만료여부, 유효기간 등 정보를 확인한다. 

        Args:
           
        Returns:
            Dict[str,str] : 반환 예시 참조
            
            {
                'id': 2110957569, 
                'expiresInMillis': 14132012, 
                'expires_in': 14132, 
                'app_id': 701835, 
                'appId': 701835
            }
        """
        access_token = cls.get_access_token()
        url = "https://kapi.kakao.com/v1/user/access_token_info"
        headers = {
            "Authorization" : f"Bearer {access_token}"
        }
        response = requests.get(url=url,headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def update__token(cls):
        """액세스 토큰과 리프레시 토큰을 갱신한다.

        Args:
           
        Returns:
        
        """
        refresh_token = cls.get_refresh_token()
        print(refresh_token)
        url = "https://kauth.kakao.com/oauth/token"
        headers = {
            "Content-Type" : "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type" : "refresh_token",
            "client_id" : f"{cls.client_id}",
            "refresh_token" : f"{refresh_token}"
        }
        response = requests.post(url=url,headers=headers,data=data)
        if response.status_code == 200:
            token_info = response.json()
            # 리프레시 토큰 값은 만료 기간이 1개월 미만으로 남았을 때 갱신되어 전달되기 때문에 응답에 리프레시 토큰이 있는지 확인한다.
            # https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api 참고
            if "refresh_token" in token_info:
                cls.save_token(token_info["refresh_token"])
            cls.save_token(token_info["access_token"])
        else:
            print(f"request failed with status: {response.status_code}")

    @classmethod
    def get_tokens(cls) -> Dict[str,str]:
        """인가코드 를 통해 토큰 관련 정보를 반환하며 재실행 필요시 웹 브라우저를 통해 인가코드를 재발급 받아야 한다.
        https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#request-code 참고

        Args:

        Returns:
            Dict[str,str] : 반환 예시 참조

            {
                'access_token': 'zmQou5uWoCpFNkfuu4N2-R5eZAUpMYTVqHHi_Qopb9UAAAF-97vVNg', 
                'token_type': 'bearer', 
                'refresh_token': 'QhBJVrzDpsZU3mteae0xikZR5ob1bQ1CQ8_YAwopb9UAAAF-97vVNQ', 
                'expires_in': 21599,
                'scope': 'account_email profile_image talk_message profile_nickname', 
                'refresh_token_expires_in': 5183999
            }
        """
        url = "https://kauth.kakao.com/oauth/token"
        headers = {
            "Content-type" : "application/x-www-form-urlencoded;charset=utf-8"
        }
        data = {
            "grant_type" : "authorization_code",
            "client_id" : "86289e71b93e7d9f67f4dcfbe69bc44d",
            "redirect_uri" : "http://localhost:3000",
            # 일회성 인가코드
            "code" : "<code>"
        }
        response = requests.post(url=url,headers=headers,data=data)
        return response.json()

