from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

MODEL = "ai4bharat/indictrans2-indic-en-dist-200M"

tokenizer = AutoTokenizer.from_pretrained(
    MODEL,
    trust_remote_code=True
)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL,
    trust_remote_code=True
)

print("Indic → English Loaded Successfully!")