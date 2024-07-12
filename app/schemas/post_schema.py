from datetime import datetime

from pydantic import BaseModel, Field


class PostCreate(BaseModel):
    subject: str = Field(default=..., description="게시글 제목")
    content: str = Field(default=..., description="게시글 내용")


class PostUpdate(BaseModel):
    subject: str | None = Field(default=None, description="게시글 제목")
    content: str | None = Field(default=None, description="게시글 내용")


class PostSimple(BaseModel):
    id: int = Field(default=..., description="게시글 ID")
    subject: str = Field(default=..., description="게시글 제목")
    create_date: datetime = Field(default=..., description="작성일시")
    user_id: int = Field(default=..., description="작성한 유저 ID")
    nickname: str = Field(default=..., description="작성한 유저 닉네임")


class PostDetail(PostSimple):
    content: str = Field(default=..., description="게시글 내용")


class PostList(BaseModel):
    post_list: list[PostSimple] = Field(default=..., description="게시글 목록")
