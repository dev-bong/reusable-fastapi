from sqlalchemy import create_engine
from sqlalchemy import URL
from sqlalchemy.orm import sessionmaker

from const import const

db_url_object = URL.create(
    "postgresql+psycopg2",
    username=const.DB_USER,
    password=const.DB_PASSWORD,
    host=const.DB_HOST,
    database=const.DB_DATABASE,
)

engine = create_engine(db_url_object)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)  # ? autocommit=False : 데이터 변경 후 commit()을 해야만 데이터베이스에 적용
