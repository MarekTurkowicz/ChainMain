from __future__ import annotations

from functools import lru_cache

from langchain_chroma import Chroma
from langchain_core.documents import Document

from config import settings
from rag.embeddings import get_embeddings


COLLECTION_NAME = "documents"


@lru_cache(maxsize=1)
def get_store() -> Chroma:
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=str(settings.chroma_path),
    )


def add_chunks(chunks: list[Document], ids: list[str]) -> None:
    get_store().add_documents(documents=chunks, ids=ids)


def delete_by_doc_id(doc_id: str) -> None:
    get_store().delete(where={"doc_id": doc_id})


def get_chunk_by_id(chunk_id: str) -> tuple[str, dict] | None:
    """Return (text, metadata) for a chunk identified by its chunk_id metadata."""
    res = get_store().get(where={"chunk_id": chunk_id}, limit=1)
    docs = res.get("documents") or []
    metas = res.get("metadatas") or []
    if not docs:
        return None
    return docs[0], metas[0] if metas else {}


def get_chunks_in_range(doc_id: str, start_index: int, end_index: int) -> list[tuple[str, dict]]:
    """Return chunks whose chunk_index is within [start_index, end_index] for a doc, ordered."""
    res = get_store().get(
        where={
            "$and": [
                {"doc_id": doc_id},
                {"chunk_index": {"$gte": start_index}},
                {"chunk_index": {"$lte": end_index}},
            ]
        }
    )
    docs = res.get("documents") or []
    metas = res.get("metadatas") or []
    paired = list(zip(docs, metas))
    paired.sort(key=lambda dm: dm[1].get("chunk_index", 0))
    return paired


def similarity_search(
    query: str,
    k: int,
    doc_ids: list[str] | None = None,
) -> list[tuple[Document, float]]:
    """Return (document, similarity_score) pairs.

    Chroma returns a distance; we convert to a similarity in [0, 1] for the UI.
    """
    where = None
    if doc_ids:
        where = {"doc_id": {"$in": doc_ids}} if len(doc_ids) > 1 else {"doc_id": doc_ids[0]}

    results = get_store().similarity_search_with_score(query, k=k, filter=where)
    return [(doc, max(0.0, 1.0 - float(dist))) for doc, dist in results]
