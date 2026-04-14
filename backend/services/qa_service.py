from __future__ import annotations

from typing import AsyncIterator

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from config import settings
from models.schemas import SourceChunk
from rag.retriever import retrieve


SYSTEM_PROMPT = """You are a precise assistant answering questions about the user's documents.

Rules:
- Answer ONLY using the context below. If the answer is not present, say: "I don't know based on the provided documents."
- Cite sources inline using their tag, e.g. [Source 1], [Source 2].
- Be concise and factual. Do not speculate.
"""


def _format_context(chunks: list[Document]) -> str:
    lines: list[str] = []
    for i, doc in enumerate(chunks, start=1):
        filename = doc.metadata.get("filename", "unknown")
        page = doc.metadata.get("page")
        tag = f"[Source {i} — {filename}" + (f", p. {page + 1}" if isinstance(page, int) else "") + "]"
        lines.append(f"{tag}\n{doc.page_content}")
    return "\n\n".join(lines)


def _to_source_chunks(pairs: list[tuple[Document, float]]) -> list[SourceChunk]:
    sources: list[SourceChunk] = []
    for doc, score in pairs:
        page = doc.metadata.get("page")
        sources.append(
            SourceChunk(
                doc_id=doc.metadata.get("doc_id", ""),
                filename=doc.metadata.get("filename", "unknown"),
                page=(page + 1) if isinstance(page, int) else None,
                chunk_id=doc.metadata.get("chunk_id", ""),
                text=doc.page_content,
                score=score,
            )
        )
    return sources


def _build_llm() -> ChatOpenAI:
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. See backend/.env.example.")
    return ChatOpenAI(
        model=settings.llm_model,
        api_key=settings.openai_api_key,
        temperature=0.0,
        streaming=True,
    )


async def answer_stream(
    question: str,
    doc_ids: list[str] | None = None,
) -> AsyncIterator[dict]:
    """Yield SSE-friendly events: token, sources, done."""
    pairs = retrieve(question, doc_ids=doc_ids)
    chunks = [doc for doc, _ in pairs]

    if not chunks:
        yield {"type": "token", "data": "I don't know based on the provided documents."}
        yield {"type": "sources", "data": []}
        yield {"type": "done"}
        return

    context = _format_context(chunks)
    messages = [
        ("system", SYSTEM_PROMPT),
        ("user", f"Context:\n{context}\n\nQuestion: {question}"),
    ]

    llm = _build_llm()
    async for chunk in llm.astream(messages):
        token = getattr(chunk, "content", "")
        if token:
            yield {"type": "token", "data": token}

    yield {"type": "sources", "data": [s.model_dump() for s in _to_source_chunks(pairs)]}
    yield {"type": "done"}
