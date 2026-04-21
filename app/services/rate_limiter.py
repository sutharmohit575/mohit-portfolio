"""
Lightweight in-memory rate limiter using a sliding window algorithm.
Thread-safe for single-process deployments.
For multi-worker deployments, swap the dict storage for Redis.
"""

import time
from collections import defaultdict
from threading import Lock


class RateLimiter:
    def __init__(self, max_requests: int, window_seconds: int) -> None:
        self.max_requests   = max_requests
        self.window_seconds = window_seconds
        self._store: dict[str, list[float]] = defaultdict(list)
        self._lock  = Lock()

    def allow(self, key: str) -> bool:
        """
        Return True if the request should be allowed, False if rate-limited.
        Evicts timestamps older than the window on each call.
        """
        now    = time.monotonic()
        cutoff = now - self.window_seconds

        with self._lock:
            # Remove stale timestamps
            self._store[key] = [t for t in self._store[key] if t > cutoff]

            if len(self._store[key]) >= self.max_requests:
                return False

            self._store[key].append(now)
            return True
