from backend.app.services.rag.retriever import retrieve


query = "What is my flight number?"


results = retrieve(
    query,
    top_k=10
)


print("=" * 80)

for i, item in enumerate(results):

    print(f"RESULT {i+1}")
    print("=" * 80)

    print(item)

    print("\n")