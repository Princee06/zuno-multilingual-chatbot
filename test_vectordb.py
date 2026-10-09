from backend.app.services.rag.loader import load_document
from backend.app.services.rag.chunker import chunk_text
from backend.app.services.rag.embeddings import embed_documents
from backend.app.services.rag.vectordb import add_document, count

text = load_document("Akka ticket.pdf")  # Use the same working path

chunks = chunk_text(text)

vectors = embed_documents(chunks)

add_document(chunks, vectors)

print("Stored:", count())