# ChainMain

> Chat with your documents. Upload a PDF or TXT, ask questions in natural language, get grounded answers with source citations — live-streamed token by token.

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Vue-3-4FC08D?logo=vuedotjs&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-RAG-1C3C3C)
![Chroma](https://img.shields.io/badge/Chroma-vector--db-orange)

---

## What it does

1. **Upload** PDF or TXT files via drag & drop
2. **Index** — files are split into chunks, embedded with OpenAI, stored in a local Chroma vector DB
3. **Ask** — questions go through semantic search → top-K chunks → LLM with grounding prompt
4. **Stream** — the answer appears token-by-token via SSE; sources show which file and page each claim came from
5. **Inspect** — click any source chip to open a side panel with the matched chunk plus its neighbors for context

---

## Stack

| Layer | Tech |
|---|---|
| Backend | FastAPI · LangChain · Chroma · OpenAI (`gpt-4o-mini` + `text-embedding-3-small`) |
| Frontend | Vue 3 · Vite · SSE streaming |
| Storage | Chroma (local, persistent) · JSON metadata index |
| Tests | pytest (12 tests, no network) · Playwright (e2e config) |

---

## Quick start

### 1. Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # then set OPENAI_API_KEY in .env

uvicorn main:app --reload --port 9000
```

API: `http://localhost:9000` · Swagger: `http://localhost:9000/docs`

### 2. Frontend

```bash
cd frontend
npm install
npm run dev                 # http://localhost:9001
```

### 3. Run tests

```bash
cd backend
pytest                      # 12 unit tests, no API key needed
```

---

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload` | Upload PDF/TXT, index into Chroma |
| `POST` | `/ask` | SSE streaming Q&A with sources |
| `GET` | `/documents` | List indexed documents |
| `DELETE` | `/documents/{id}` | Remove document + vectors |
| `GET` | `/chunks/{id}` | Fetch chunk + neighbor context window |
| `GET` | `/health` | Config + liveness check |

---

## Project layout

```
ChainMain/
├── backend/
│   ├── main.py              # FastAPI app, CORS, router wiring
│   ├── config.py            # Settings via pydantic-settings + .env
│   ├── routes/              # upload · ask · documents · chunks
│   ├── services/            # document_service · qa_service
│   ├── rag/                 # loader → splitter → embeddings → vectorstore → retriever → pipeline
│   ├── models/schemas.py    # Pydantic models
│   └── tests/               # 12 pytest unit tests
│
└── frontend/
    └── src/
        ├── App.vue
        ├── components/      # Upload · Chat · Message · DocumentList · ChunkPreview
        └── services/api.js  # fetch + SSE consumer
```

---

## Configuration

All settings live in `backend/.env` (copy from `.env.example`):

```env
OPENAI_API_KEY=sk-...
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=4
MAX_UPLOAD_MB=20
```

---

## Roadmap

- [x] RAG pipeline (upload → index → ask → stream)
- [x] Per-document filter (search only selected files)
- [x] Source chip → chunk context panel with neighbors
- [x] Upload validation (size, extension, MIME)
- [x] Server-side stream cancel on client disconnect
- [ ] Conversation memory (follow-up questions)
- [ ] Persistent chat history (SQLite)
- [ ] Reranking (cross-encoder)
- [ ] Local models — Ollama + `sentence-transformers`
- [ ] Auth + rate limiting
- [ ] Docker Compose one-command start
