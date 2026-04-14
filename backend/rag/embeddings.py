from __future__ import annotations

from functools import lru_cache

from langchain_core.embeddings import Embeddings
from langchain_openai import OpenAIEmbeddings

from config import settings


@lru_cache(maxsize=1)
def get_embeddings() -> Embeddings:
    """Return the configured embedding provider.

    Provider abstraction: to plug in a local model (e.g. sentence-transformers,
    Ollama) add a branch here that returns any `Embeddings` implementation —
    callers downstream don't change.
    """
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is not set. See backend/.env.example.")
    return OpenAIEmbeddings(
        model=settings.embedding_model,
        api_key=settings.openai_api_key,
    )
