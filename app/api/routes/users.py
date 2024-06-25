from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from starlette import status

from app.schemas import user_schema
from app.crud import user_crud
from app.core import security
from app.api.deps import SessionDep, TokenDep

router = APIRouter()


@router.post(
    "/signup",
    response_model=user_schema.UserPublic,
    status_code=status.HTTP_201_CREATED,
    summary="회원가입",
    description="신규 유저 회원가입",
)
def create_user(session: SessionDep, user_info: user_schema.UserCreate) -> Any:
    user = user_crud.get_user_by_nickname(session=session, nickname=user_info.nickname)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="중복되는 닉네임입니다."
        )
    user = user_crud.create_user(session=session, user_create=user_info)

    return user


@router.get(
    "/me",
    response_model=user_schema.UserPublic,
    summary="현재 회원 정보 조회",
    description="현재 로그인 되어있는 회원의 정보 조회",
)
def read_user_me(session: SessionDep, token: TokenDep) -> Any:
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
