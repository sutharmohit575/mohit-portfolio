"""
Static data for the portfolio.
All content lives here — update this file to change portfolio content
without touching routes or templates.
"""

from app.models.schemas import Project, SkillCategory, Skill

# ── Projects ──────────────────────────────────────────────────────────────────

PROJECTS: list[Project] = [
    Project(
        slug="neuralchat",
        name="⚡ NEURALCHAT",
        description="AI-powered real-time chat with multi-model support, custom memory, and plugin system. 2k+ active users.",
        tags=["React", "WebSocket", "OpenAI", "Redis"],
        biome="🏜 DESERT BIOME",
        demo_url="https://neuralchat.mohit.dev",
        status="Live — 2k+ users",
    ),
    Project(
        slug="pixelmart",
        name="🛒 PIXELMART",
        description="Full-stack e-commerce with real-time inventory, AI recommendations, and Stripe checkout.",
        tags=["Next.js", "Stripe", "PostgreSQL", "Vercel"],
        biome="🏜 DESERT BIOME",
        demo_url="https://pixelmart.mohit.dev",
        status="Live",
    ),
    Project(
        slug="jobai",
        name="🤖 JOBAI",
        description="AI-powered hiring platform with smart Resume Builder, Resume Analyzer & ATS scoring — helping job seekers stand out and recruiters hire faster.",
        tags=["Python", "Django", "HTML", "CSS", "JavaScript", "Railway"],
        biome="🔥 NETHER BIOME",
        demo_url="https://jobai-sutharmohit-575.up.railway.app",
        status="Live",
    ),
    Project(
        slug="autoscribe",
        name="🤖 AUTOSCRIBE",
        description="AI document intelligence — extract, summarize, and query any file. Used by 500+ businesses.",
        tags=["Python", "LangChain", "FastAPI", "Pinecone"],
        biome="🌌 END BIOME",
        demo_url="https://autoscribe.mohit.dev",
        status="Live — 500+ businesses",
    ),
]

# ── Skill tree ────────────────────────────────────────────────────────────────

SKILL_CATEGORIES: list[SkillCategory] = [
    SkillCategory(
        label="FRONTEND", icon="⚡", color="cyan",
        skills=[
            Skill(name="HTML5",            level=95),
            Skill(name="Canvas API",       level=80, parent="HTML5"),
            Skill(name="WebGL / Three.js", level=65, parent="Canvas API"),
            Skill(name="CSS3 + Tailwind",  level=90),
            Skill(name="Animations",       level=85, parent="CSS3 + Tailwind"),
            Skill(name="React / Next.js",  level=88),
        ],
    ),
    SkillCategory(
        label="BACKEND", icon="🔥", color="orange",
        skills=[
            Skill(name="Node.js",              level=85),
            Skill(name="Python + FastAPI",     level=82),
            Skill(name="AI / ML",              level=70, parent="Python + FastAPI"),
            Skill(name="PostgreSQL + MongoDB", level=78),
        ],
    ),
    SkillCategory(
        label="DEVOPS & TOOLS", icon="⚙", color="yellow",
        skills=[
            Skill(name="Docker + AWS", level=75),
            Skill(name="Git + CI/CD",  level=90),
        ],
    ),
]

# ── Achievements ──────────────────────────────────────────────────────────────

ACHIEVEMENTS: dict[str, dict] = {
    "curious":  {"label": "Curious Human",   "emoji": "👁",  "xp": 1,  "hint": "Stayed 30 seconds"},
    "hacker":   {"label": "Elite Hacker",    "emoji": "💻", "xp": 1,  "hint": "Typed 'help'"},
    "explorer": {"label": "Explorer",        "emoji": "🗺",  "xp": 3,  "hint": "Viewed all sections"},
    "gamer":    {"label": "True Gamer",      "emoji": "🎮", "xp": 2,  "hint": "Played Snake"},
    "hunter":   {"label": "Secret Hunter",   "emoji": "🥚", "xp": 5,  "hint": "sudo hire-me"},
    "boss":     {"label": "Boss Slayer",     "emoji": "⚔",  "xp": 5,  "hint": "Defeated the boss"},
    "matrix":   {"label": "Matrix Initiate", "emoji": "🟩", "xp": 2,  "hint": "Entered the Matrix"},
    "konami":   {"label": "Konami Master",   "emoji": "⬆",  "xp": 3,  "hint": "↑↑↓↓←→←→BA"},
    "neofetch": {"label": "Sysadmin",        "emoji": "🖥",  "xp": 2,  "hint": "Ran neofetch"},
    "shutdown": {"label": "Chaos Agent",     "emoji": "💀", "xp": 3,  "hint": "Ran shutdown"},
}

# ── Virtual filesystem (used by terminal 'ls', 'cd', 'cat') ──────────────────

VIRTUAL_FS: dict[str, dict] = {
    "~": {"type": "dir", "children": ["projects", "skills", "about", "resume.txt"]},
    "~/projects": {"type": "dir", "children": ["neuralchat", "pixelmart", "jobai", "autoscribe"]},
    "~/projects/neuralchat":  {"type": "file", "content": ["NAME:    NeuralChat", "STACK:   React, WebSocket, OpenAI, Redis", "STATUS:  ● Live — 2k+ users", "DEMO:    neuralchat.mohit.dev"]},
    "~/projects/pixelmart":   {"type": "file", "content": ["NAME:    PixelMart", "STACK:   Next.js, Stripe, PostgreSQL, Vercel", "STATUS:  ● Live", "DEMO:    pixelmart.mohit.dev"]},
    "~/projects/jobai":       {"type": "file", "content": ["NAME:    JobAI", "STACK:   Python, Django, HTML, CSS, JavaScript, Railway", "STATUS:  ● Live", "DEMO:    jobai-sutharmohit-575.up.railway.app", "REPO:    github.com/sutharmohit575/jobai", "DESC:    AI-powered hiring platform — Resume Builder & Analyzer"]},
    "~/projects/autoscribe":  {"type": "file", "content": ["NAME:    AutoScribe", "STACK:   Python, LangChain, FastAPI, Pinecone", "STATUS:  ● Live — 500+ biz", "DEMO:    autoscribe.mohit.dev"]},
    "~/skills": {"type": "dir", "children": ["frontend", "backend", "devops"]},
    "~/skills/frontend": {"type": "file", "content": ["HTML5: 95%", "CSS3+Tailwind: 90%", "React/Next.js: 88%", "Canvas API: 80%", "WebGL/Three.js: 65%"]},
    "~/skills/backend":  {"type": "file", "content": ["Node.js: 85%", "Python+FastAPI: 82%", "PostgreSQL+MongoDB: 78%", "AI/ML: 70%"]},
    "~/skills/devops":   {"type": "file", "content": ["Git+CI/CD: 90%", "Docker+AWS: 75%"]},
    "~/about": {"type": "dir", "children": ["bio.txt", "links.txt"]},
    "~/about/bio.txt": {"type": "file", "content": [
        "Name:     Mohit Suthar",
        "Role:     Full Stack Dev · AI Enthusiast",
        "Location: 🇮🇳 India (IST UTC+5:30)",
        "Level:    42 🔥",
        "Projects: 24+ shipped",
        "Bugs:     9,999+ squashed",
    ]},
    "~/about/links.txt": {"type": "file", "content": [
        "GitHub:   https://github.com/sutharmohit575",
        "LinkedIn: https://linkedin.com/in/suthar-mohit575",
        "Email:    mohit@dev.io",
    ]},
    "~/resume.txt": {"type": "file", "content": [
        "Run 'sudo hire-me' to unlock the resume.",
    ]},
}

# ── Terminal boot lines ───────────────────────────────────────────────────────

BOOT_LINES: list[dict] = [
    {"text": "Initializing PORTFOLIO_OS v2.0...",       "cls": "",     "delay_ms": 150},
    {"text": "Loading kernel modules...",               "cls": "ok",   "delay_ms": 300},
    {"text": "Mounting /dev/mohit...",                  "cls": "ok",   "delay_ms": 450},
    {"text": "Scanning for threats...",                 "cls": "fail", "delay_ms": 600},
    {"text": "Importing 9999 npm packages...",          "cls": "ok",   "delay_ms": 750},
    {"text": "Detecting gamer profile... CONFIRMED",    "cls": "ok",   "delay_ms": 900},
    {"text": "Loading easter eggs...",                  "cls": "ok",   "delay_ms": 1050},
    {"text": "Starting achievement system...",          "cls": "ok",   "delay_ms": 1200},
    {"text": "Mounting filesystem /projects /skills...", "cls": "ok",  "delay_ms": 1350},
    {"text": "XP tracker online...",                    "cls": "ok",   "delay_ms": 1500},
    {"text": "Spawning boss...",                        "cls": "warn", "delay_ms": 1650},
    {"text": "System ready. Welcome, traveler.",        "cls": "",     "delay_ms": 1800},
]
