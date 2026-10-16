import os
import tempfile

from fastapi import APIRouter, File, Form, UploadFile

from backend.app.schemas.chat import ChatResponse
from backend.app.services.chat_service import process_chat
from backend.app.services.memory import clear_history
from backend.app.services.rag.pipeline import ingest_document

router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)


@router.post("", response_model=ChatResponse)
async def chat(
    message: str = Form(...),
    session_id: str = Form(...),
    preferred_language: str = Form(""),
    file: UploadFile | None = File(None),
):
    if file:
        suffix = os.path.splitext(file.filename)[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as temp:
            temp.write(await file.read())
            temp_path = temp.name

        try:
            ingest_document(temp_path, session_id)
        finally:
            os.remove(temp_path)

    result = process_chat(message, session_id, preferred_language)

    return ChatResponse(
        response=result["response"],
        language=result["language"],
    )


@router.delete("/reset/{session_id}")
async def reset_chat(session_id: str):
    clear_history(session_id)

    return {
        "message": "Conversation reset successfully."
    }