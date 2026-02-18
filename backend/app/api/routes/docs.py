from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.config import Settings, get_settings
from app.models.docs import FileListResponse, UploadResponse
from app.services.ingestion_service import DOCS_DIR, ingest_doc

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
    summary="Upload documents (PDFs) into the working directory of knowledge.",
)
async def upload_document(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
):
    content = await file.read()

    try:
        result = await ingest_doc(
            file_content=content,
            original_filename=file.filename or "upload.pdf",
            content_type=file.content_type or "",
            settings=settings,
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except FileExistsError as e:
        raise HTTPException(status_code=409, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))

    return UploadResponse(
        filename=result["filename"],
        size_bytes=result["size_bytes"],
        doc_id=result["doc_id"],
        chunk_count=result["chunk_count"],
        vectorized=result["vectorized"],
    )


@router.get("/list", response_model=FileListResponse)
async def get_document_list():
    dir_files = [
        f.name
        for f in DOCS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() == ".pdf"
    ]

    return FileListResponse(file_list=dir_files)
