import re

from sentence_transformers import CrossEncoder

from backend.app.services.rag.embeddings import embed_text
from backend.app.services.rag.vectordb import search


print("Loading reranker model...")
reranker = CrossEncoder(
    "cross-encoder/ms-marco-MiniLM-L-6-v2"
)
print("Reranker loaded.")


def calculate_boost(
    query: str,
    document: str,
    metadata: dict | None,
) -> float:
    """
    Generic scoring that works for resumes, invoices,
    tickets, reports, IDs, certificates, etc.
    """

    boost = 0.0

    query_lower = query.lower()
    doc_lower = document.lower()

    personal_intent = any(
        phrase in query_lower
        for phrase in [
            "my",
            "mine",
            "what is",
            "what are",
            "tell me",
            "give me",
            "show me",
        ]
    )

    if personal_intent:

        value_patterns = [

            r"\b[A-Z0-9]{5,15}\b",

            r"\b\d{3,12}\b",

            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b",

            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",

            r"\+?\d[\d\s-]{7,}",

        ]

        for pattern in value_patterns:
            if re.search(pattern, document):
                boost += 3
                break

        structure_patterns = [
            ":",
            "|",
            "-",
            "name",
            "date",
            "number",
            "id",
            "details",
            "information",
            "summary",
            "skills",
            "education",
            "experience",
            "projects",
            "certifications",
        ]

        for pattern in structure_patterns:
            if pattern in doc_lower:
                boost += 1

    instruction_patterns = [
        "for example",
        "example:",
        "sample",
        "how to",
        "instructions",
        "step 1",
        "step 2",
    ]

    for pattern in instruction_patterns:
        if pattern in doc_lower:
            boost -= 3

    if metadata:

        if metadata.get("source"):
            boost += 0.2

        if metadata.get("page") is not None:
            boost += 0.1

    return boost


def retrieve(
    query: str,
    session_id: str,
    top_k: int = 3,
    candidate_k: int = 50,
):
    """
    Vector Search
        ↓
    Cross Encoder
        ↓
    Generic Boosting
        ↓
    Final Ranking
    """

    query_embedding = embed_text(query)

    results = search(
        query_embedding=query_embedding,
        session_id=session_id,
        top_k=candidate_k,
    )

    documents = results.get("documents", [])
    metadatas = results.get("metadatas", [])

    if not documents:
        return []

    if isinstance(documents[0], list):
        documents = documents[0]

    if metadatas and isinstance(metadatas[0], list):
        metadatas = metadatas[0]

    if not metadatas:
        metadatas = [None] * len(documents)

    cleaned = []

    seen = set()

    for doc, meta in zip(documents, metadatas):

        if not isinstance(doc, str):
            continue

        if doc in seen:
            continue

        seen.add(doc)

        cleaned.append(
            (
                doc,
                meta,
            )
        )

    if not cleaned:
        return []

    pairs = [
        (
            query,
            doc,
        )
        for doc, _ in cleaned
    ]

    scores = reranker.predict(pairs)

    ranked = []

    for (doc, meta), score in zip(cleaned, scores):

        final_score = (
            float(score)
            + calculate_boost(
                query,
                doc,
                meta,
            )
        )

        ranked.append(
            (
                doc,
                final_score,
            )
        )

    ranked.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    return [
    doc
    for doc, _ in ranked[: min(top_k, len(ranked))]
]