"""
Email service — sends contact form submissions via SMTP.
Falls back to console logging when SMTP credentials are not configured.
This means in development you don't need to set up email at all —
the message will just print to the terminal.
"""

import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from app.models.schemas import ContactSubmission
from app.core.config import settings

logger = logging.getLogger(__name__)


async def send_contact_email(submission: ContactSubmission) -> None:
    """
    Send an email notification for a new contact submission.
    If SMTP is not configured, logs to stdout instead (dev mode).
    """
    subject = f"[Portfolio] New message from {submission.name} — {submission.reason.value}"
    body = _build_body(submission)

    # ── Dev mode: no SMTP configured → just log it ────────────────
    if not settings.smtp_host:
        logger.info("📬 [DEV — no SMTP configured]\n%s", body)
        print(f"\n{'='*50}\n📬 CONTACT FORM SUBMISSION\n{'='*50}\n{body}\n{'='*50}\n")
        return

    # ── Production: send via SMTP ─────────────────────────────────
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"]    = settings.smtp_user
    msg["To"]      = settings.contact_email
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(settings.smtp_user, settings.smtp_password)
            server.sendmail(settings.smtp_user, settings.contact_email, msg.as_string())
        logger.info("✅ Contact email sent for %s", submission.email)
    except smtplib.SMTPException as exc:
        logger.error("❌ Failed to send contact email: %s", exc)
        raise


def _build_body(s: ContactSubmission) -> str:
    return (
        f"New contact form submission\n"
        f"{'─' * 40}\n"
        f"Name:     {s.name}\n"
        f"Email:    {s.email}\n"
        f"Reason:   {s.reason.value}\n"
        f"Project:  {s.interested_project or 'N/A'}\n"
    )
