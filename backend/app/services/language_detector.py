import re
from langdetect import detect


# -----------------------------------
# Unicode Script Detection
# -----------------------------------

SCRIPT_RANGES = {
    "te": r"[\u0C00-\u0C7F]",   # Telugu
    "hi": r"[\u0900-\u097F]",   # Hindi / Devanagari
    "ta": r"[\u0B80-\u0BFF]",   # Tamil
    "kn": r"[\u0C80-\u0CFF]",   # Kannada
    "ml": r"[\u0D00-\u0D7F]",   # Malayalam
    "gu": r"[\u0A80-\u0AFF]",   # Gujarati
    "bn": r"[\u0980-\u09FF]",   # Bengali
    "pa": r"[\u0A00-\u0A7F]",   # Punjabi
    "or": r"[\u0B00-\u0B7F]",   # Odia
}


def detect_script(text: str):
    """
    Detects whether the input contains a native Indian script.
    """

    for lang, pattern in SCRIPT_RANGES.items():
        if re.search(pattern, text):
            return lang

    return None


def detect_language(text: str):
    """
    Detects:
    - Native Indian languages
    - English
    - Unknown Roman text (handled later)
    """

    script = detect_script(text)

    if script:
        return {
            "language": script,
            "style": "native"
        }

    try:
        lang = detect(text)

        if lang == "en":
            return {
                "language": "en",
                "style": "english"
            }

        return {
            "language": lang,
            "style": "native"
        }

    except Exception:
        return {
            "language": "unknown",
            "style": "unknown"
        }