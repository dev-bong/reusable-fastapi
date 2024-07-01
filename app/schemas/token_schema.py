from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(default=..., description="액세스 토큰")
    token_type: str = Field(default="bearer", description="토큰 유형")
