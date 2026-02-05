import pymupdf4llm
from functools import lru_cache

@lru_cache(maxsize=1)
def get_documentation() -> str:
    """
    Lee la documentación y la cachea en memoria.
    Se ejecuta solo una vez gracias a @lru_cache.
    """
    print("📖 Leyendo PDF de documentación...")
    md_doc = pymupdf4llm.to_markdown("docs/polars/dataframe_documentation.pdf")
    print(f"✅ PDF leído: {len(md_doc)} caracteres")
    return md_doc