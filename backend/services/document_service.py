from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock

from config import settings
from models.schemas import DocumentInfo
from rag.loader import SUPPORTED_EXTENSIONS, UnsupportedFileType
from rag.pipeline import ingest
from rag.vectorstore import delete_by_doc_id


_lock = Lock()


def _load_index() -> list[dict]:
    if not settings.metadata_path.exists():
        return []
    try:
        return json.loads(settings.metadata_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return []


def _save_index(entries: list[dict]) -> None:
    settings.metadata_path.parent.mkdir(parents=True, exist_ok=True)
    settings.metadata_path.write_text(
        json.dumps(entries, indent=2, default=str),
        encoding="utf-8",
    )


def list_documents() -> list[DocumentInfo]:
    return [DocumentInfo(**entry) for entry in _load_index()]


def save_and_index(filename: str, content: bytes, mime_type: str) -> DocumentInfo:
    ext = Path(filename).suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise UnsupportedFileType(
            f"Unsupported file type '{ext}'. Allowed: {sorted(SUPPORTED_EXTENSIONS)}"
        )

    doc_id = str(uuid.uuid4())
    safe_name = Path(filename).name
    stored_path = settings.upload_path / f"{doc_id}_{safe_name}"
    stored_path.write_bytes(content)

    chunk_count = ingest(stored_path, doc_id=doc_id, filename=safe_name)

    info = DocumentInfo(
        doc_id=doc_id,
        filename=safe_name,
        mime_type=mime_type or "application/octet-stream",
        chunk_count=chunk_count,
        uploaded_at=datetime.now(timezone.utc),
    )

    with _lock:
        entries = _load_index()
        entries.append(info.model_dump(mode="json"))
        _save_index(entries)

    return info


def delete_document(doc_id: str) -> bool:
    with _lock:
        entries = _load_index()
        remaining = [e for e in entries if e["doc_id"] != doc_id]
        if len(remaining) == len(entries):
            return False
        _save_index(remaining)

    delete_by_doc_id(doc_id)

    for f in settings.upload_path.glob(f"{doc_id}_*"):
        try:
            f.unlink()
        except OSError:
            pass
    return True
