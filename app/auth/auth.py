import requests
import json
from typing import Dict, List
from config.config_secret import secret_file_path


class Auth:
    @classmethod
    def get_secret(cls, secret_types: List[str]) -> Dict[str,str]:
        """json 파일로부터 요구되는 시크릿키 목록을 읽어 반환한다.

        Args:
            secret_types : 요구되는 시크릿 키 이름들을 담은 배열

        Returns:
            요구되는 시크릿 키 정보를 담은 딕셔너리
            example:

            {
                "access_token" : "86289e71b93e7d9f67f4dcfbe69bc44d"
                "client_id" : "86289e71b93e7d9f67f4dcfbe6123w4d"
            }
        """
        with open(secret_file_path, "r") as json_file:
            secret_info = json.load(json_file)
            return dict(filter(
                lambda secret:  True if secret[0] in secret_types else False, secret_info.items()))

    @classmethod
    def save_token(cls, access_token: str) -> None:
        """액세스 토큰 정보를 받아 json 파일에 저장한다.

        Args:
            access_token (str) : 발급한 액세스 토큰
        """
        with open(secret_file_path, "r") as json_file:
            secret_info = json.load(json_file)
            secret_info["access_token"] = access_token

        with open(secret_file_path, "w") as outfile:
            json.dump(secret_info, outfile, indent=4)

    @classmethod
    def get_access_token_info(cls) -> Dict[str, str]:
        """액세스 토큰의 만료여부, 유효기간 등 정보를 확인한다. 

        Returns:
            엑세스 토큰 관련 정보를 담은 딕셔너리
            example:

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
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(url=url, headers=headers)
        if response.status_code == 200:
            return response.json()

    @classmethod
    def update_token(cls) -> None:
        """액세스 토큰과 리프레시 토큰을 갱신한다.
        """
        secret = cls.get_secret(['client_id','refresh_token'])
        url = "https://kauth.kakao.com/oauth/token"
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "refresh_token",
            "client_id": f"{secret['client_id']}",
            "refresh_token": f"{secret['refresh_token']}"
        }
        response = requests.post(url=url, headers=headers, data=data)
        if response.status_code == 200:
            token_info = response.json()
            # 리프레시 토큰 값은 만료 기간이 1개월 미만으로 남았을 때 갱신되어 전달되기 때문에 응답에 리프레시 토큰이 있는지 확인한다.
            # https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api 참고
            if "refresh_token" in token_info:
                cls.save_token(token_info['refresh_token'])
            cls.save_token(token_info['access_token'])
        else:
            print(f"request failed with status: {response.status_code}")

    @classmethod
    def get_tokens(cls) -> Dict[str, str]:
        """인가코드 를 통해 토큰 관련 정보를 반환하며 재실행 필요시 웹 브라우저를 통해 인가코드를 재발급 받아야 한다.
        https://developers.kakao.com/docs/latest/ko/kakaologin/rest-api#request-code 참고

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
        secret = cls.get_secret(["code"])
        headers = {
            "Content-type": "application/x-www-form-urlencoded;charset=utf-8"
        }
        data = {
            "grant_type": "authorization_code",
            "client_id": "86289e71b93e7d9f67f4dcfbe69bc44d",
            "redirect_uri": "http://localhost:3000",
            # 일회성 인가코드
            "code": f"{secret['code']}"
        }
        response = requests.post(url=url, headers=headers, data=data)
        return response.json()


#  직접 실행시 토큰 정보 확인
if __name__ == "__main__":
    print(Auth.get_tokens())
