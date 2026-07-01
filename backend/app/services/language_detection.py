from langdetect import detect, DetectorFactory

# Ensures consistent language detection results
DetectorFactory.seed = 0


def detect_language(text: str) -> str:
    """
    Detects the language of the input text.

    Returns:
        en - English
        hi - Hindi
        te - Telugu
        kn - Kannada
        ta - Tamil
        ml - Malayalam
        mr - Marathi
        bn - Bengali
        gu - Gujarati
        pa - Punjabi
        ...
    """

    try:
        return detect(text)

    except Exception:
        return "unknown"