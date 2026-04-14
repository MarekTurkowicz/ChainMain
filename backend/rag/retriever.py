from __future__ import annotations

from langchain_core.documents import Document

from config import settings
from rag.vectorstore import similarity_search


def retrieve(
    question: str,
    doc_ids: list[str] | None = None,
    k: int | None = None,
) -> list[tuple[Document, float]]:
    """Return top-k (chunk, similarity) pairs, optionally scoped to doc_ids."""
    return similarity_search(question, k=k or settings.top_k, doc_ids=doc_ids)
