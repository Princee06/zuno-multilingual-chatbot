from pathlib import Path

import pdfplumber
from docx import Document


SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
}


def load_document(file_path: str) -> str:
    """
    Loads a document and returns extracted text.
    Supports:
    - PDF
    - DOCX
    - TXT
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"{file_path} does not exist."
        )

    extension = path.suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported file type: {extension}"
        )


    if extension == ".pdf":
        return _load_pdf(path)


    if extension == ".docx":
        return _load_docx(path)


    if extension == ".txt":
        return _load_txt(path)


    raise ValueError(
        "Unsupported file type."
    )


def _load_pdf(path: Path) -> str:

    pages = []

    with pdfplumber.open(path) as pdf:

        for page in pdf.pages:

            text = page.extract_text(
                x_tolerance=2,
                y_tolerance=2
            )

            if text:
                pages.append(text)


    return "\n".join(pages)



def _load_docx(path: Path) -> str:

    document = Document(path)

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(
                paragraph.text
            )


    return "\n".join(paragraphs)



def _load_txt(path: Path) -> str:

    with open(
        path,
        "r",
        encoding="utf-8"
    ) as file:

        return file.read()