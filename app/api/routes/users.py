from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from starlette import status

from app.schemas import user_schema
from app.crud import user_crud
from app.api.deps import SessionDep

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