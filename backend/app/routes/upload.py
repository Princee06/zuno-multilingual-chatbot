from pathlib import Path
import shutil

from fastapi import APIRouter, UploadFile, File, HTTPException

from backend.app.services.rag.pipeline import ingest_document

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("")
async def upload_document(
    file: UploadFile = File(...)
):

    suffix = Path(file.filename).suffix.lower()

    if suffix not in [".pdf", ".docx", ".txt"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file type."
        )

    file_path = UPLOAD_DIR / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    ingest_document(str(file_path))

    return {
        "message": "Document uploaded and indexed successfully."
    }