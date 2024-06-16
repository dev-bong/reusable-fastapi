from starlette.config import Config


class Const:
    """
    ### 시스템에서 사용되는 각종 상수를 관리한다.
    * DB_USER : 데이터베이스 사용자
    * DB_PASSWORD : 데이터베이스 사용자 비밀번호
    * DB_HOST : 데이터베이스 호스트 주소
    * DB_DATABASE : 데이터베이스 이름
    """

    config = Config(".env")  # .env 파일 불러오기

    DB_USER = config("DB_USER")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_HOST = config("DB_HOST")
    DB_DATABASE = config("DB_DATABASE")


const = Const()
