from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class DocumentInfo(BaseModel):
    doc_id: str
    filename: str
    mime_type: str
    chunk_count: int
    uploaded_at: datetime


class UploadResponse(BaseModel):
    doc_id: str
    filename: str
    chunk_count: int


class AskRequest(BaseModel):
    question: str = Field(..., min_length=1)
    doc_ids: list[str] | None = None


class SourceChunk(BaseModel):
    doc_id: str
    filename: str
    page: int | None = None
    chunk_id: str
    text: str
    score: float | None = None


class AskResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]


class ChunkPreview(BaseModel):
    chunk_id: str
    chunk_index: int
    doc_id: str
    filename: str
    page: int | None = None
    text: str
    is_target: bool = False


class ChunkPreviewResponse(BaseModel):
    target: ChunkPreview
    neighbors: list[ChunkPreview]


class DocumentsResponse(BaseModel):
    documents: list[DocumentInfo]


class ErrorResponse(BaseModel):
    detail: str
    context: dict[str, Any] | None = None
