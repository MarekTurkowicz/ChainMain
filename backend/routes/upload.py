from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile, status

from models.schemas import UploadResponse
from rag.loader import UnsupportedFileType
from services import document_service


router = APIRouter(tags=["upload"])


@router.post("/upload", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)) -> UploadResponse:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing filename",
        )
    content = await file.read()
    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty file",
        )
    try:
        info = document_service.save_and_index(
            filename=file.filename,
            content=content,
            mime_type=file.content_type or "application/octet-stream",
        )
    except UnsupportedFileType as e:
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to index document: {e}",
        )
    return UploadResponse(
        doc_id=info.doc_id,
        filename=info.filename,
        chunk_count=info.chunk_count,
    )
