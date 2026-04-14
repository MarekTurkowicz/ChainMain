# TODO

Keep this list pruned. Check items off when done, add new ones as they come up.

## MVP (must-have)

- [x] Project scaffolding (backend + frontend folders)
- [x] Backend: FastAPI app with CORS
- [x] Backend: `.env` loading via pydantic-settings
- [x] Backend: `POST /upload` (PDF + TXT)
- [x] Backend: RAG pipeline (load → split → embed → store)
- [x] Backend: Chroma persistent vector store
- [x] Backend: `POST /ask` with source attribution
- [x] Backend: `GET /documents` listing
- [x] Backend: streaming responses (SSE)
- [x] Frontend: Vue 3 + Vite scaffolding, dev server on 9001
- [x] Frontend: Upload component (drag & drop)
- [x] Frontend: Chat interface (history + input)
- [x] Frontend: display sources under each answer
- [x] Frontend: loading states
- [x] Frontend: API service layer
- [x] Docs: README, PROJECT_STRUCTURE, HOW_IT_WORKS, TODO

## Next up (nice-to-have)

- [ ] Delete document endpoint (`DELETE /documents/{id}`) + cascade remove from Chroma
- [ ] File filter in UI (checkbox per document to scope question)
- [ ] Chunk preview modal (click a source to see surrounding context)
- [ ] Conversation memory (follow-up questions using chat history)
- [ ] Reranking (e.g. Cohere rerank or cross-encoder) before LLM
- [ ] Persistent chat history (SQLite)
- [ ] Auth (API key or basic session)

## Future / exploratory

- [ ] Local embeddings (e.g. `sentence-transformers`) toggle in `rag/embeddings.py`
- [ ] Local LLM support (Ollama) behind a provider flag
- [ ] Hybrid search (BM25 + dense) via `EnsembleRetriever`
- [ ] Evaluation harness (RAGAS or custom) with a tiny golden set
- [ ] Dockerfile + docker-compose for one-command start
- [ ] Unit tests for splitter and retriever
- [ ] E2E test: upload → ask → assert source chunk

## Known limitations

- No auth — do not deploy publicly as-is
- No rate limiting
- Chroma runs in-process (fine for MVP, swap for a service at scale)
- Large PDFs are parsed synchronously (blocks the request)
