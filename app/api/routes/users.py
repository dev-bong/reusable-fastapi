from typing import Any

from fastapi import APIRouter, HTTPException, Depends, Query, Path
from starlette import status

from app.schemas import user_schema, common_schema
from app.crud import user_crud
from app.api.deps import SessionDep, CurrentUser
from app.core import security

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
    summary="내 정보 조회",
    description="현재 로그인 되어있는 회원의 정보 조회",
)
def read_user_me(current_user: CurrentUser) -> Any:
    return current_user


@router.patch(
    "/me",
    response_model=user_schema.UserPublic,
    summary="내 정보 수정",
    description="현재 로그인 되어있는 회원의 정보 수정",
)
def update_user_me(
    session: SessionDep, user_info: user_schema.UserUpdate, current_user: CurrentUser
) -> Any:
    if user_info.nickname:
        user = user_crud.get_user_by_nickname(
            session=session, nickname=user_info.nickname
        )
        if user and user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="중복되는 닉네임입니다."
            )
    user = user_crud.update_user(
        session=session, user=current_user, user_update=user_info
    )

    return user


@router.patch(
    "/me/password",
    response_model=common_schema.Message,
    summary="내 비밀번호 수정",
    description="현재 로그인 되어있는 회원의 비밀번호 수정",
)
def update_password(
    session: SessionDep,
    passwords: user_schema.PasswordUpdate,
    current_user: CurrentUser,
) -> Any:
    if not security.verify_password(
        plain_password=passwords.current_password, hashed_password=current_user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="잘못된 비밀번호입니다."
        )
    user_crud.update_user_password(
        session=session, user=current_user, new_password=passwords.new_password
    )

    return common_schema.Message(message="비밀번호가 변경되었습니다.")


@router.delete(
    "/me",
    response_model=common_schema.Message,
    summary="내 계정 삭제",
    description="현재 로그인 되어있는 회원 탈퇴",
)
def delete_user_me(session: SessionDep, current_user: CurrentUser) -> Any:
    # todo : 플래그값만 바꾸는 식으로 변경?
    user_crud.delete_user(session=session, user=current_user)

    return common_schema.Message(message="회원 탈퇴가 완료되었습니다.")
