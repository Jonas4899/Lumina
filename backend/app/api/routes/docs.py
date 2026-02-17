import re
from pathlib import Path
import shutil
from fastapi import APIRouter, File, HTTPException, UploadFile
from app.models.docs import UploadResponse, FileListResponse

router = APIRouter()

DOCS_DIR = Path(__file__).parent.parent.parent.parent / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)


def _sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    name = re.sub(r"[^\w.\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name


@router.post("/upload", response_model=UploadResponse, summary="Upload documents (PDFs) into the working directory of knowledge.")
def upload_document(file: UploadFile = File(...)):
    """
    Upload a PDF document to the docs folder.
    """
    #* Validate file to be a Valid PDF
    content = file.read(5)

    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=422,
            detail="File content is not a valid PDF! (Invalid magic bytes)"
        )
    
    file.seek(0)

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=422,
            detail=f"Only PDF files are accepted. Received: {file.content_type}",
        )

    #* Sanitize name of the file
    safe_name = _sanitize_filename(file.filename or "upload.pdf")
    if not safe_name.lower().endswith(".pdf"):
        safe_name += ".pdf"

    dest = DOCS_DIR / safe_name

    #* Write file in folder
    try:
        with open(dest, "xb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except FileExistsError:
        raise HTTPException(
            status_code=409,
            detail=f"A document named '{safe_name}' already exists.",
        )
    
    #* Get the file size
    file_size = dest.stat().st_size

    return UploadResponse(
        filename=safe_name,
        size_bytes=file_size,
    )


@router.get("/list", response_model=FileListResponse)
async def get_document_list():
    dir_files = [
        f.name for f in DOCS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]

    return FileListResponse(
        file_list=dir_files
    )