from typing import Optional

from pydantic import BaseModel


class ChatRequest(BaseModel):
    message: str
    language: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    language: str