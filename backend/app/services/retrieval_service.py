from fastapi import HTTPException

from app.config import Settings
from app.services.embedding_service import embed_query
from app.services.vector_store import get_or_create_collection


async def retrieve_relevant_chunks(
    user_query: str,
    settings: Settings,
) -> list[dict]:
    query_vector = await embed_query(user_query, settings)

    collection = get_or_create_collection(
        settings.chroma_collection_name,
        settings.chroma_persist_dir,
    )

    if collection.count() == 0:
        raise HTTPException(
            status_code=404,
            detail="No documentation has been uploaded yet. Please upload PDF documents first.",
        )

    results = collection.query(
        query_embeddings=[query_vector],
        n_results=settings.retrieval_top_k,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"document": doc, "metadata": meta, "distance": dist})

    return chunks


def format_chunks_as_context(chunks: list[dict]) -> str:
    sections = []

    for chunk in chunks:
        meta = chunk["metadata"]
        parts = []
        for key in ("Header 1", "Header 2", "Header 3"):
            if key in meta and meta[key]:
                parts.append(meta[key])

        header = " > ".join(parts) if parts else "General"
        sections.append(f"[Fuente: {header}]\n{chunk['document']}")

    return "\n\n---\n\n".join(sections)
