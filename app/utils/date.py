from time import localtime

class DateUtil:
    """게시물 작성 시간 포맷
    """
    @staticmethod
    def to_date(date_string: str) -> str:
        """ 게시물 작성 시간을 년/월/일 시:분:초 형식으로 변환한다.

        Args:
            date_string : 도로앤사이클 페이지에서 가져온 시:분:초
        """
        date = localtime()
        return f"{date.tm_year}/{date.tm_mon}/{date.tm_mday} {date_string}"