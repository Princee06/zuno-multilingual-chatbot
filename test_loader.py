from backend.app.services.rag.loader import load_document

text = load_document("Akka ticket.pdf")

print(text[:1000])