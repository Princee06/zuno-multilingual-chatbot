from backend.app.services.language_detection import detect_language
from backend.app.services.llm import generate_response


class ChatService:

    @staticmethod
    def chat(message: str, language: str | None = None) -> tuple[str, str]:
        """
        Complete chat workflow.
        """

        detected_language = language

        if not detected_language:
            detected_language = detect_language(message)

        response = generate_response(message)

        return response, detected_language