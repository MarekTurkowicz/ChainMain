from __future__ import annotations

import uuid
from pathlib import Path

from rag.loader import load_file
from rag.splitter import split_documents
from rag.vectorstore import add_chunks


def ingest(path: Path, doc_id: str, filename: str) -> int:
    """Load → split → embed → store. Returns the number of chunks written."""
    raw_docs = load_file(path)
    chunks = split_documents(raw_docs)

    chunk_ids: list[str] = []
    for index, chunk in enumerate(chunks):
        chunk_id = str(uuid.uuid4())
        chunk_ids.append(chunk_id)
        chunk.metadata = {
            **chunk.metadata,
            "doc_id": doc_id,
            "filename": filename,
            "chunk_id": chunk_id,
            "chunk_index": index,
        }

    if chunks:
        add_chunks(chunks, ids=chunk_ids)
    return len(chunks)
