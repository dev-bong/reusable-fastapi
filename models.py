"""
ORM models mapping
"""

from typing import Optional, List
from typing_extensions import Annotated
from datetime import datetime

from sqlalchemy import String, Text, ForeignKey, TIMESTAMP
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


# mapped_column() overrides
int_pk = Annotated[int, mapped_column(primary_key=True)]
user_fk = Annotated[int, mapped_column(ForeignKey("user.id"))]
str30 = Annotated[str, mapped_column(String(30))]
text = Annotated[str, mapped_column(Text)]
date = Annotated[datetime, mapped_column(TIMESTAMP(timezone=True))]


class Base(DeclarativeBase):
    pass


class User(Base):  # 사용자 테이블
    __tablename__ = "user"

    id: Mapped[int_pk]
    nickname: Mapped[str30] = mapped_column(unique=True)
    email: Mapped[Optional[str]]
    join_date: Mapped[date] = mapped_column(insert_default=func.now())

    posts: Mapped[List["Post"]] = relationship(back_populates="user")


class Post(Base):  # 게시글 테이블
    __tablename__ = "post"

    id: Mapped[int_pk]
    subject: Mapped[str]
    content: Mapped[Optional[text]]
    create_date: Mapped[date] = mapped_column(insert_default=func.now())

    user_id: Mapped[user_fk]
    user: Mapped["User"] = relationship(back_populates="posts")
