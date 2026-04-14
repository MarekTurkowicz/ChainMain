# Jak korzystać z ChainMain

Praktyczny przewodnik do aplikacji RAG.

---

## 📖 Co to jest ChainMain?

**ChainMain** to chatbot do dokumentów. Możesz:

1. **Uploadować dokumenty** (PDF lub TXT)
2. **Pytać o ich zawartość** w naturalnym języku
3. **Dostawać odpowiedzi z cytatami** ze źródeł
4. **Widzieć skąd** wziął się fragment

Wykorzystuje **RAG** (Retrieval-Augmented Generation):
- Dokumenty dzielą się na fragmenty
- Fragmenty zamieniają się na wektory (liczby)
- Gdy pytasz, system szuka podobnych fragmentów
- AI czyta te fragmenty i generuje odpowiedź

---

## 🎯 Szybki przykład

### Scenariusz: Masz artykuł o Machine Learning

**Krok 1: Upload dokumentu**
- Przeciągnij `artykul-ml.pdf` na upload area
- Zobaczysz: `artykul-ml.pdf (10 stron, 45 fragmentów)`

**Krok 2: Zadaj pytanie**
- Wpisz: "Jakie są główne typy machine learning?"
- Naciśnij Enter lub kliknij Ask

**Krok 3: Dostajesz odpowiedź ze źródłami**
```
Asystent:
Główne typy machine learning to:

1. Supervised Learning - nauka z oznaczonych przykładów
2. Unsupervised Learning - znajdowanie wzorów bez oznaczeń
3. Reinforcement Learning - nauka poprzez interakcję

Źródła:
📄 artykul-ml.pdf (strony 2-3)
```

---

## 📁 Uploadowanie dokumentów

### Jak uploadować

**Opcja 1: Kliknij i przeglądaj**
1. Kliknij na pole uploadowania
2. Wybierz plik z komputera
3. Kliknij Otwórz

**Opcja 2: Drag & Drop**
1. Znajdź PDF lub TXT na komputerze
2. Przeciągnij na upload area
3. Pole się podświetli
4. Upload start automatycznie

**Opcja 3: Wiele plików**
- Zaznacz kilka plików naraz
- Lub przeciągnij kilka na raz
- Wszystkie uploadują się

### Wspierane formaty

| Format | Wsparcie | Notatka |
|--------|----------|---------|
| **PDF** | ✅ | Tylko tekstowe PDF-y |
| **TXT** | ✅ | Zwykłe tekstowe |
| **DOCX** | ❌ | Konwertuj do PDF |
| **Obrazy** | ❌ | Brak OCR |

### Feedback uploadowania

- **Sukces**: Plik pojawi się na liście
- **Błąd**: Czerwona wiadomość z problemem
- **Status**: Pasek postępu podczas uploadowania

---

## 💬 Zadawanie pytań

### Podstawowy Q&A

**Wpisz pytanie:**
```
"Co dokument mówi o..."
"Wyjaśnij proces..."
"Wymień główne tematy"
"Porównaj X i Y"
```

**Wyślij:**
- Naciśnij `Enter` (lub `Shift+Enter` do nowej linii)
- Lub kliknij przycisk `Ask`

**Odpowiedź:**
- Pojawia się w czasie rzeczywistym (streaming)
- Źródła pokazane na dole
- Możesz pytać dalej

### Porady do pytań

**Dobre pytania:**
```
✅ "Jakie są korzyści machine learning?"
✅ "Jak działa algorytm?"
✅ "Jakie dane są potrzebne?"
✅ "Kiedy to zostało napisane?"
```

**Unikaj:**
```
❌ "Powiedz mi wszystko" (za szerokie)
❌ Pojedyncze słowa
❌ Pytania poza dokumentem
```

### Filtrowanie dokumentów

**Aby szukać w konkretnych dokumentach:**

1. **Zaznacz checkboxy** obok dokumentów
2. Będą przeszukiwane **tylko zaznaczone** dokumenty
3. Kliknij **"Clear"** aby odznączyć wszystko
4. Zostaw wszystko odznaczone aby szukać wszędzie

**Przykład:**
- Upload: `sprzedaż-2023.pdf` i `sprzedaż-2024.pdf`
- Zaznacz tylko `sprzedaż-2024.pdf`
- Pytaj: "Jaki był przychód?"
- Dostajesz tylko dane z 2024

---

## 📚 Zarządzanie dokumentami

### Widok dokumentów

**Sidebar pokazuje:**
- Nazwa pliku
- Liczba stron
- Liczba fragmentów
- Checkbox do zaznaczenia
- Przycisk do usunięcia

**Przykład:**
```
📄 research-paper.pdf
   Strony: 12
   Fragmenty: 48
   [✓] Zaznacz  [🗑] Usuń
```

### Usuwanie dokumentów

1. Znajdź dokument w sidebarze
2. Kliknij przycisk Delete (kosz)
3. Potwierdź jeśli trzeba
4. Dokument usunięty z wyszukiwania

### Statystyki dokumentów

- **Strony**: Przybliżona liczba stron
- **Fragmenty**: Liczba kawałków tekstu
- Fragment = ~1000 znaków z nakładaniem

---

## 🔍 Rozumienie odpowiedzi

### Struktura odpowiedzi

```
┌─────────────────────────────────┐
│ Twoje pytanie:                  │
│ "Co to jest vector search?"     │
└─────────────────────────────────┘

┌─────────────────────────────────┐
│ Odpowiedź asystenta:            │
│ "Vector search to technika...   │
│  Działa poprzez konwersję..."   │
│                                 │
│ Źródła:                         │
│ 📄 Document.pdf (Strona 5)     │
│ 📄 Document.pdf (Strona 7)     │
└─────────────────────────────────┘
```

### Co oznaczają źródła

**Źródła pokazują:**
- **Nazwa dokumentu**: Z którego pliku pochodzi info
- **Strona**: Która przybliżona strona
- **Fragment**: Który kawałek tekstu był użyty

**Dlaczego źródła są ważne:**
- Możesz zweryfikować odpowiedź
- Możesz przeczytać pełny kontekst
- Wiesz gdzie szukać więcej infon

### Zaufanie do odpowiedzi

**Wyższa pewność gdy:**
- Pytanie dokładnie odpowiada zawartości
- Wiele źródeł mówi to samo
- Info jest jasno napisane

**Niższa pewność gdy:**
- Pytanie wymaga wniosków
- Dokument ma sprzeczne info
- Specjalistyczna terminologia

---

## ⌨️ Skróty klawiszowe

| Skrót | Akcja |
|-------|-------|
| `Enter` | Wyślij pytanie |
| `Shift+Enter` | Nowa linia |
| `Tab` | Następny element |
| `Esc` | Zamknij błędy |

---

## ⚙️ Jak to działa pod spodem

```
Wpisujesz pytanie
        ↓
   [Model embeddingów]
   Zamienia na wektor
        ↓
   [Wyszukiwanie wektorowe]
   Znajduje podobne fragmenty
        ↓
   [Pobrane fragmenty]
   Zwykle 4 fragmenty
        ↓
   [LLM (GPT-4)]
   Czyta fragmenty + pytanie
        ↓
   [Generowanie odpowiedzi]
   Streaming odpowiedzi
        ↓
   Widzisz odpowiedź
```

### Konfiguracja

System wykorzystuje:
- **Embedding**: `text-embedding-3-small` (OpenAI)
- **LLM**: `gpt-4o-mini` (szybki i tani)
- **Baza wektorów**: Chroma (lokalna, szybka)
- **Rozmiar fragmentu**: 1000 znaków
- **Top K**: 4 najrelewantniejsze fragmenty

### Dlaczego działa

1. **Embeddingi** zamieniają tekst na liczby
2. **Wyszukiwanie wektorowe** znajduje relevantne fragmenty
3. **LLM** rozumie kontekst i może wnioskować
4. **Kombinacja** = dokładne, ugruntowane odpowiedzi

---

## 🚀 Zaawansowane zastosowania

### Scenariusz 1: Analiza artykułu naukowego

1. Upload: `paper.pdf`
2. Pytania:
   ```
   "Jakie jest główne pytanie badawcze?"
   "Jaką metodologię wykorzystali?"
   "Jakie są najważniejsze ustalenia?"
   "Jak to się ma do wcześniejszych prac?"
   "Jakie są ograniczenia?"
   ```
3. Dostajesz ustrukturyzowaną wiedzę

### Scenariusz 2: Przegląd umowy

1. Upload: `umowa.pdf`
2. Pytania:
   ```
   "Jakie są warunki płatności?"
   "Co się dzieje jeśli naruszę umowę?"
   "Jaka jest klauzula zakończenia?"
   "Czy są gwarancje?"
   ```
3. Kluczowe warunki ze źródłami

### Scenariusz 3: Baza wiedzy dla zespołu

1. Upload: Wiele dokumentów (zasady, przewodniki)
2. Zaznaczaj specific doc jeśli trzeba
3. Pytania:
   ```
   "Jaka jest nasza polityka urlopów?"
   "Jak zgłaszam wydatek?"
   "Kto jest kontaktem HR?"
   ```
4. Pracownicy dostaną instant, dokładne odpowiedzi

### Scenariusz 4: Porównanie dokumentów

1. Upload: `raport-2023.pdf`, `raport-2024.pdf`
2. Zaznacz oba (nie filtruj)
3. Pytania:
   ```
   "Jak zmienił się przychód?"
   "Które segmenty rosły?"
   "Jakie nowe produkty?"
   ```
4. Porównawcza analiza ze źródłami z obu lat

---

## ⚠️ Częste problemy

### "Nie widzę mojego pytania w chacie"

**Problem**: Pytanie wysłane ale nic się nie pojawia  
**Rozwiązanie**:
- Sprawdź internet
- Czekaj moment (streaming jest wolny na pierwszym tokenie)
- Sprawdź console w przeglądarce (F12)

### "Odpowiedź wydaje się zła"

**Problem**: AI dała off-topic odpowiedź  
**Rozwiązanie**:
- Przeformułuj pytanie bardziej jasno
- Pytaj o konkretne części dokumentu
- Sprawdź czy dokument zawiera info
- Podziel na mniejsze pytania

### "Dostaję tę samą odpowiedź za każde pytanie"

**Problem**: System wydaje się cachować  
**Rozwiązanie**:
- Przeładuj stronę (Ctrl+R)
- Wyczyść cache przeglądarki
- Pytaj wyraźnie inne pytanie

### "Uploadowanie zawsze się nie powiedzie"

**Problem**: Pliki nie uploadują  
**Rozwiązanie**:
- Sprawdzić rozmiar (<50MB)
- Upewnij się że to PDF lub TXT
- Spróbuj inny plik
- Sprawdź że backend działa
- Sprawdź network tab (F12)

### "Backend nie odpowiada"

**Problem**: Nie mogę się połączyć z API  
**Rozwiązanie**:
- Uruchom backend: `uvicorn main:app --reload --port 9000`
- Sprawdź http://localhost:9000
- Sprawdź firewall port 9000
- Sprawdź FRONTEND_ORIGIN w .env

---

## 📊 Porady do wydajności

### Dla lepszych wyników

1. **Jasne, konkretne pytania** → Lepsze odpowiedzi
2. **Mniejsze dokumenty** → Szybsze odpowiedzi
3. **Zaznaczaj dokumenty** → Bardziej targeted
4. **Wiele uploadów** → Używaj filtrów

### Dla szybszych odpowiedzi

1. Mniej fragmentów = szybsze szukanie
2. Filtruj dokumenty
3. Konkretne pytania (mniej tokenów)
4. Sprawdź limit API

---

## 🔐 Dane i prywatność

### Co się dzieje z danymi?

1. **Dokumenty**: Przechowywane lokalnie w `backend/data/`
2. **Embeddingi**: W lokalnej bazie Chroma
3. **Czat**: W pamięci przeglądarki (nie trwały)
4. **API**: Wysyłane do OpenAI (embeddingi i LLM)

### Tym zarządzasz

- Usuwaj dokumenty kiedy chcesz
- Dane zostają na Twojej maszynie
- Zarządzasz kluczami API w .env
- Backend można self-hostować

---

## 💡 Best practices

✅ **RÓB:**
- Jedno pytanie na raz
- Sprawdzaj źródła
- Używaj filtrów
- Usuwaj stare dokumenty
- Organizuj dokumenty

❌ **NIE RÓB:**
- Uploaduj mega-pliki (>50MB)
- Nie ufaj bez weryfikacji
- Nie polegaj na jednym źródle
- Nie uploaduj wrażliwych danych
- Nie ignoruj źródeł

---

## 📚 Powiązana dokumentacja

- [SETUP.md](SETUP.md) - Instalacja i setup
- [README.md](README.md) - Przegląd projektu
- [HOW_IT_WORKS.md](HOW_IT_WORKS.md) - Deep dive w architekturę

---

Powodzenia z ChainMain! 🚀
