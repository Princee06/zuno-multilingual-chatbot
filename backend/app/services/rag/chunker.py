from langchain_text_splitters import RecursiveCharacterTextSplitter

from backend.app.services.rag.constants import (
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=CHUNK_SIZE,
    chunk_overlap=CHUNK_OVERLAP,
    separators=[
        "\n\n",
        "\n",
        ". ",
        "? ",
        "! ",
        " ",
        "",
    ],
)


def chunk_text(text: str):
    """
    Splits text into semantically meaningful overlapping chunks.
    """

    if not text.strip():
        return []

    return splitter.split_text(text)