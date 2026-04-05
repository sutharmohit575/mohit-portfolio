"""
Achievements API router.
GET  /api/achievements/         — list all achievement definitions
POST /api/achievements/unlock   — record an unlock (server-side log)
"""

from fastapi import APIRouter, HTTPException
from datetime import datetime, timezone
from app.models.schemas import UnlockRequest, AchievementUnlocked
from app.data.portfolio_data import ACHIEVEMENTS

router = APIRouter()


@router.get("/")
async def list_achievements():
    """Return all achievement metadata so the frontend can render the badge grid."""
    return {"achievements": ACHIEVEMENTS}


@router.post("/unlock", response_model=AchievementUnlocked)
async def unlock_achievement(payload: UnlockRequest):
    """
    Called by the frontend when a visitor unlocks an achievement.
    Returns enriched achievement data (XP reward, label, emoji).
    In production you'd persist this to a DB / analytics pipeline.
    """
    meta = ACHIEVEMENTS.get(payload.achievement_id.value)
    if not meta:
        raise HTTPException(status_code=404, detail="Unknown achievement")

    return AchievementUnlocked(
        achievement_id=payload.achievement_id.value,
        label=meta["label"],
        emoji=meta["emoji"],
        xp_reward=meta["xp"],
        unlocked_at=datetime.now(timezone.utc),
    )
