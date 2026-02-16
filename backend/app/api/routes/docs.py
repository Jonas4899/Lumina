import re
from pathlib import Path
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.docs import UploadResponse, FileListResponse

router = APIRouter()

DOCS_DIR = Path(__file__).parent.parent.parent.parent / "docs"


def _sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    name = re.sub(r"[^\w.\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name


@router.post("/upload", response_model=UploadResponse, summary="Upload documents (PDFs) into the working directory of knowledge.")
async def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document to the docs folder.
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=422,
            detail=f"Only PDF files are accepted. Received: {file.content_type}",
        )

    safe_name = _sanitize_filename(file.filename or "upload.pdf")
    if not safe_name.lower().endswith(".pdf"):
        safe_name += ".pdf"

    dest = DOCS_DIR / safe_name

    if dest.exists():
        raise HTTPException(
            status_code=409,
            detail=f"A document named '{safe_name}' already exists.",
        )

    content = await file.read()
    dest.write_bytes(content)

    return UploadResponse(
        filename=safe_name,
        path=safe_name,
        size_bytes=len(content),
    )


@router.get("/list", response_model=FileListResponse)
async def get_document_list():
    dir_files = [file.name for file in DOCS_DIR.iterdir()]

    return FileListResponse(
        file_list=dir_files
    )