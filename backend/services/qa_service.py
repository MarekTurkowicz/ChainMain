from __future__ import annotations

from typing import AsyncIterator

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from config import settings
from models.schemas import SourceChunk
from rag.retriever import retrieve


SYSTEM_PROMPT = """Jesteś precyzyjnym asystentem odpowiadającym na pytania dotyczące dokumentów użytkownika.

Zasady:
- Odpowiadaj WYŁĄCZNIE na podstawie poniższego kontekstu. Jeśli odpowiedź nie jest zawarta w dokumentach, powiedz: „Nie wiem na podstawie dostarczonych dokumentów."
- Cytuj źródła inline używając ich tagu, np. [Źródło 1], [Źródło 2].
- Bądź zwięzły i rzeczowy. Nie spekuluj.
- Zawsze odpowiadaj po polsku, niezależnie od języka pytania.
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
