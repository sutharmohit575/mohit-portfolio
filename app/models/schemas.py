"""
Pydantic models used across the application.
"""

from __future__ import annotations
from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime, timezone
from enum import Enum


# ── Contact / Boss Fight ──────────────────────────────────────────────────────

class ContactReason(str, Enum):
    freelance = "Freelance Project"
    fulltime  = "Full-time Role"
    collab    = "Collab / Open Source"
    exploring = "Just Exploring"


class ContactSubmission(BaseModel):
    name:               str          = Field(..., min_length=2, max_length=80)
    email:              EmailStr
    reason:             ContactReason
    interested_project: Optional[str] = Field(None, max_length=50)

    model_config = {"str_strip_whitespace": True}


class ContactResponse(BaseModel):
    success:      bool
    message:      str
    loot_dropped: bool = False


# ── Projects ──────────────────────────────────────────────────────────────────

class Project(BaseModel):
    slug:        str
    name:        str
    description: str
    tags:        List[str]
    biome:       str
    demo_url:    Optional[str] = None
    repo_url:    Optional[str] = None
    status:      str = "Live"


class ProjectList(BaseModel):
    projects: List[Project]


# ── Achievements ──────────────────────────────────────────────────────────────

class AchievementID(str, Enum):
    curious  = "curious"
    hacker   = "hacker"
    explorer = "explorer"
    gamer    = "gamer"
    hunter   = "hunter"
    boss     = "boss"
    matrix   = "matrix"
    konami   = "konami"
    neofetch = "neofetch"
    shutdown = "shutdown"


class UnlockRequest(BaseModel):
    achievement_id: AchievementID
    session_id:     str = Field(..., min_length=4, max_length=64)


class AchievementUnlocked(BaseModel):
    achievement_id: str
    label:          str
    emoji:          str
    xp_reward:      int
    unlocked_at:    datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


# ── Skill tree ────────────────────────────────────────────────────────────────

class Skill(BaseModel):
    name:   str
    level:  int            # 0–100
    parent: Optional[str] = None


class SkillCategory(BaseModel):
    label:  str
    icon:   str
    color:  str
    skills: List[Skill]
