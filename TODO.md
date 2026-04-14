# TODO

Keep this list pruned. Check items off when done, add new ones as they come up.

> Last updated: 2026-04-14

## 🔜 Start here tomorrow

1. **Install & smoke test**
   - [ ] `cd backend && python -m venv .venv && source .venv/Scripts/activate && pip install -r requirements.txt`
   - [ ] Copy `.env.example` → `.env`, set `OPENAI_API_KEY`
   - [ ] `pytest` — should be green (uses fake embeddings, no network)
   - [ ] `uvicorn main:app --reload --port 9000` → `http://localhost:9000/health`
   - [ ] `cd frontend && npm install && npm run dev` → `http://localhost:9001`
   - [ ] Upload a small PDF, ask a question, verify streaming + sources
2. **Playwright** (parked by choice — add when you want it)
   - [ ] Add `playwright.config.js` + `tests/e2e/happy_path.spec.js`
   - [ ] Scripts in `package.json`: `test:e2e`, `playwright:install`
   - [ ] Stub `/api/upload`, `/api/documents`, `/api/ask` (SSE) or run real backend
3. **Git flow**
   - [ ] Current branch: `feat/frontend-mvp`. When ready: PR → `dev`. When dev verified → `main`.

## MVP (must-have)

- [x] Project scaffolding (backend + frontend folders)
- [x] Backend: FastAPI app with CORS (port 9000)
- [x] Backend: `.env` loading via pydantic-settings
- [x] Backend: `POST /upload` (PDF + TXT)
- [x] Backend: RAG pipeline (load → split → embed → store)
- [x] Backend: Chroma persistent vector store
- [x] Backend: `POST /ask` with SSE streaming + source attribution
- [x] Backend: `GET /documents` listing
- [x] Backend: `DELETE /documents/{id}` (cascade into Chroma + uploads)
- [x] Backend: pytest smoke tests (splitter, pipeline, health) with fake embeddings
- [x] Frontend: Vue 3 + Vite scaffolding, dev server on 9001 with `/api` proxy
- [x] Frontend: Upload component (drag & drop, multi-file)
- [x] Frontend: DocumentList with per-doc filter checkboxes + delete
- [x] Frontend: Chat interface (SSE streaming, stop button, sources with expand)
- [x] Frontend: modern dark theme, fast transitions (no long loaders)
- [x] Docs: README, PROJECT_STRUCTURE, HOW_IT_WORKS, TODO
- [x] Git: `main` + `dev` + `feat/frontend-mvp` branches, Claude artifacts gitignored

## Next up (nice-to-have)

- [ ] **Playwright e2e** (postponed): upload → ask → assert sources visible
- [ ] Backend: streaming error mid-answer — currently appends `⚠` in UI, could add retry
- [ ] Backend: chunk preview endpoint (`GET /chunks/{chunk_id}`) for surrounding context
- [ ] Frontend: click a source chip → jump to/highlight in a document preview pane
- [ ] Conversation memory (follow-up questions using chat history)
- [ ] Reranking (Cohere or cross-encoder) before the LLM
- [ ] Persistent chat history (SQLite)
- [ ] Auth (API key in header, or a lightweight session)
- [ ] Rate limiting on `/ask`
- [ ] File size limit + large-file background indexing (Celery/RQ)

## Added mid-session (discovered while writing)

- [ ] Backend: swap `langchain` `1.2.x` for stable channel if breaking changes hit
- [ ] Confirm `langchain-chroma>=0.2.5` matches `chromadb>=1.5.7` (API drift risk)
- [ ] Frontend: `npm install` currently requires Node 20+ (Vite 7). Document in README?
- [ ] Wire `Stop` button to also cancel server-side generation (currently only aborts the fetch)
- [ ] `.env.example` has `OPENAI_API_KEY` — add a clearer note that tests don't need it
- [ ] Add a one-command dev script (`make dev` or `concurrently` at repo root) to start both servers
- [ ] Consider `uv` instead of `pip` for faster installs (personal preference)

## Future / exploratory

- [ ] Local embeddings (`sentence-transformers`) toggle in `rag/embeddings.py`
- [ ] Local LLM support (Ollama) behind a provider flag
- [ ] Hybrid search (BM25 + dense) via `EnsembleRetriever`
- [ ] Evaluation harness (RAGAS or custom) with a tiny golden set
- [ ] Dockerfile + docker-compose for one-command start
- [ ] More test coverage: upload route (with monkeypatched pipeline), ask route (mocked LLM stream)

## Known limitations

- No auth — do not deploy publicly as-is
- No rate limiting
- Chroma runs in-process (fine for MVP, swap for a service at scale)
- Large PDFs are parsed synchronously (blocks the request)
- `Stop` only aborts the client; the backend LLM call may continue until completion
