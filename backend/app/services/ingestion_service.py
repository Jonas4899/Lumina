import re
import uuid
from pathlib import Path

import pymupdf4llm
from langchain_text_splitters import MarkdownHeaderTextSplitter

from app.config import Settings
from app.services.embedding_service import embed_chunks
from app.services.vector_store import get_or_create_collection, store_chunks

DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
DOCS_DIR.mkdir(parents=True, exist_ok=True)


def _sanitize_filename(filename: str) -> str:
    name = Path(filename).name
    name = re.sub(r"[^\w.\-]", "_", name)
    name = re.sub(r"_+", "_", name)
    return name


async def ingest_doc(
    file_content: bytes,
    original_filename: str,
    content_type: str,
    settings: Settings,
) -> dict:
    # 1. Validar que sea un PDF válido
    if not file_content[:5].startswith(b"%PDF-"):
        raise ValueError("File content is not a valid PDF! (Invalid magic bytes)")

    if content_type != "application/pdf":
        raise ValueError(f"Only PDF files are accepted. Received: {content_type}")

    # 2. Sanitizar nombre
    safe_name = _sanitize_filename(original_filename)
    if not safe_name.lower().endswith(".pdf"):
        safe_name += ".pdf"

    # 3. Generar UUID único
    doc_id = str(uuid.uuid4())

    # 4. Guardar archivo en disco (backup)
    dest = DOCS_DIR / safe_name
    try:
        with open(dest, "xb") as f:
            f.write(file_content)
    except FileExistsError:
        raise FileExistsError(f"A document named '{safe_name}' already exists.")

    # 5. Obtener tamaño
    file_size = dest.stat().st_size

    try:
        # 6. Convertir PDF a markdown
        md_text = pymupdf4llm.to_markdown(str(dest))

        # 7. Splitear con MarkdownHeaderTextSplitter
        headers_to_split_on = [
            ("#", "Header 1"),
            ("##", "Header 2"),
            ("###", "Header 3"),
        ]
        splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
        chunks = splitter.split_text(md_text)

        if len(chunks) == 0:
            raise ValueError("No text content could be extracted from this PDF.")

        # 8. Generar embeddings
        vectors = await embed_chunks(chunks, settings)

        # 9. Almacenar en ChromaDB
        collection = get_or_create_collection(
            settings.chroma_collection_name,
            settings.chroma_persist_dir,
        )
        chunk_count = store_chunks(collection, doc_id, chunks, vectors)

    except Exception as e:
        # Rollback: eliminar archivo para mantener consistencia disco/vectores
        if dest.exists():
            dest.unlink()
        if isinstance(e, ValueError):
            raise
        raise RuntimeError(
            f"Ingestion failed for '{safe_name}' (doc_id={doc_id}): {e}"
        ) from e

    return {
        "doc_id": doc_id,
        "filename": safe_name,
        "size_bytes": file_size,
        "chunk_count": chunk_count,
        "vectorized": True,
    }
