from backend.app.services.language_detector import detect_language
from backend.app.services.translator import (
    translate_to_english,
    translate_from_english,
)
from backend.app.services.rag.rag_service import get_context
from backend.app.services.llm import generate_response


def process_chat(
    message: str,
    session_id: str,
):
    """
    Main chat pipeline.

    1. Detect the language of the message
    2. Translate to English if needed
    3. Retrieve context from the uploaded document
    4. Generate a reply with the LLM, which also saves memory
    5. Translate the reply back to the user's language
    """

    detected = detect_language(message)

    language = detected["language"]

    if language in ("en", "unknown"):
        language = "en"
        english_message = message
    else:
        english_message = translate_to_english(
            message,
            language,
        )

    context = get_context(
        query=english_message,
        session_id=session_id,
    )

    response = generate_response(
        message=english_message,
        session_id=session_id,
        context=context,
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