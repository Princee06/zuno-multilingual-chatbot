from backend.app.services.rag.loader import load_document
from backend.app.services.rag.chunker import chunk_text

text = load_document("Akka ticket.pdf")

chunks = chunk_text(text)

print(f"Chunks: {len(chunks)}")

print("\nFirst Chunk:\n")
print(chunks[0])

print("\nSecond Chunk:\n")
print(chunks[1])