from backend.app.services.rag.loader import load_document
from backend.app.services.rag.chunker import chunk_text
from backend.app.services.rag.embeddings import embed_documents

text = load_document("Akka ticket.pdf")  # use the same path that worked before

chunks = chunk_text(text)

vectors = embed_documents(chunks)

print(f"Chunks: {len(chunks)}")
print(f"Embeddings: {len(vectors)}")
print(f"Embedding Dimension: {len(vectors[0])}")