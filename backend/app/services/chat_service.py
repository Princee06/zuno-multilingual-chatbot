from backend.app.services.language_detector import detect_language
from backend.app.services.translator import (
    translate_to_english,
    translate_from_english,
)
from backend.app.services.transliterator import roman_to_native
from backend.app.services.rag.rag_service import get_context
from backend.app.services.llm import generate_response


def process_chat(
    message: str,
    session_id: str,
    preferred_language: str = "",
):
    detected = detect_language(message, preferred_language)

    language = detected["language"]
    style = detected["style"]

    if language in ("en", "unknown"):
        language = "en"
        english_message = message
    else:
        source_text = message

        # Romanized input is converted to native script before translating
        if style == "roman":
            source_text = roman_to_native(message, language)

        english_message = translate_to_english(source_text, language)

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
        response = translate_from_english(response, language)

    return {
        "response": response,
        "language": language,
    }