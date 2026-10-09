from backend.app.services.rag.embeddings import embed_text
from backend.app.services.rag.vectordb import search, count

print("Total documents in DB:", count())
print()

query = "What is my flight number?"
query_embedding = embed_text(query)

results = search(query_embedding, top_k=20)

documents = results.get("documents", [])
distances = results.get("distances", [])

if documents and isinstance(documents[0], list):
    documents = documents[0]
if distances and isinstance(distances[0], list):
    distances = distances[0]

print(f"=== TOP {len(documents)} RAW VECTOR RESULTS ===\n")

for i, doc in enumerate(documents):
    dist = distances[i] if i < len(distances) else "?"
    has_flight_number = "6E 5309" in doc or "PNR" in doc
    marker = "  <-- CONTAINS TARGET DATA" if has_flight_number else ""
    print(f"--- rank {i} | distance {dist}{marker} ---")
    print(doc[:300])
    print()