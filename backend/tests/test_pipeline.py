from __future__ import annotations

from pathlib import Path


def test_ingest_txt_then_retrieve(tmp_path: Path, fake_embeddings):
    from rag.pipeline import ingest
    from rag.retriever import retrieve

    sample = tmp_path / "sample.txt"
    sample.write_text(
        "The capital of France is Paris. "
        "Python is a programming language created by Guido van Rossum. "
        "The Eiffel Tower is located in Paris, France.\n",
        encoding="utf-8",
    )

    chunk_count = ingest(sample, doc_id="doc-1", filename="sample.txt")
    assert chunk_count >= 1

    results = retrieve("Where is the Eiffel Tower?")
    assert len(results) >= 1
    top_doc, top_score = results[0]
    assert "Eiffel" in top_doc.page_content or "Paris" in top_doc.page_content
    assert top_doc.metadata["doc_id"] == "doc-1"
    assert top_doc.metadata["filename"] == "sample.txt"
    assert 0.0 <= top_score <= 1.0


def test_document_filter_scopes_results(tmp_path: Path, fake_embeddings):
    from rag.pipeline import ingest
    from rag.retriever import retrieve

    a = tmp_path / "a.txt"
    b = tmp_path / "b.txt"
    a.write_text("Alpha document talks about cats and dogs.", encoding="utf-8")
    b.write_text("Beta document talks about spaceships and rockets.", encoding="utf-8")

    ingest(a, doc_id="A", filename="a.txt")
    ingest(b, doc_id="B", filename="b.txt")

    scoped = retrieve("anything", doc_ids=["A"])
    assert scoped, "Expected at least one scoped result"
    assert all(doc.metadata["doc_id"] == "A" for doc, _ in scoped)
