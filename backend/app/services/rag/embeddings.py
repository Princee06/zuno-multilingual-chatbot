from sentence_transformers import SentenceTransformer
import torch

from backend.app.config.settings import EMBEDDING_MODEL


DEVICE = "mps" if torch.backends.mps.is_available() else "cpu"


print("Loading embedding model...")


model = SentenceTransformer(
    EMBEDDING_MODEL,
    device=DEVICE,
)


print("Embedding model loaded.")



def embed_text(
    text: str
):

    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()



def embed_documents(
    documents: list[str]
):

    embeddings = model.encode(
        documents,
        normalize_embeddings=True,
    )

    return embeddings.tolist()