from datetime import datetime

from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    nickname: str = Field(default=..., title="닉네임")
    email: EmailStr | None = Field(default=None, title="이메일")


class UserCreate(UserBase):
    password1: str = Field(default=..., title="비밀번호")
    password2: str = Field(default=..., title="비밀번호 재입력")


class UserPublic(UserBase):
    id: int = Field(default=..., title="유저 ID")
    join_date: datetime = Field(default=..., title="가입일시")

    class Config:
        from_attributes = True
