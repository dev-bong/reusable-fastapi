from pydantic import BaseModel, Field


class Token(BaseModel):
    access_token: str = Field(default=..., title="액세스 토큰")
    token_type: str = Field(default="bearer", title="토큰 유형")
