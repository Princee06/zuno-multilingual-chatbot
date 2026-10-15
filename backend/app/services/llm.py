from groq import Groq

from backend.app.config.settings import GROQ_API_KEY, GROQ_MODEL
from backend.app.utils.prompt import SYSTEM_PROMPT, DOCUMENT_PROMPT
from backend.app.services.memory import add_message, get_history


client = Groq(api_key=GROQ_API_KEY)


def generate_response(
    message: str,
    session_id: str,
    context: str = "",
) -> str:
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    # Document excerpts are added only when this session has a document
    if context:
        messages.append(
            {
                "role": "system",
                "content": DOCUMENT_PROMPT.format(context=context),
            }
        )

    messages.extend(get_history(session_id))
    messages.append({"role": "user", "content": message})

    completion = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=messages,
        temperature=0.2,
        max_tokens=1024,
    )

    response = (
        completion.choices[0].message.content
        or "Sorry, I could not produce an answer. Please try again."
    )

    add_message(session_id, "user", message)
    add_message(session_id, "assistant", response)

    return response