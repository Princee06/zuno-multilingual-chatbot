import uuid

import chromadb

client = chromadb.PersistentClient(path="database")


def get_collection(session_id: str):
    return client.get_or_create_collection(
        name=f"documents_{session_id}"
    )


def add_document(
    texts,
    embeddings,
    source,
    session_id,
):
    collection = get_collection(session_id)

    ids = [
        str(uuid.uuid4())
        for _ in texts
    ]

    metadatas = [
        {
            "source": source,
        }
        for _ in texts
    ]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def search(
    query_embedding,
    session_id,
    top_k=50,
):
    collection = get_collection(session_id)

    return collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        include=[
            "documents",
            "metadatas",
            "distances",
        ],
    )


def clear(session_id):
    name = f"documents_{session_id}"

    try:
        client.delete_collection(name)
    except Exception:
        pass