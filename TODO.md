# TODO

Keep this list pruned. Check items off when done, add new ones as they come up.

> Last updated: 2026-04-15

## 🔜 Start here tomorrow

1. **Manual smoke test of Phase 1 work** (browser)
   - [ ] Upload PDF → ask → click a source chip → context panel opens with neighbors
   - [ ] Hit Stop mid-stream → backend stops generating (check logs)
   - [ ] Kill backend mid-stream → Retry button appears → restart backend → Retry works
   - [ ] Try uploading a 25 MB file → 413; try `.exe` → 415
2. **Merge Phase 1**
   - [ ] PR `feat/frontend-mvp` → `dev`, verify, then `dev` → `main`
3. **Open new branch for Phase 2**: `feat/conversation-memory`

## Roadmap (post-MVP)

### Phase 1 — Stability & UX polish ✅ DONE
- [x] Backend: cancel SSE on client disconnect (`request.is_disconnected()` + `aclose()`)
- [x] Backend: upload validation — file size limit (MAX_UPLOAD_MB), extension + MIME allowlist
- [x] Backend: `GET /chunks/{id}?window=N` returns chunk + neighbors (uses new `chunk_index` metadata)
- [x] Frontend: source chip → side panel with target chunk highlighted + neighbors
- [x] Frontend: Retry button on stream error (replaces inline `⚠` text)
- [x] Tests: upload validation + chunk preview endpoint; flaky-conftest fix (pop package roots)

### Phase 2 — Conversation memory & answer quality
- [ ] **Conversation memory** — last N Q/A pairs in context; condense follow-up questions
- [ ] **Persistent chat history** — SQLite (`conversations`, `messages` tables); `GET/POST /conversations`
- [ ] **Reranking** — cross-encoder (e.g. `bge-reranker`) after retrieve, before LLM
- [ ] **Hybrid search** — BM25 + dense via `EnsembleRetriever`
- [ ] Frontend: conversation list sidebar; new-chat button; rename/delete

### Phase 3 — Local models (toggle)
- [ ] Provider flag in `config.py`: `openai` | `ollama` | `local`
- [ ] Local embeddings (`sentence-transformers/paraphrase-multilingual`) — better for PL
- [ ] Local LLM via Ollama (`bielik`, `llama3.1`) — works offline
- [ ] Health endpoint reports the active provider

### Phase 4 — Productionization
- [ ] **Auth** — API key header or lightweight session
- [ ] **Rate limiting** on `/ask` (`slowapi`)
- [ ] **Dockerfile + docker-compose** — one-command start
- [ ] **Eval harness** — RAGAS + ~20-question Polish golden set
- [ ] **Background indexing** for large PDFs (BackgroundTasks first, RQ+Redis if needed)

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

## Loose / unscheduled

- [ ] Playwright e2e: write actual happy-path test (config exists, spec is a stub)
- [ ] Large-file background indexing (Celery/RQ) — only if file size limit gets bumped

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
