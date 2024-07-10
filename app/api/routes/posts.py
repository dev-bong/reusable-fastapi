from typing import Any

from fastapi import APIRouter, HTTPException, Query, Path
from starlette import status

from app.schemas import post_schema
from app.crud import post_crud
from app.api.deps import SessionDep, CurrentUser

router = APIRouter()


@router.post(
    "/",
    response_model=post_schema.PostDetail,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 쓰기",
    description="게시글 쓰기",
)
def create_post(
    session: SessionDep, current_user: CurrentUser, post_in: post_schema.PostCreate
) -> Any:
    post = post_crud.create_post(
        session=session, post_create=post_in, user_id=current_user.id
    )
    return {**post.__dict__, "user_id": post.user.id, "nickname": post.user.nickname}


@router.get(
    "/",
    response_model=post_schema.PostList,
    summary="게시글 목록 읽기",
    description="게시글 목록 읽기",
)
def read_posts(
    session: SessionDep,
    page: int = Query(default=1, description="페이지 번호", ge=1),
    size: int = Query(
        default=10, description="페이지 크기 (한 페이지에 표시할 코드 수)", ge=1
    ),
) -> Any:
    posts = post_crud.get_posts(session=session, page=page, size=size)
    post_list = []
    for post in posts:
        post_list.append(
            {
                "id": post.id,
                "subject": post.subject,
                "create_date": post.create_date,
                "user_id": post.user.id,
                "nickname": post.user.nickname,
            }
        )

    return {"post_list": post_list}


@router.get(
    "/{id}",
    response_model=post_schema.PostDetail,
    summary="게시글 읽기",
    description="id로 게시글 1개 상세 읽기",
)
def read_post(
    session: SessionDep, id: int = Path(default=..., description="게시글 ID")
) -> Any:
    post = post_crud.get_post(session=session, id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 게시글입니다."
        )

    return {**post.__dict__, "user_id": post.user.id, "nickname": post.user.nickname}


@router.patch(
    "/{id}",
    response_model=post_schema.PostDetail,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 수정하기",
    description="자신이 쓴 게시글 수정하기",
)
def update_post(
    session: SessionDep,
    current_user: CurrentUser,
    post_in: post_schema.PostUpdate,
    id: int = Path(default=..., description="게시글 ID"),
):
    post = post_crud.get_post(session=session, id=id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 게시글입니다."
        )
    if post.user.id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="해당 게시글을 수정할 권한이 없습니다.",
        )

    post = post_crud.update_post(session=session, post=post, post_update=post_in)
    return {**post.__dict__, "user_id": post.user.id, "nickname": post.user.nickname}
