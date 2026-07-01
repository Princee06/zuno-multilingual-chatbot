from groq import Groq

from backend.app.config.settings import GROQ_API_KEY, GROQ_MODEL
from backend.app.utils.prompt import SYSTEM_PROMPT

client = Groq(api_key=GROQ_API_KEY)


def generate_response(message: str) -> str:
    """
    Sends the user's message to Groq and returns the AI response.
    """

    try:
        chat_completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT,
                },
                {
                    "role": "user",
                    "content": message,
                },
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        return chat_completion.choices[0].message.content

    except Exception as e:
        return f"Error communicating with Groq API: {str(e)}"