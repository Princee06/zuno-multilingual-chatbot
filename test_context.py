from backend.app.services.rag.retriever import retrieve


query = "What is my flight number?"


results = retrieve(
    query,
    top_k=3
)


print("\n========== FINAL CONTEXT SENT ==========\n")


for i, result in enumerate(results):

    print(f"--- CHUNK {i+1} ---")
    print(result)
    print("\n")