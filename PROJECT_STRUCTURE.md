# Project Structure

Living map of the repository. Update this file whenever files are added, removed, or significantly changed.

> Last updated: 2026-04-14

## Tree

```
ChainMain/
├── README.md                  # Run instructions and overview
├── PROJECT_STRUCTURE.md       # THIS FILE — file-by-file map
├── TODO.md                    # Roadmap and task checklist
├── HOW_IT_WORKS.md            # Deep-dive technical explanation (no code)
│
├── backend/
│   ├── main.py                # FastAPI app entry, CORS, router wiring
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example           # Template for environment variables
│   ├── .gitignore
│   │
│   ├── config.py              # Settings loaded from .env (pydantic-settings)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── upload.py          # POST /upload — accepts PDF/TXT
│   │   ├── ask.py             # POST /ask — SSE streaming Q&A
│   │   └── documents.py       # GET /documents — list indexed files
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_service.py  # File persistence + indexing orchestration
│   │   └── qa_service.py        # Question answering orchestration
│   │
│   ├── rag/
│   │   ├── __init__.py
│   │   ├── loader.py          # LangChain document loaders (PDF/TXT)
│   │   ├── splitter.py        # RecursiveCharacterTextSplitter wrapper
│   │   ├── embeddings.py      # Embedding provider abstraction (OpenAI now, pluggable)
│   │   ├── vectorstore.py     # Chroma wrapper (add, query, list)
│   │   ├── retriever.py       # Similarity search with optional file filter
│   │   └── pipeline.py        # End-to-end: load → split → embed → store
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py         # Pydantic request/response models
│   │
│   └── data/                  # Runtime-created (gitignored)
│       ├── uploads/           # Raw uploaded files
│       └── chroma/            # Chroma persistent store
│
└── frontend/
    ├── package.json
    ├── vite.config.js         # Dev server on 9001, /api proxy to 9000
    ├── index.html
    ├── .gitignore
    │
    └── src/
        ├── main.js            # Vue app bootstrap
        ├── App.vue            # Layout: Upload + Chat + DocumentList
        ├── style.css          # Global styles
        │
        ├── components/
        │   ├── Upload.vue         # Drag & drop + file picker
        │   ├── Chat.vue           # Message history + input
        │   ├── Message.vue        # Single chat bubble with sources
        │   └── DocumentList.vue   # Sidebar of indexed documents
        │
        └── services/
            └── api.js             # fetch wrappers, SSE consumer
```

## Module Responsibilities (quick reference)

| Module | Responsibility |
|--------|----------------|
| `rag/loader.py` | Turn a file path into LangChain `Document` objects |
| `rag/splitter.py` | Chunk `Document`s with overlap |
| `rag/embeddings.py` | Return a LangChain `Embeddings` instance (provider-abstracted) |
| `rag/vectorstore.py` | Chroma persistence and lookups |
| `rag/retriever.py` | Build a retriever with optional metadata filter |
| `rag/pipeline.py` | Glue: ingest a file into the store |
| `services/document_service.py` | Save file to disk, call pipeline, track metadata |
| `services/qa_service.py` | Retrieve chunks, call LLM, format sources |
| `routes/*` | Thin HTTP layer — validate, delegate, serialize |

## Extension Points

- **Swap embeddings:** implement a new `get_embeddings(provider=...)` branch in `rag/embeddings.py`.
- **Swap vector DB:** reimplement `rag/vectorstore.py` — callers use the abstraction.
- **Swap LLM:** change the model in `services/qa_service.py`.

## Generated / Gitignored

- `backend/.venv/`
- `backend/data/uploads/**`
- `backend/data/chroma/**`
- `frontend/node_modules/`
- `frontend/dist/`
- `**/.env`
