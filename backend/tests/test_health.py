from __future__ import annotations

from fastapi.testclient import TestClient


def test_health_endpoint_reports_settings():
    from main import app

    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert "embedding_model" in body
    assert body["chunk_size"] > 0


def test_documents_empty_by_default():
    from main import app

    client = TestClient(app)
    r = client.get("/documents")
    assert r.status_code == 200
    assert r.json() == {"documents": []}
