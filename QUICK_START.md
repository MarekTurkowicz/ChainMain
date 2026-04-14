# 🚀 ChainMain - Quick Start

Szybki start do uruchomienia aplikacji.

---

## ✅ Co już masz

```
ChainMain/
├── backend/
│   ├── pyproject.toml         ✅ Zależności Python (Poetry)
│   ├── .env                   ✅ Konfiguracja (klucz już wklejony!)
│   ├── main.py
│   ├── config.py
│   ├── routes/
│   ├── services/
│   ├── rag/
│   ├── models/
│   ├── tests/
│   └── data/                  (będzie tworzyć się automatycznie)
│
├── frontend/
│   ├── playwright.config.js   ✅ E2E testy (Playwright)
│   ├── e2e/
│   │   └── app.spec.js        ✅ Test suite (~250 testów)
│   ├── package.json
│   ├── vite.config.js
│   ├── src/
│   │   ├── App.vue
│   │   ├── components/
│   │   └── services/
│   └── node_modules/          (będzie po npm install)
│
├── SETUP.md                   ✅ Pełna instrukcja instalacji
├── HOW_TO_USE.md              ✅ Praktyczny przewodnik
└── QUICK_START.md             ← Ty jesteś tutaj
```

---

## 🎯 3 kroki do uruchomienia

### 1️⃣ Backend (Terminal 1)

```bash
cd backend

# Utwórz venv
python -m venv chainmain-venv

# Aktywuj (Windows)
chainmain-venv\Scripts\activate

# Lub (macOS/Linux)
source chainmain-venv/bin/activate

# Zainstaluj zależności
pip install -r requirements.txt

# Uruchom
uvicorn main:app --reload --port 9000
```

✅ **Powinno pokazać:**
```
INFO:     Application startup complete
INFO:     Uvicorn running on http://127.0.0.1:9000
```

### 2️⃣ Frontend (Terminal 2)

```bash
cd frontend

# Zainstaluj zależności
npm install

# Uruchom
npm run dev
```

✅ **Powinno pokazać:**
```
VITE v7.1.12  ready in XXX ms

➜  Local:   http://localhost:9001/
```

### 3️⃣ Otwórz przeglądarkę

Przejdź do **http://localhost:9001** i testuj! 🎉

---

## 🧪 Uruchomienie testów

### Playwright E2E Tests

```bash
cd frontend

# Zainstaluj przeglądarki (tylko raz)
npm run playwright:install

# Uruchom testy
npm run test:e2e

# Lub z UI (visual debugging)
npm run test:e2e:ui
```

### Backend Unit Tests

```bash
cd backend

# Z aktywnym venv:
pytest
pytest -v
pytest tests/test_pipeline.py -v
```

---

## 📋 Status - Co już działa?

| Komponenta | Status | Notatka |
|-----------|--------|---------|
| **Backend API** | ✅ Gotowy | FastAPI + RAG pipeline |
| **Frontend UI** | ✅ Gotowy | Vue 3 SPA z Vite |
| **Upload dokumentów** | ✅ Gotowy | PDF/TXT support |
| **Chat/Q&A** | ✅ Gotowy | SSE streaming |
| **Playwright tests** | ✅ Gotowy | ~250 testów |
| **Config (pyproject)** | ✅ Gotowy | Poetry ready |
| **.env setup** | ✅ Gotowy | API key już tam |

---

## 🎮 Jak testować aplikację

1. **Uploaduj dokument**
   - Przeciągnij PDF/TXT lub kliknij area
   - Poczekaj aż się pojawi w liście

2. **Zaznacz dokument** (opcjonalnie)
   - Sprawdź checkbox obok dokumentu
   - Tylko zaznaczone będą przeszukiwane

3. **Zadaj pytanie**
   - Wpisz coś w input
   - Naciśnij Enter lub kliknij Ask
   - Czekaj na odpowiedź ze źródłami

4. **Sprawdź źródła**
   - Każda odpowiedź ma źródła
   - Kliknij aby zobaczyć z którego dokumentu

---

## 🔍 Przydatne porty

| Port | Serwis | URL |
|------|--------|-----|
| 9000 | Backend API | http://localhost:9000 |
| 9000 | API Docs | http://localhost:9000/docs |
| 9001 | Frontend | http://localhost:9001 |

---

## 📚 Pełna dokumentacja

- **[SETUP.md](SETUP.md)** - Szczegółowa instrukcja + troubleshooting
- **[HOW_TO_USE.md](HOW_TO_USE.md)** - Praktyczne przykłady użycia
- **[README.md](README.md)** - Przegląd projektu
- **[HOW_IT_WORKS.md](HOW_IT_WORKS.md)** - Deep dive w architekturę

---

## 🆘 Problemy?

**Backend nie startuje?**
```
ModuleNotFoundError → pip install -r requirements.txt
Permission denied → chmod +x chainmain-venv/bin/activate
```

**Frontend nie łączy się z backendem?**
```
POST /api/upload failed → Sprawdź że backend działa na :9000
CORS error → Sprawdź FRONTEND_ORIGIN w .env
```

**Playwright test fail?**
```
Browser not found → npm run playwright:install
Connection refused → Upewnij się że oba serwery działają
```

Pełne rozwiązywanie problemów w [SETUP.md](SETUP.md) 👈

---

## 🎯 Następne kroki

- [ ] Uruchom backend (krok 1)
- [ ] Uruchom frontend (krok 2)
- [ ] Otwórz http://localhost:9001
- [ ] Uploaduj dokument
- [ ] Zadaj pytanie
- [ ] Uruchom testy Playwright
- [ ] Poczytaj [HOW_TO_USE.md](HOW_TO_USE.md)

---

## 💡 Pro tips

✨ **Keyboard shortcuts:**
- `Enter` = Wyślij pytanie
- `Shift+Enter` = Nowa linia
- `F12` = DevTools (zobacz błędy)

✨ **Development:**
- Backend ma `--reload` (hot reload na zmianę pliku)
- Frontend ma hot reload z Vite
- Tests mogą być uruchomione podczas developmentu

✨ **Production:**
- Zmień `FRONTEND_ORIGIN` w .env
- Zamiast `--reload` rób `uvicorn main:app --port 9000`
- Build frontend: `npm run build`

---

**Powodzenia!** 🚀 Jeśli coś nie działa, sprawdź [SETUP.md](SETUP.md) lub poczytaj błędy w terminalu/console.
