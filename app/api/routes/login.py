from typing import Any

from fastapi import APIRouter, HTTPException, Depends
from starlette import status

from app.schemas import token_schema
from app.crud import user_crud
from app.api.deps import SessionDep, PasswordFormDep
from app.core import security


router = APIRouter()


@router.post(
    "/login",
    response_model=token_schema.Token,
    status_code=status.HTTP_201_CREATED,
    summary="로그인",
    description="로그인해서 JWT 토큰 받기",
)
def login_access_token(session: SessionDep, form_data: PasswordFormDep) -> Any:
    user = user_crud.authenticate(
        session=session, nickname=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="잘못된 닉네임 또는 비밀번호입니다.",
        )

    return token_schema.Token(access_token=security.create_access_token(sub=user.id))
