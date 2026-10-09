from backend.app.services.rag.retriever import retrieve

results = retrieve(
    "What is the departure time?"
)

print()

for i, chunk in enumerate(results, start=1):
    print("=" * 60)
    print(f"Result {i}")
    print("=" * 60)
    print(chunk)
    print()
