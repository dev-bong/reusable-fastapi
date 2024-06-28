from pydantic import BaseModel, Field


class Message(BaseModel):
    message: str = Field(default=..., title="메시지")
