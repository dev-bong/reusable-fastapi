from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models import User
from app.schemas.user_schema import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


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


def get_user_by_nickname(session: Session, nickname: str) -> User | None:
    statement = select(User).filter_by(nickname=nickname)
    user = session.execute(statement).scalar_one_or_none()
    return user


def get_user_by_id(session: Session, id: int) -> User | None:
    return session.get(User, id)


def authenticate(session: Session, nickname: str, password: str) -> User | None:
    user = get_user_by_nickname(session=session, nickname=nickname)
    if not user or not verify_password(password, user.password):
        return None
    return user


def update_user(session: Session, user: User, user_update: UserUpdate) -> User:
    if user_update.email:
        user.email = user_update.email
    if user_update.nickname:
        user.nickname = user_update.nickname

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def update_user_password(session: Session, user: User, new_password: str) -> None:
    user.password = get_password_hash(new_password)

    session.add(user)
    session.commit()


def delete_user(session: Session, user: User) -> None:
    session.delete(user)
    session.commit()
