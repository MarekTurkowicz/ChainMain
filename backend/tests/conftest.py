"""Pytest configuration: isolate data dirs and stub OpenAI-dependent modules.

Tests should run with NO network access and NO OPENAI_API_KEY.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))


@pytest.fixture(autouse=True)
def isolated_env(tmp_path, monkeypatch):
    """Point every path-using setting at a tmp_path so tests don't touch real data."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    monkeypatch.setenv("UPLOAD_DIR", str(tmp_path / "uploads"))
    monkeypatch.setenv("CHROMA_DIR", str(tmp_path / "chroma"))
    monkeypatch.setenv("METADATA_FILE", str(tmp_path / "documents.json"))

    # Force re-import of config + dependents so fresh env is picked up.
    # Also pop package roots — otherwise `from rag import embeddings` would
    # return a stale attribute from the cached `rag` package, bypassing the
    # fresh module we expect to be re-imported.
    targets = ("config", "main", "rag", "services", "routes")
    for mod in list(sys.modules):
        if mod in targets or mod.startswith(tuple(f"{t}." for t in targets)):
            sys.modules.pop(mod, None)
    yield


class _FakeEmbeddings:
    """Deterministic bag-of-characters embedding — no network, stable, trivial."""

    dim = 64

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(t) for t in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)

    def _embed(self, text: str) -> list[float]:
        vec = [0.0] * self.dim
        for ch in text.lower():
            vec[ord(ch) % self.dim] += 1.0
        norm = sum(v * v for v in vec) ** 0.5 or 1.0
        return [v / norm for v in vec]


@pytest.fixture
def fake_embeddings(monkeypatch):
    from rag import embeddings as emb_mod

    fake = _FakeEmbeddings()
    emb_mod.get_embeddings.cache_clear()
    monkeypatch.setattr(emb_mod, "get_embeddings", lambda: fake)
    return fake
