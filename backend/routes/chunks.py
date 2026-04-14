from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query, status

from models.schemas import ChunkPreview, ChunkPreviewResponse
from rag.vectorstore import get_chunk_by_id, get_chunks_in_range


router = APIRouter(tags=["chunks"])


def _to_preview(chunk_id: str, text: str, meta: dict, *, is_target: bool) -> ChunkPreview:
    page = meta.get("page")
    return ChunkPreview(
        chunk_id=chunk_id,
        chunk_index=int(meta.get("chunk_index", 0)),
        doc_id=str(meta.get("doc_id", "")),
        filename=str(meta.get("filename", "unknown")),
        page=(int(page) + 1) if isinstance(page, int) else None,
        text=text,
        is_target=is_target,
    )


@router.get("/chunks/{chunk_id}", response_model=ChunkPreviewResponse)
def get_chunk(
    chunk_id: str,
    window: int = Query(2, ge=0, le=10, description="Number of neighbors on each side"),
) -> ChunkPreviewResponse:
    found = get_chunk_by_id(chunk_id)
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Chunk not found")

    text, meta = found
    target_index = int(meta.get("chunk_index", 0))
    doc_id = str(meta.get("doc_id", ""))
    target = _to_preview(chunk_id, text, meta, is_target=True)

    neighbors: list[ChunkPreview] = []
    if window > 0 and doc_id:
        rng = get_chunks_in_range(doc_id, target_index - window, target_index + window)
        for n_text, n_meta in rng:
            n_id = str(n_meta.get("chunk_id", ""))
            if n_id == chunk_id:
                continue
            neighbors.append(_to_preview(n_id, n_text, n_meta, is_target=False))

    return ChunkPreviewResponse(target=target, neighbors=neighbors)
