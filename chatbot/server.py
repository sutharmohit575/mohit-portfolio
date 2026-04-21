"""
MOHIT.EXE — Chatbot API Server  (DSA Edition)
FastAPI wrapper around the chatbot engine.

IMPORTANT — How to run correctly:
    cd mohit_portfolio/chatbot
    uvicorn server:app --reload --port 8001

Endpoints:
    POST /chat     — send a message, get a response
    GET  /health   — uptime check
    GET  /stats    — DSA engine statistics
    GET  /docs     — Swagger UI (test in browser)
"""

import time
import os
from collections import defaultdict

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from pydantic import BaseModel, Field

from chatbot_engine import ChatbotEngine

# ── App init ──────────────────────────────────────────────────────
app = FastAPI(
    title="Mohit.exe Chatbot API",
    description="DSA-powered chatbot — Trie · LRU Cache · Min-Heap · BFS Graph",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # restrict to your domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

engine     = ChatbotEngine()
START_TIME = time.time()

# In-memory rate limiter (HashMap + sliding window)
_rate_map: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT  = 30   # requests
RATE_WINDOW = 60   # seconds


# ── Schemas ───────────────────────────────────────────────────────
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500,
                         example="Tell me about Mohit's skills")


class ChatResponse(BaseModel):
    intent:       str
    text:         str
    suggestions:  list[str]
    next_topics:  list[str]
    from_cache:   bool
    query_number: int
    dsa_trace:    dict


# ── Rate limiting middleware ──────────────────────────────────────
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    if request.url.path == "/chat" and request.method == "POST":
        ip  = request.client.host if request.client else "unknown"
        now = time.time()
        _rate_map[ip] = [t for t in _rate_map[ip] if now - t < RATE_WINDOW]
        if len(_rate_map[ip]) >= RATE_LIMIT:
            return JSONResponse(
                status_code=429,
                content={"error": f"Rate limit: max {RATE_LIMIT} requests per {RATE_WINDOW}s."}
            )
        _rate_map[ip].append(now)
    return await call_next(request)


# ── Routes ────────────────────────────────────────────────────────
@app.get("/", include_in_schema=False)
async def root():
    """Redirect root to Swagger docs so visiting / doesn't give 404."""
    return RedirectResponse(url="/docs")


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Send a message to Mohit.exe chatbot.
    Pipeline: Trie → FuzzyScorer (Min-Heap) → BFS Graph → LRU Cache
    """
    result = engine.respond(req.message)
    return result


@app.get("/health")
async def health():
    """Quick health check — open this in browser to verify server is running."""
    return {
        "status":  "online",
        "uptime":  round(time.time() - START_TIME, 2),
        "version": "2.0.0",
    }


@app.get("/stats")
async def stats():
    """DSA engine runtime statistics."""
    s = engine.stats()
    s["uptime_seconds"]    = round(time.time() - START_TIME, 2)
    s["lru_cache_capacity"] = engine.cache.cap
    return s


# ── Dev runner ────────────────────────────────────────────────────
if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8001))
    print(f"\n🤖 Mohit.exe Chatbot API starting...")
    print(f"   → http://localhost:{port}/health  (check it's working)")
    print(f"   → http://localhost:{port}/docs    (test in browser)\n")
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=True)
