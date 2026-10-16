import re

# -----------------------------
# Native Script Unicode Ranges
# -----------------------------

SCRIPT_RANGES = {
    "hi": r"[\u0900-\u097F]",  # Hindi (Devanagari)
    "te": r"[\u0C00-\u0C7F]",  # Telugu
    "ta": r"[\u0B80-\u0BFF]",  # Tamil
    "kn": r"[\u0C80-\u0CFF]",  # Kannada
    "ml": r"[\u0D00-\u0D7F]",  # Malayalam
    "gu": r"[\u0A80-\u0AFF]",  # Gujarati
    "bn": r"[\u0980-\u09FF]",  # Bengali
    "pa": r"[\u0A00-\u0A7F]",  # Punjabi (Gurmukhi)
}


# ---------------------------------------------------
# Roman Vocabulary
# (We'll keep expanding this over time.)
# ---------------------------------------------------

ROMAN_WORDS = {

    "te": {
        "nenu", "meeru", "ela", "unnaru", "unnava",
        "bagunnanu", "bagunnara", "andi", "avunu",
        "kaadu", "em", "enti", "naaku", "mee",
        "ekkada", "vellanu", "vastundi", "cheppu",
        "cheppandi", "sare", "ledu", "inka",
        "ippudu", "emi", "enduku", "evaru", "namaskaram", "naa", "peru", "daggara", "maamuluga",
"maatladutunna", "maatladutunnanu", "maatladutunnaru"
    },

    "hi": {
        "namaste", "aap", "kaise", "ho",
        "hai", "haan", "nahi", "mera",
        "meri", "kya", "kyun", "kaun",
        "main", "tum", "hum", "acha",
        "accha", "theek", "dhanyavaad"
    },

    "ta": {
        "vanakkam", "naan", "iruken",
        "irukkiren", "unga", "epadi",
        "saptingala", "nandri", "seri",
        "illai", "enga", "enna"
    },

    "kn": {
        "namaskara", "hegiddira",
        "hegide", "nanu", "neevu",
        "chenagiddini", "illa", "haudu",
        "yenu", "elli", "dhanyavada"
    },

    "ml": {
        "namaskaram", "sughamano",
        "njan", "ningal", "entha",
        "evide", "alle", "sheri"
    },

    "bn": {
        "ami", "bhalo", "achi",
        "tumi", "kemon", "dhonnobad"
    },

    "gu": {
        "kem", "cho", "majama",
        "hu", "tame", "shu"
    },

    "mr": {
        "namaskar", "tumhi",
        "kasa", "aahat",
        "mi", "bara"
    }

}


def detect_language(text: str, hint: str = ""):
    text = text.strip()

    if not text:
        return {"language": "unknown", "style": "unknown"}

    for language, pattern in SCRIPT_RANGES.items():
        if re.search(pattern, text):
            return {"language": language, "style": "native"}

    cleaned = re.sub(r"[^a-zA-Z ]", "", text).lower()
    words = cleaned.split()

    english_words = {
        "hello", "hi", "how", "are", "you",
        "what", "where", "when", "why",
        "good", "morning", "night",
        "thank", "thanks", "please",
        "yes", "no", "can", "could",
        "would", "is", "am", "the",
        "my", "your", "name",
    }

    english_score = sum(word in english_words for word in words)

    scores = {
        lang: sum(word in vocab for word in words)
        for lang, vocab in ROMAN_WORDS.items()
    }

    best_score = max(scores.values())
    best = [lang for lang, s in scores.items() if s == best_score]
    best_language = hint if hint in best else best[0]

    if best_score > english_score and best_score > 0:
        return {"language": best_language, "style": "roman"}

    if english_score > 0:
        return {"language": "en", "style": "english"}

    return {"language": "unknown", "style": "unknown"}