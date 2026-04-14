from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from models.schemas import DocumentsResponse
from services import document_service


router = APIRouter(tags=["documents"])


@router.get("/documents", response_model=DocumentsResponse)
def list_documents() -> DocumentsResponse:
    return DocumentsResponse(documents=document_service.list_documents())


@router.delete("/documents/{doc_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(doc_id: str) -> None:
    if not document_service.delete_document(doc_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )
