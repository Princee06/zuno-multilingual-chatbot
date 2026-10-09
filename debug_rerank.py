from sentence_transformers import CrossEncoder

from backend.app.services.rag.embeddings import embed_text
from backend.app.services.rag.vectordb import search

print("Loading reranker...")
reranker = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2")
print("Loaded.\n")

query = "What is my flight number?"
query_embedding = embed_text(query)

results = search(query_embedding, top_k=15)
documents = results.get("documents", [])
if documents and isinstance(documents[0], list):
    documents = documents[0]

# dedup, same as retriever.py
seen = set()
deduped = []
for doc in documents:
    if doc not in seen:
        seen.add(doc)
        deduped.append(doc)
documents = deduped

pairs = [(query, doc) for doc in documents]
scores = reranker.predict(pairs)

ranked = sorted(zip(documents, scores), key=lambda p: p[1], reverse=True)

print(f"=== {len(ranked)} CANDIDATES, RERANKED ===\n")
for i, (doc, score) in enumerate(ranked):
    has_target = "PNR" in doc or "6E 5309" in doc
    marker = "  <-- TARGET CHUNK" if has_target else ""
    print(f"rank {i} | score {score:.4f}{marker}")
    print(repr(doc[:150]))
    print()
