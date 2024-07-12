from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator
from pydantic_core.core_schema import FieldValidationInfo


class UserBase(BaseModel):
    nickname: str = Field(default=..., description="닉네임")
    email: EmailStr | None = Field(default=None, description="이메일")


class UserCreate(UserBase):
    password1: str = Field(default=..., description="비밀번호")
    password2: str = Field(default=..., description="비밀번호 재입력")

    @field_validator("password2")
    def passwords_match(cls, v, info: FieldValidationInfo):
        if "password1" in info.data and v != info.data["password1"]:
            raise ValueError("비밀번호가 일치하지 않습니다")
        return v


class UserPublic(UserBase):
    id: int = Field(default=..., description="유저 ID")
    join_date: datetime = Field(default=..., description="가입일시")

    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    nickname: str | None = Field(default=None, description="닉네임")
    email: EmailStr | None = Field(default=None, description="이메일")


class PasswordUpdate(BaseModel):
    current_password: str = Field(default=..., description="현재 비밀번호")
    new_password: str = Field(default=..., description="새 비밀번호")
