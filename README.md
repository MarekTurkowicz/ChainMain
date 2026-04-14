# ChainMain — RAG Starter

Full-stack Retrieval-Augmented Generation app. Upload PDF/TXT documents, ask questions, get answers with source citations.

**Stack:** FastAPI · LangChain · Chroma · OpenAI · Vue 3 (Vite)

## Ports

- Backend: **9000**
- Frontend: **9001**

## Quick Start

### 1. Backend

```bash
cd backend
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env        # then edit .env and set OPENAI_API_KEY
uvicorn main:app --reload --port 9000
```

Backend runs at `http://localhost:9000`. Docs at `http://localhost:9000/docs`.

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend runs at `http://localhost:9001`.

## Project Docs

- [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) — file-by-file map of the repo (kept updated).
- [TODO.md](TODO.md) — task list and roadmap.
- [HOW_IT_WORKS.md](HOW_IT_WORKS.md) — deep-dive explanation of the RAG pipeline, data flow, and design choices.

## API

| Method | Endpoint     | Purpose                           |
|--------|--------------|-----------------------------------|
| POST   | `/upload`    | Upload PDF/TXT, index into Chroma |
| POST   | `/ask`       | Ask a question (streaming SSE)    |
| GET    | `/documents` | List indexed documents            |

## Environment Variables

See [backend/.env.example](backend/.env.example).
