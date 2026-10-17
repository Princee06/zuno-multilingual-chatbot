import re

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
# Splitting long text into pieces the models can handle
# ==========================================================

MAX_CHARS = 300
BATCH_SIZE = 8
SENTENCE_SPLIT = re.compile(r"(?<=[.!?।॥])\s+")
BULLET = re.compile(r"^(\s*(?:[-*•]|\d+[.)])\s+)")


def _chunks(text: str):
    """Group sentences into pieces of at most MAX_CHARS characters."""
    chunks, current = [], ""

    for sentence in SENTENCE_SPLIT.split(text):

        # A single very long sentence is cut at a space
        while len(sentence) > MAX_CHARS:
            cut = sentence.rfind(" ", 0, MAX_CHARS)
            cut = cut if cut > 0 else MAX_CHARS

            if current:
                chunks.append(current)
                current = ""

            chunks.append(sentence[:cut].strip())
            sentence = sentence[cut:].strip()

        if current and len(current) + len(sentence) + 1 > MAX_CHARS:
            chunks.append(current)
            current = sentence
        else:
            current = (current + " " + sentence).strip()

    if current:
        chunks.append(current)

    return [c for c in chunks if c]


def _translate(text, src_lang, tgt_lang, tokenizer, model):
    if not text.strip():
        return text

    lines = text.split("\n")
    prefixes, jobs = [], []

    # Line breaks and bullet markers are kept as they are
    for i, line in enumerate(lines):
        match = BULLET.match(line)
        prefix = match.group(1) if match else ""
        prefixes.append(prefix)

        for chunk in _chunks(line[len(prefix):].strip()):
            jobs.append((i, chunk))

    if not jobs:
        return text

    outputs = []

    for start in range(0, len(jobs), BATCH_SIZE):
        group = [chunk for _, chunk in jobs[start:start + BATCH_SIZE]]

        batch = processor.preprocess_batch(
            group,
            src_lang=src_lang,
            tgt_lang=tgt_lang,
        )

        inputs = tokenizer(
            batch,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256,
        ).to(DEVICE)

        with torch.no_grad():
            generated = model.generate(
                **inputs,
                max_length=256,
            )

        decoded = tokenizer.batch_decode(
            generated,
            skip_special_tokens=True,
        )

        outputs.extend(
            processor.postprocess_batch(decoded, lang=tgt_lang)
        )

    done = {}

    for (i, _), out in zip(jobs, outputs):
        done.setdefault(i, []).append(out)

    return "\n".join(
        prefixes[i] + " ".join(done[i]) if i in done else line
        for i, line in enumerate(lines)
    )

# ==========================================================
# Indic → English
# ==========================================================

def to_english(text: str, source_language: str):
    return _translate(
        text,
        LANGUAGE_CODES[source_language],
        "eng_Latn",
        indic_en_tokenizer,
        indic_en_model,
    )

# ==========================================================
# English → Indic
# ==========================================================

def from_english(text: str, target_language: str):
    return _translate(
        text,
        "eng_Latn",
        LANGUAGE_CODES[target_language],
        en_indic_tokenizer,
        en_indic_model,
    )

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