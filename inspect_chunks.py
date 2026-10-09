from backend.app.services.rag.loader import load_document
from backend.app.services.rag.chunker import chunk_text

text = load_document("Akka ticket.pdf")   # same path you used before

chunks = chunk_text(text)

for i, chunk in enumerate(chunks):
    print("=" * 80)
    print(f"Chunk {i}")
    print("=" * 80)
    print(chunk)
    print()