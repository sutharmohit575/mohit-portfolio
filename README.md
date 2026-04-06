# 🖥 MOHIT.EXE — Portfolio OS v2.0

> The most unhinged developer portfolio you'll ever visit.
> Terminal · RPG Skill Tree · Boss Fight · Snake.EXE · AI Chatbot · Easter Eggs
```
🌐 **Live Demo:**
👉 **https://mohit-portfolio-zmdr.onrender.com**
```

---

## 📁 Project Structure

```
mohit_portfolio/
├── app/                        ← Main FastAPI application
│   ├── core/
│   │   └── config.py           ← Settings loaded from .env
│   ├── data/
│   │   └── portfolio_data.py   ← All content (projects, skills, achievements)
│   ├── models/
│   │   └── schemas.py          ← Pydantic models
│   ├── routers/
│   │   ├── contact.py          ← POST /api/contact/submit
│   │   ├── projects.py         ← GET  /api/projects/
│   │   └── achievements.py     ← GET/POST /api/achievements/
│   ├── services/
│   │   ├── email_service.py    ← SMTP email sender
│   │   └── rate_limiter.py     ← In-memory rate limiter
│   ├── static/
│   │   ├── css/                ← (place custom CSS here)
│   │   └── js/                 ← (place custom JS here)
│   ├── templates/
│   │   └── index.html          ← The full portfolio SPA
│   └── main.py                 ← FastAPI app entry point
│
├── chatbot/                    ← DSA-powered AI chatbot (separate server)
│   ├── chatbot_engine.py       ← Trie, LRU, Min-Heap, BFS engine
│   ├── server.py               ← FastAPI chatbot API (port 8001)
│   ├── chatbot_widget.html     ← Drop-in widget for index.html
│   ├── test_chatbot.py         ← 26 unit tests
│   ├── requirements.txt        ← Chatbot-specific deps (same as root)
│   └── README.md               ← Chatbot documentation
│
├── tests/                      ← Portfolio backend tests
│   ├── test_contact.py
│   ├── test_projects.py
│   ├── test_achievements.py
│   └── test_rate_limiter.py
│
├── .env                        ← Your secrets (NOT in git)
├── .env.example                ← Template — copy to .env and fill in
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run

### 1. Setup

```bash
# Clone / unzip the project
cd mohit_portfolio

# Create virtual environment
python -m venv .venv

# Activate it
# Windows:
.venv\Scripts\activate
# Mac/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env with your real values (SECRET_KEY, SMTP settings)
```

### 3. Run the portfolio

```bash
uvicorn app.main:app --reload --port 8000
```

Open: **http://localhost:8000**
API docs: **http://localhost:8000/api/docs**

### 4. Run the chatbot (separate terminal)

```bash
cd chatbot
uvicorn server:app --reload --port 8001
```

Test it: **http://localhost:8001/health**
Chat API: **POST http://localhost:8001/chat**
Chat docs: **http://localhost:8001/docs**

### 5. Run tests

```bash
# From the project root (mohit_portfolio/)
pytest tests/ -v
```

---

## 🔌 API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/` | Portfolio SPA |
| GET | `/api/health` | Health check |
| GET | `/api/docs` | Swagger UI |
| POST | `/api/contact/submit` | Boss fight form |
| GET | `/api/projects/` | List all projects |
| GET | `/api/projects/{slug}` | Single project |
| GET | `/api/achievements/` | List achievements |
| POST | `/api/achievements/unlock` | Record unlock |
| POST | `/chat` (port 8001) | Chatbot message |
| GET | `/health` (port 8001) | Chatbot health |

---

## 🚀 Deploy (Production)

**Render / Railway / any VPS:**

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Set these environment variables in your hosting dashboard:
- `SECRET_KEY` — a long random string
- `SMTP_HOST`, `SMTP_USER`, `SMTP_PASSWORD`, `CONTACT_EMAIL`
- `ALLOWED_ORIGINS` — your domain, e.g. `["https://mohit.dev"]`
