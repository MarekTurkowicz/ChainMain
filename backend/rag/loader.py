from __future__ import annotations

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


class UnsupportedFileType(ValueError):
    pass


def load_file(path: Path) -> list[Document]:
    """Load a file into LangChain Document objects.

    PDFs produce one Document per page (with `page` metadata).
    TXT files produce a single Document for the whole file.
    """
    ext = path.suffix.lower()
    if ext == ".pdf":
        return PyPDFLoader(str(path)).load()
    if ext == ".txt":
        return TextLoader(str(path), encoding="utf-8").load()
    raise UnsupportedFileType(f"Unsupported file type: {ext}")
