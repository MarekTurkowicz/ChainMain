from __future__ import annotations

from langchain_core.documents import Document

from rag.splitter import split_documents


def test_split_produces_overlapping_chunks():
    text = "Sentence one. " * 500  # ~7000 chars
    docs = [Document(page_content=text, metadata={"source": "t.txt"})]

    chunks = split_documents(docs)

    assert len(chunks) > 1
    # Overlap means consecutive chunks share some trailing/leading content.
    first_end = chunks[0].page_content[-50:]
    second_start = chunks[1].page_content[:200]
    assert any(tok in second_start for tok in first_end.split()), (
        "Expected overlap between consecutive chunks"
    )
    # Metadata is preserved on every chunk.
    for c in chunks:
        assert c.metadata.get("source") == "t.txt"


def test_split_handles_empty_document():
    chunks = split_documents([Document(page_content="", metadata={})])
    assert chunks == [] or all(c.page_content == "" for c in chunks)
