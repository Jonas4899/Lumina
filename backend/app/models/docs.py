from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    size_bytes: int
    doc_id: str
    chunk_count: int
    vectorized: bool


class FileListResponse(BaseModel):
    file_list: list