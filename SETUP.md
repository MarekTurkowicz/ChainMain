# ChainMain Setup Guide

Complete setup and usage instructions for the RAG application.

## 📋 Prerequisites

- **Python** 3.10+ (check with `python --version`)
- **Node.js** 18+ (check with `node --version`)
- **Poetry** (Python dependency manager) - [Install here](https://python-poetry.org/docs/#installation)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

## 🚀 Quick Start

### 1. Backend Setup (FastAPI + RAG)

```bash
cd backend

# Create and activate virtual environment
python -m venv chainmain-venv

# Windows:
chainmain-venv\Scripts\activate
# macOS/Linux:
source chainmain-venv/bin/activate

# Install dependencies using Poetry
poetry install

# Create .env file
cp .env.example .env

# ⚠️ IMPORTANT: Edit .env and add your OpenAI API key
# nano .env   (or edit in your editor)
# OPENAI_API_KEY=sk-...

# Start the backend server
uvicorn main:app --reload --port 9000
```

**Backend is ready** → http://localhost:9000  
**API Docs** → http://localhost:9000/docs

### 2. Frontend Setup (Vue 3 + Playwright Tests)

**In a new terminal:**

```bash
cd frontend

# Install dependencies
npm install

# Start the dev server
npm run dev
```

**Frontend is ready** → http://localhost:9001

---

## 💬 Using ChainMain

### In the Browser (http://localhost:9001)

1. **Upload Documents**
   - Click the dropzone or drag files
   - Supports PDF and TXT files
   - Files are indexed in Chroma immediately

2. **Select Documents** (optional)
   - Check documents in the sidebar
   - Only selected documents will be used for Q&A
   - Leave all unchecked to search all documents

3. **Ask Questions**
   - Type a question in the chat box
   - Press **Enter** or click **Ask**
   - Streaming response with sources appears below

4. **Source Citations**
   - Each answer includes source documents
   - Click sources to see which file the answer came from

---

## 🧪 Running Tests

### Unit Tests (Backend)

```bash
cd backend
source chainmain-venv/bin/activate  # or chainmain-venv\Scripts\activate on Windows

pytest                      # Run all tests
pytest -v                   # Verbose output
pytest tests/test_pipeline.py -v  # Single test file
```

### E2E Tests (Frontend with Playwright)

**Prerequisites:** Backend and frontend must be running

```bash
cd frontend

# Install Playwright browsers (first time only)
npm run playwright:install

# Run tests (headless)
npm run test:e2e

# Run tests with UI (visual debugging)
npm run test:e2e:ui

# Run specific test file
npx playwright test e2e/app.spec.js

# Run tests in headed mode (see browser)
npx playwright test --headed

# Debug mode with Playwright Inspector
npx playwright test --debug
```

### View Test Report

After tests run:

```bash
npx playwright show-report
```

---

## 📁 Project Structure

```
ChainMain/
├── backend/                      # FastAPI backend
│   ├── main.py                  # FastAPI app entry
│   ├── config.py                # Settings & environment
│   ├── pyproject.toml           # Python dependencies (Poetry)
│   ├── requirements.txt          # Legacy requirements
│   ├── .env.example             # Environment template
│   ├── chainmain-venv/          # Virtual environment (do not commit)
│   ├── models/                  # Pydantic models
│   ├── routes/                  # API endpoints
│   │   ├── upload.py            # POST /api/upload
│   │   ├── ask.py               # POST /api/ask (SSE streaming)
│   │   └── documents.py         # GET/DELETE /api/documents
│   ├── services/                # Business logic
│   │   ├── document_service.py  # Document management
│   │   └── qa_service.py        # Q&A logic
│   ├── rag/                     # RAG pipeline
│   │   ├── loader.py            # File loading
│   │   ├── splitter.py          # Text chunking
│   │   ├── embeddings.py        # Vector embeddings
│   │   ├── vectorstore.py       # Chroma integration
│   │   ├── retriever.py         # Document retrieval
│   │   └── pipeline.py          # Full RAG pipeline
│   └── tests/                   # Unit tests
│
├── frontend/                     # Vue 3 SPA
│   ├── node_modules/            # npm packages (do not commit)
│   ├── src/
│   │   ├── App.vue              # Main layout
│   │   ├── main.js              # Vue app entry
│   │   ├── services/
│   │   │   └── api.js           # API client (fetch)
│   │   └── components/
│   │       ├── Upload.vue       # File upload
│   │       ├── Chat.vue         # Chat interface
│   │       ├── DocumentList.vue # Sidebar documents
│   │       └── Message.vue      # Message display
│   ├── index.html               # HTML template
│   ├── package.json             # Node.js dependencies
│   ├── vite.config.js           # Vite config
│   ├── playwright.config.js     # E2E test config
│   └── e2e/                     # Playwright tests
│       └── app.spec.js          # E2E test suite
│
├── README.md                    # Project overview
└── SETUP.md                     # This file
```

---

## 🔧 API Endpoints

### Health Check
```
GET /health
```
Returns system config and models being used.

### Upload Document
```
POST /api/upload
Content-Type: multipart/form-data

Body:
  file: <PDF or TXT file>

Response:
  {
    "doc_id": "uuid",
    "filename": "example.pdf",
    "pages": 10,
    "chunks": 45
  }
```

### Ask Question (Streaming SSE)
```
POST /api/ask
Content-Type: application/json

Body:
  {
    "question": "What is machine learning?",
    "doc_ids": ["uuid1", "uuid2"]  // optional, null = search all
  }

Events:
  { "type": "token", "data": "Machine learning is..." }
  { "type": "sources", "data": [{"doc_id": "...", "text": "...", "page": 1}] }
  { "type": "done" }
```

### List Documents
```
GET /api/documents

Response:
  {
    "documents": [
      {"doc_id": "uuid", "filename": "x.pdf", "pages": 5, "chunks": 20},
      ...
    ]
  }
```

### Delete Document
```
DELETE /api/documents/{doc_id}
```

---

## 🌍 Environment Variables

Create `backend/.env`:

```env
# OpenAI API
OPENAI_API_KEY=sk-...

# Server
BACKEND_ORIGIN=http://localhost:9000
FRONTEND_ORIGIN=http://localhost:9001

# RAG Pipeline
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o-mini
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
TOP_K=5

# Storage
DATA_DIR=./data
```

---

## 🐛 Troubleshooting

### Backend won't start
```
Error: ModuleNotFoundError: No module named 'fastapi'
→ Activate venv: source chainmain-venv/bin/activate
→ Install deps: pip install -r requirements.txt  (or poetry install)
```

### Frontend can't connect to backend
```
Error: POST /api/upload failed
→ Check if backend is running on port 9000
→ Check CORS settings in backend/main.py
→ Frontend FRONTEND_ORIGIN must match your setup
```

### Playwright tests fail
```
Error: Browser not found
→ Run: npm run playwright:install

Error: connection refused
→ Make sure frontend (9001) and backend (9000) are running
```

### OpenAI API errors
```
Error: Invalid API key
→ Check .env file has valid OPENAI_API_KEY
→ Get key from: https://platform.openai.com/api-keys

Error: Rate limited
→ Wait a moment and retry
→ Check your API quota
```

---

## 📚 Learning Resources

- **FastAPI**: https://fastapi.tiangolo.com/
- **LangChain**: https://python.langchain.com/
- **Chroma**: https://www.trychroma.com/
- **Vue 3**: https://vuejs.org/
- **Playwright**: https://playwright.dev/

---

## 🎯 Next Steps

1. ✅ Install dependencies
2. ✅ Set up `.env` file
3. ✅ Start backend and frontend
4. ✅ Upload a document
5. ✅ Ask a question
6. ✅ Run E2E tests

Happy chatting with your documents! 🚀
