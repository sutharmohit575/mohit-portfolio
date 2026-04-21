"""
Unit tests for the in-memory rate limiter.
Run: pytest tests/ -v
"""

import time
from app.services.rate_limiter import RateLimiter


def test_allows_requests_under_limit():
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    assert limiter.allow("ip1") is True
    assert limiter.allow("ip1") is True
    assert limiter.allow("ip1") is True


def test_blocks_when_limit_exceeded():
    limiter = RateLimiter(max_requests=3, window_seconds=60)
    limiter.allow("ip2")
    limiter.allow("ip2")
    limiter.allow("ip2")
    assert limiter.allow("ip2") is False


def test_different_keys_are_independent():
    limiter = RateLimiter(max_requests=1, window_seconds=60)
    assert limiter.allow("ip_a") is True
    assert limiter.allow("ip_b") is True   # different key — not affected


def test_window_expiry():
    limiter = RateLimiter(max_requests=1, window_seconds=1)
    assert limiter.allow("ip3") is True
    assert limiter.allow("ip3") is False   # blocked within window
    time.sleep(1.1)
    assert limiter.allow("ip3") is True    # window expired — allowed again


def test_exact_limit_boundary():
    limiter = RateLimiter(max_requests=2, window_seconds=60)
    assert limiter.allow("ip4") is True   # 1st — allowed
    assert limiter.allow("ip4") is True   # 2nd — allowed
    assert limiter.allow("ip4") is False  # 3rd — blocked
