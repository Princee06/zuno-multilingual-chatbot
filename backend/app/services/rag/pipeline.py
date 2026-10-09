from backend.app.services.rag.loader import load_document
from backend.app.services.rag.chunker import chunk_text
from backend.app.services.rag.embeddings import embed_documents
from backend.app.services.rag.vectordb import add_document


def ingest_document(
    file_path: str,
    session_id: str,
):
    text = load_document(file_path)

    if not text.strip():
        return

    chunks = chunk_text(text)

    if not chunks:
        return

    embeddings = embed_documents(chunks)

    add_document(
        texts=chunks,
        embeddings=embeddings,
        source=file_path,
        session_id=session_id,
    )