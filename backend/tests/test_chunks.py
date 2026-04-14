from __future__ import annotations

from pathlib import Path


def test_get_chunk_returns_target_and_neighbors(tmp_path: Path, fake_embeddings):
    from fastapi.testclient import TestClient

    from main import app
    from rag.pipeline import ingest
    from rag.vectorstore import get_store

    sample = tmp_path / "doc.txt"
    sample.write_text(
        ("Lorem ipsum dolor sit amet. " * 200),
        encoding="utf-8",
    )
    chunk_count = ingest(sample, doc_id="docX", filename="doc.txt")
    assert chunk_count >= 3, "Need multiple chunks to exercise the neighbor window"

    res = get_store().get(where={"doc_id": "docX"})
    metas = res["metadatas"]
    middle = sorted(metas, key=lambda m: m["chunk_index"])[len(metas) // 2]
    target_id = middle["chunk_id"]

    client = TestClient(app)
    r = client.get(f"/chunks/{target_id}", params={"window": 2})
    assert r.status_code == 200
    body = r.json()
    assert body["target"]["chunk_id"] == target_id
    assert body["target"]["is_target"] is True
    assert 1 <= len(body["neighbors"]) <= 4
    indices = [n["chunk_index"] for n in body["neighbors"]]
    assert indices == sorted(indices)


def test_get_chunk_404(fake_embeddings):
    from fastapi.testclient import TestClient

    from main import app

    client = TestClient(app)
    r = client.get("/chunks/does-not-exist")
    assert r.status_code == 404
