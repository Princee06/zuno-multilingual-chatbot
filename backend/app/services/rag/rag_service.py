from backend.app.services.rag.retriever import retrieve


def get_context(
    query: str,
    session_id: str,
):
    documents = retrieve(
        query=query,
        session_id=session_id,
        top_k=5,
        candidate_k=20,
    )

    if not documents:
        return ""

    return "\n\n".join(documents)