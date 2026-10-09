from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

# Language mapping

SCRIPT_CODES = {
    "hi": sanscript.DEVANAGARI,
    "te": sanscript.TELUGU,
    "ta": sanscript.TAMIL,
    "kn": sanscript.KANNADA,
    "ml": sanscript.MALAYALAM,
    "mr": sanscript.DEVANAGARI,
    "bn": sanscript.BENGALI,
    "gu": sanscript.GUJARATI,
    "pa": sanscript.GURMUKHI,
}


def roman_to_native(text: str, language: str) -> str:
    """
    Converts Romanized Indian language into its native script.
    """

    if language not in SCRIPT_CODES:
        return text

    return transliterate(
        text,
        sanscript.ITRANS,
        SCRIPT_CODES[language],
    )


def native_to_roman(text: str, language: str) -> str:
    """
    Converts native script back to Roman.
    """

    if language not in SCRIPT_CODES:
        return text

    return transliterate(
        text,
        SCRIPT_CODES[language],
        sanscript.ITRANS,
    )