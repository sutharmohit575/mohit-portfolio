"""
Contact / Boss Fight API router.
POST /api/contact/submit  — processes the boss fight form
"""

from contextlib import suppress

from fastapi import APIRouter, HTTPException, Request

from app.models.schemas import ContactResponse, ContactSubmission
from app.services.email_service import send_contact_email
from app.services.rate_limiter import RateLimiter

router = APIRouter()
_limiter = RateLimiter(max_requests=5, window_seconds=3600)


@router.post("/submit", response_model=ContactResponse)
async def submit_contact(payload: ContactSubmission, request: Request):
    """
    Process the Boss Fight contact form.
    Returns loot_dropped=True on success so the frontend can reveal links.
    """
    client_ip = request.client.host if request.client else "unknown"

    if not _limiter.allow(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Too many contact attempts. Try again later."
        )

    with suppress(Exception):
        await send_contact_email(payload)

    return ContactResponse(
        success=True,
        message="Message transmitted. Mohit will respawn shortly.",
        loot_dropped=True,
    )
