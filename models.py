'''
데이터베이스 테이블 구성
'''
from typing import Optional, List
import datetime

from sqlalchemy import String, Text, ForeignKey, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime.datetime: TIMESTAMP(timezone=True),
    }


class User(Base):  # 사용자 테이블
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[Optional[str]]
    join_date: Mapped[datetime.datetime] = mapped_column(insert_default=func.now())

    posts: Mapped[List["Post"]] = relationship(back_populates="user")


class Post(Base):  # 게시글 테이블
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    subject: Mapped[str]
    content: Mapped[Optional[str]] = mapped_column(Text)
    create_date: Mapped[datetime.datetime] = mapped_column(insert_default=func.now())

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    user: Mapped["User"] = relationship(back_populates="posts")
