from backend.app.services.language_detector import detect_language
from backend.app.services.translator import (
    translate_to_english,
    translate_from_english,
)
from backend.app.services.memory import (
    get_history,
    add_message,
)
from backend.app.services.rag.rag_service import get_context
from backend.app.services.llm import generate_response


def process_chat(
    message: str,
    session_id: str,
):
    """
    Main chat pipeline.

    User
      ↓
    Detect Language
      ↓
    Translate to English
      ↓
    Retrieve Document Context
      ↓
    LLM
      ↓
    Translate Back
    """

    language = detect_language(message)

    if language != "en":
        english_message = translate_to_english(
            message,
            language,
        )
    else:
        english_message = message

    history = get_history(session_id)

    context = get_context(
        query=english_message,
        session_id=session_id,
    )

    response = generate_response(
        query=english_message,
        context=context,
        history=history,
    )

    add_message(
        session_id,
        "user",
        english_message,
    )

    add_message(
        session_id,
        "assistant",
        response,
    )

    if language != "en":
        response = translate_from_english(
            response,
            language,
        )

    return {
        "response": response,
        "language": language,
    }