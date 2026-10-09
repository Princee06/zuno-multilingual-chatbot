from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from IndicTransToolkit import IndicProcessor
import torch

# Model Names

INDIC_TO_EN_MODEL = "ai4bharat/indictrans2-indic-en-dist-200M"
EN_TO_INDIC_MODEL = "ai4bharat/indictrans2-en-indic-dist-200M"

DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"

print(f"Using device: {DEVICE}")

# Load Indic → English

print("Loading Indic → English model...")

indic_en_tokenizer = AutoTokenizer.from_pretrained(
    INDIC_TO_EN_MODEL,
    trust_remote_code=True
)

indic_en_model = AutoModelForSeq2SeqLM.from_pretrained(
    INDIC_TO_EN_MODEL,
    trust_remote_code=True
).to(DEVICE)

print("Indic → English loaded.")

# Load English → Indic

print("Loading English → Indic model...")

en_indic_tokenizer = AutoTokenizer.from_pretrained(
    EN_TO_INDIC_MODEL,
    trust_remote_code=True
)

en_indic_model = AutoModelForSeq2SeqLM.from_pretrained(
    EN_TO_INDIC_MODEL,
    trust_remote_code=True
).to(DEVICE)

print("English → Indic loaded.")

# ==========================================================
# Processor
# ==========================================================

processor = IndicProcessor(inference=True)

# ==========================================================
# Language Codes
# ==========================================================

LANGUAGE_CODES = {

    "hi": "hin_Deva",
    "te": "tel_Telu",
    "ta": "tam_Taml",
    "kn": "kan_Knda",
    "ml": "mal_Mlym",
    "mr": "mar_Deva",
    "bn": "ben_Beng",
    "gu": "guj_Gujr",
    "pa": "pan_Guru",

}

# ==========================================================
# Indic → English
# ==========================================================

def to_english(text: str, source_language: str):

    src_lang = LANGUAGE_CODES[source_language]

    batch = processor.preprocess_batch(
        [text],
        src_lang=src_lang,
        tgt_lang="eng_Latn"
    )

    inputs = indic_en_tokenizer(
        batch,
        return_tensors="pt",
        padding=True
    ).to(DEVICE)

    with torch.no_grad():

        generated = indic_en_model.generate(
            **inputs,
            max_length=256
        )

    decoded = indic_en_tokenizer.batch_decode(
        generated,
        skip_special_tokens=True
    )

    result = processor.postprocess_batch(
        decoded,
        lang="eng_Latn"
    )

    return result[0]

# ==========================================================
# English → Indic
# ==========================================================

def from_english(text: str, target_language: str):

    tgt_lang = LANGUAGE_CODES[target_language]

    batch = processor.preprocess_batch(
        [text],
        src_lang="eng_Latn",
        tgt_lang=tgt_lang
    )

    inputs = en_indic_tokenizer(
        batch,
        return_tensors="pt",
        padding=True
    ).to(DEVICE)

    with torch.no_grad():

        generated = en_indic_model.generate(
            **inputs,
            max_length=256
        )

    decoded = en_indic_tokenizer.batch_decode(
        generated,
        skip_special_tokens=True
    )

    result = processor.postprocess_batch(
        decoded,
        lang=tgt_lang
    )

    return result[0]
# ==========================================================
# Compatibility wrappers
# ==========================================================

def translate_to_english(
    text: str,
    source_language: str,
):
    if source_language == "en":
        return text

    return to_english(
        text=text,
        source_language=source_language,
    )


def translate_from_english(
    text: str,
    target_language: str,
):
    if target_language == "en":
        return text

    return from_english(
        text=text,
        target_language=target_language,
    )