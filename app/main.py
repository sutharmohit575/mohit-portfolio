"""
MOHIT.EXE — Portfolio OS v2.0
FastAPI backend powering the interactive developer portfolio.
"""

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from app.routers import contact, achievements, projects
from app.core.config import settings

app = FastAPI(
    title="MOHIT.EXE — Portfolio OS",
    description="Interactive developer portfolio with terminal, RPG skill tree, boss fight, and Snake.EXE",
    version="3.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
)

# ── Middleware ────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Static files & templates ──────────────────────────────
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# ── API routers ───────────────────────────────────────────
app.include_router(contact.router,      prefix="/api/contact",      tags=["Contact"])
app.include_router(achievements.router, prefix="/api/achievements",  tags=["Achievements"])
app.include_router(projects.router,     prefix="/api/projects",      tags=["Projects"])


# ── Root — serve the portfolio SPA ───────────────────────
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


# ── Health check ──────────────────────────────────────────
@app.get("/api/health", tags=["System"])
async def health():
    return {"status": "online", "version": "3.0.0", "system": "PORTFOLIO_OS"}
