from typing import Annotated

from sqlalchemy.orm import Session
from fastapi import HTTPException, Depends
from fastapi.security import (
    OAuth2PasswordRequestForm,
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from starlette import status

from app.core.db import SessionLocal
from app.models import User
from app.core import security
from app.crud import user_crud


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


SessionDep = Annotated[Session, Depends(get_db)]
PasswordFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenDep = Annotated[HTTPAuthorizationCredentials, Depends(HTTPBearer())]


def get_current_user(session: SessionDep, token: TokenDep) -> User:
    payload = security.decode_token(token=token.credentials)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="잘못된 토큰입니다."
        )

    current_user = user_crud.get_user_by_id(session=session, id=payload["sub"])
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 유저입니다."
        )
    return current_user


CurrentUser = Annotated[User, Depends(get_current_user)]
