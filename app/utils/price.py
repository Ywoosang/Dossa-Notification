class PriceUtil:
    """게시물 가격 정보 포맷
    """
    @staticmethod
    def to_price(price_string: str) -> str:
        """가격 정보를 올바른 형식으로 변환한다.
        
        """
        characters = ["1. 판매(희망)금액 :","판매(희망)금액 :"]
        for index in range(len(characters)):
            price_string = price_string.replace(characters[index],"")

        # 15자 이하가 되도록 자름
        if len(price_string) > 15:
            price_string = price_string[0:15]
        
        price_string = price_string.strip()
        if price_string == "":
            price_string = "확인 요망"
        return price_string