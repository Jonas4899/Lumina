from pydantic import BaseModel


class UploadResponse(BaseModel):
    filename: str
    path: str
    size_bytes: int


class FileListResponse(BaseModel):
    file_list: list