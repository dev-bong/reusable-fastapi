from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import User
from app.schemas.user_schema import UserCreate
from app.core.security import get_password_hash


def create_user(session: Session, user_create: UserCreate) -> User:
    user = User(
        nickname=user_create.nickname,
        password=get_password_hash(user_create.password1),
        email=user_create.email,
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def get_user_by_nickname(session: Session, nickname: str) -> User:
    statement = select(User).filter_by(nickname=nickname)
    user = session.execute(statement).scalar_one_or_none()
    return user