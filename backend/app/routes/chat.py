from fastapi import APIRouter

from backend.app.schemas.chat import ChatRequest, ChatResponse
from backend.app.services.chat_service import ChatService

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    response, detected_language = ChatService.chat(
        message=request.message,
        language=request.language,
    )

    return ChatResponse(
        response=response,
        language=detected_language,
    )