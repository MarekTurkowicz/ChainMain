from __future__ import annotations

from io import BytesIO


def _client(monkeypatch):
    from fastapi.testclient import TestClient

    from main import app
    from routes import upload as upload_route

    def fake_save(filename, content, mime_type):
        from models.schemas import DocumentInfo
        from datetime import datetime, timezone

        return DocumentInfo(
            doc_id="stub",
            filename=filename,
            mime_type=mime_type,
            chunk_count=1,
            uploaded_at=datetime.now(timezone.utc),
        )

    monkeypatch.setattr(upload_route.document_service, "save_and_index", fake_save)
    return TestClient(app)


def test_upload_rejects_unsupported_extension(monkeypatch):
    client = _client(monkeypatch)
    r = client.post(
        "/upload",
        files={"file": ("evil.exe", BytesIO(b"MZ"), "application/octet-stream")},
    )
    assert r.status_code == 415
    assert "extension" in r.json()["detail"].lower()


def test_upload_rejects_unsupported_mime(monkeypatch):
    client = _client(monkeypatch)
    r = client.post(
        "/upload",
        files={"file": ("doc.pdf", BytesIO(b"%PDF-1.4"), "image/png")},
    )
    assert r.status_code == 415
    assert "mime" in r.json()["detail"].lower()


def test_upload_rejects_oversized(monkeypatch):
    monkeypatch.setenv("MAX_UPLOAD_MB", "1")
    client = _client(monkeypatch)
    payload = b"x" * (2 * 1024 * 1024)
    r = client.post(
        "/upload",
        files={"file": ("big.txt", BytesIO(payload), "text/plain")},
    )
    assert r.status_code == 413


def test_upload_accepts_valid_txt(monkeypatch):
    client = _client(monkeypatch)
    r = client.post(
        "/upload",
        files={"file": ("notes.txt", BytesIO(b"hello world"), "text/plain")},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["filename"] == "notes.txt"
    assert body["chunk_count"] == 1
