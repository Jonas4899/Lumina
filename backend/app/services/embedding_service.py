from openai import AsyncOpenAI
from app.config import Settings


def build_enrichment_string(page_content: str, metadata: dict) -> str:
    parts = []
    for key in ("Header 1", "Header 2", "Header 3"):
        if key in metadata and metadata[key]:
            parts.append(metadata[key])

    topic = " > ".join(parts) if parts else "General"
    return f"Tema: {topic}. Texto: {page_content}"


async def embed_chunks(
    chunks: list,
    settings: Settings,
    batch_size: int = 100,
) -> list[list[float]]:
    client = AsyncOpenAI(
        api_key=settings.openai_api_key,
    )

    enriched_texts = [
        build_enrichment_string(chunk.page_content, chunk.metadata)
        for chunk in chunks
    ]

    all_vectors: list[list[float]] = []

    for i in range(0, len(enriched_texts), batch_size):
        batch = enriched_texts[i : i + batch_size]
        response = await client.embeddings.create(
            model=settings.embedding_model,
            input=batch,
        )
        batch_vectors = [
            item.embedding
            for item in sorted(response.data, key=lambda x: x.index)
        ]
        all_vectors.extend(batch_vectors)

    return all_vectors
