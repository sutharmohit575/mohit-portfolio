"""
App-wide configuration loaded from environment variables / .env file.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # ── App ──────────────────────────────────────────────
    app_name:   str  = "MOHIT.EXE Portfolio OS"
    debug:      bool = False
    secret_key: str  = "change-me-in-production"

    # ── CORS ─────────────────────────────────────────────
    allowed_origins: List[str] = ["*"]

    # ── Email (optional — for contact boss form) ─────────
    smtp_host:     str = "smtp.gmail.com"
    smtp_port:     int = 587
    smtp_user:     str = "sutharmohit575@gmail.com"
    smtp_password: str = "anhs dsek nmcz Itat"
    contact_email: str = "sutharmohit575@gmail.com"

    # ── Rate limiting ─────────────────────────────────────
    contact_rate_limit: int = 5   # max submissions per hour per IP

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
