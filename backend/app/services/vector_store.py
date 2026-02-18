from functools import lru_cache
from pathlib import Path

import chromadb

BACKEND_ROOT = Path(__file__).parent.parent.parent


def _resolve_persist_dir(persist_dir: str) -> str:
    p = Path(persist_dir)
    if not p.is_absolute():
        p = BACKEND_ROOT / p
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


@lru_cache
def _get_chroma_client(persist_dir: str) -> chromadb.PersistentClient:
    resolved = _resolve_persist_dir(persist_dir)
    return chromadb.PersistentClient(path=resolved)


def get_or_create_collection(
    collection_name: str,
    persist_dir: str,
) -> chromadb.Collection:
    client = _get_chroma_client(persist_dir)
    return client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"},
    )


def store_chunks(
    collection: chromadb.Collection,
    doc_id: str,
    chunks: list,
    vectors: list[list[float]],
) -> int:
    ids = [f"{doc_id}_{i}" for i in range(len(chunks))]
    documents = [chunk.page_content for chunk in chunks]
    metadatas = [
        {k: v for k, v in {**chunk.metadata, "source_id": doc_id}.items() if v is not None}
        for chunk in chunks
    ]

    collection.upsert(
        ids=ids,
        embeddings=vectors,
        documents=documents,
        metadatas=metadatas,
    )

    return len(chunks)
