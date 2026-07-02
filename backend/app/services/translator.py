import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSeq2SeqLM,
)

from IndicTransToolkit import IndicProcessor


DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

MODEL_NAME = "ai4bharat/indictrans2-en-indic-dist-200M"

print("Loading IndicTrans2 model...")

tokenizer = AutoTokenizer.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_NAME,
    trust_remote_code=True,
)

model = model.to(DEVICE)

processor = IndicProcessor(inference=True)

print("IndicTrans2 loaded successfully.")