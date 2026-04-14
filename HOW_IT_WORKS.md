# How It Works

A plain-English walkthrough of the RAG system. No code here — read this alongside the source if you want to understand the *why*.

---

## 1. The Problem RAG Solves

Large language models are frozen at training time and don't know about your private documents. Rather than fine-tuning (expensive) or cramming everything into a prompt (impossible at scale), **Retrieval-Augmented Generation** does two things:

1. **Retrieve** — find the small slices of your corpus that look relevant to the user's question.
2. **Generate** — hand those slices to an LLM as context and ask it to answer *based on them*.

The retriever keeps the prompt small and focused; the generator turns raw text into a fluent answer. The LLM cites which slices it used, so the user can verify.

---

## 2. The Ingestion Pipeline (what happens on `POST /upload`)

When a user uploads a file, five stages run in order:

### Stage 1 — Persist the raw file
The file is streamed to `backend/data/uploads/<uuid>_<original-name>`. We keep the UUID so filename collisions don't matter, and the original name for display. Metadata (doc id, filename, mime, chunk count, timestamp) is tracked in a tiny JSON index next to the uploads folder.

### Stage 2 — Load
A LangChain document loader turns the file into `Document` objects. PDFs go through `PyPDFLoader`, which produces **one Document per page** with page-number metadata. Plain `.txt` files go through `TextLoader` (one Document for the whole file). The loader abstraction matters: adding `.docx` or `.md` later is just a new branch.

### Stage 3 — Split (chunking with overlap)
Full pages are too big to embed usefully (they dilute semantic meaning) and too big to fit many of them into an LLM context. So each Document is split into chunks of ~1000 characters with ~200 characters of **overlap**.

**Why overlap?** A sentence that starts at the end of chunk N may finish at the start of chunk N+1. Without overlap, retrieving one chunk loses half the thought. Overlap ensures any sentence is fully contained in at least one chunk, at the cost of a bit of duplicate storage. 20% overlap is a common sweet spot.

The splitter is `RecursiveCharacterTextSplitter`: it tries to split on paragraph breaks first, then newlines, then sentences, then words — preserving semantic boundaries where possible.

Each chunk inherits the parent Document's metadata (filename, doc id, page number) and gets a fresh `chunk_id`. This metadata is what lets us show the user *which part of which file* an answer came from.

### Stage 4 — Embed
Each chunk's text is sent to the embedding model (OpenAI `text-embedding-3-small` by default). The model returns a fixed-length vector (1536 dimensions) that represents the chunk's meaning in semantic space. Semantically similar texts produce vectors that are close under cosine distance — that's the whole trick.

The embeddings module is an abstraction: swapping to a local model (e.g. `sentence-transformers`) is a one-function change because everything downstream only depends on the LangChain `Embeddings` interface.

### Stage 5 — Store
Chunks + vectors + metadata are written to **Chroma**, a local, persistent vector database. Chroma runs in-process and writes to `backend/data/chroma/`. Each chunk becomes a row keyed by `chunk_id` with its vector, the original text, and metadata for filtering.

We use a single Chroma collection (`documents`) for everything. To scope a query to one file, we filter on the `doc_id` metadata field at query time — simpler than multiple collections and just as fast for typical corpora.

---

## 3. The Query Pipeline (what happens on `POST /ask`)

### Stage 1 — Embed the question
The user's question goes through the *same* embedding model as the chunks. This is non-negotiable: you can only compare vectors that live in the same space.

### Stage 2 — Retrieve
Chroma runs a cosine-similarity search and returns the top K chunks (default K=4). If the request included a `doc_ids` filter, the search is restricted to those documents via metadata filtering — done inside Chroma, not as a post-filter, so you still get K results even if the filter is restrictive.

### Stage 3 — Build the prompt
The retrieved chunks are concatenated into a **context block**, each prefixed with a short tag like `[Source 1 — filename.pdf, p. 3]`. This is then wrapped in a system prompt that tells the LLM: *"Answer using only the context below. If the context doesn't contain the answer, say so. Cite sources by tag."*

Two subtle things:
- **Answer refusal:** the prompt explicitly instructs the model to say "I don't know" rather than guess. This matters — LLMs will confabulate if you let them.
- **Tag-based citation:** the model is told to reference `[Source N]` in its answer. The frontend then renders each source chunk the LLM actually cited.

### Stage 4 — Generate (streaming)
The prompt is sent to the chat model (`gpt-4o-mini` by default) with `stream=True`. Tokens are forwarded to the client as **Server-Sent Events** so the UI renders the answer as it's produced — which feels ~3× faster than waiting for the full response.

### Stage 5 — Attach sources
After the stream completes, one final SSE event carries the source chunks (text + metadata) as a JSON payload. The frontend shows these below the answer so the user can verify every claim.

---

## 4. Why These Specific Choices

### Why FastAPI?
Native async (needed for streaming), automatic OpenAPI docs, Pydantic validation for free. It's the standard for Python AI backends in 2025/2026.

### Why LangChain?
Not because it's elegant — it isn't — but because it has *every* loader, splitter, retriever, and vector store glued together with a consistent interface. When you want to try a new chunking strategy or add reranking, you swap one object.

### Why Chroma (not Pinecone, Weaviate, pgvector)?
Zero setup, persistent to disk, good enough up to ~1M vectors. Perfect for an MVP. At scale, swap the `vectorstore.py` module — everything else stays.

### Why OpenAI embeddings (with an abstraction)?
Quality-per-dollar is still unbeaten for general text. But the `embeddings.py` module hides the provider, so moving to `bge-small` or `nomic-embed-text` locally is a one-file change. Lock-in is avoided at the architecture level.

### Why SSE and not WebSockets?
Streaming is unidirectional (server → client), SSE is simpler, works over plain HTTP, auto-reconnects in the browser, and doesn't need a separate protocol upgrade. WebSockets are overkill here.

### Why Vue 3 (Composition API)?
Lighter than React for a small app, SFCs keep component code colocated, `<script setup>` makes reactive state near-invisible. Vite gives instant HMR. Good ergonomics for a thin frontend.

---

## 5. Data Flow (end-to-end)

```
User drops file in browser
        │
        ▼
POST /upload (multipart)
        │
        ▼
document_service.save_and_index()
        │
        ├── write file to data/uploads/
        │
        ▼
rag/pipeline.ingest()
        │
        ├── loader.load() ──► Documents
        ├── splitter.split() ──► Chunks (w/ metadata)
        ├── embeddings.embed_documents() ──► Vectors
        └── vectorstore.add() ──► Chroma (persisted)
        │
        ▼
Return {doc_id, filename, chunk_count}

========================================================

User types question in chat
        │
        ▼
POST /ask {question, doc_ids?}
        │
        ▼
qa_service.answer_stream()
        │
        ├── retriever.get_relevant(question, filter) ──► top-K chunks
        ├── build prompt with [Source N] tags
        ├── llm.stream(prompt) ──► token stream
        │                               │
        │      ┌────────────────────────┘
        │      ▼
        │   SSE event: {"type":"token","data":"..."}
        │      (repeated per token)
        │
        └── on finish:
            SSE event: {"type":"sources","data":[...]}
            SSE event: {"type":"done"}
        │
        ▼
Frontend renders answer live, then sources below.
```

---

## 6. Tuning Knobs That Actually Matter

| Knob | Where | Effect |
|---|---|---|
| `CHUNK_SIZE` | `config.py` | Larger = more context per chunk, fewer chunks, coarser retrieval. Smaller = precise retrieval but fragmented answers. 800–1200 chars is typical. |
| `CHUNK_OVERLAP` | `config.py` | Too little → lost sentences at boundaries. Too much → wasted storage and duplicate hits in top-K. 10–25% of chunk size. |
| `TOP_K` | `config.py` | More chunks = better recall but dilutes the prompt and costs more tokens. 3–6 is the sweet spot. |
| Embedding model | `rag/embeddings.py` | Bigger model = better recall on nuanced queries, higher cost. |
| LLM temperature | `services/qa_service.py` | Keep low (0–0.2) for factual RAG — creativity = hallucination risk. |

---

## 7. What This Is NOT

- **Not production multi-tenant.** Every user shares one Chroma collection. Add auth + per-user namespaces if that matters.
- **Not a chatbot with memory.** Each `/ask` call is independent. Follow-ups don't see prior turns. Add a conversation buffer when needed.
- **Not agentic.** The LLM can't call tools or iterate — it answers once from retrieved context. That's deliberate: most "chat with your docs" use cases don't need agents, and agents add latency, cost, and failure modes.

---

## 8. Common Failure Modes (and what to check)

| Symptom | Likely cause |
|---|---|
| "I don't know" on obvious questions | Chunks too small, or K too low, or query uses different vocabulary than doc |
| Answer contradicts the source | Temperature too high, or context window overflowed and got truncated |
| Retrieval returns irrelevant chunks | Embedding model mismatch between ingest and query (must be the same!) |
| Slow uploads | Large PDFs — offload to a background task (Celery/RQ) for production |
| `OPENAI_API_KEY` errors | `.env` not loaded — check working directory when running `uvicorn` |
