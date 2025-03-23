# rate_limiter/token_bucket.py

import time
from collections import defaultdict
from .base import RateLimiter


class TokenBucketRateLimiter(RateLimiter):
    """
    Token bucket rate limiter.

    Each key has a bucket with:
      - capacity: maximum tokens it can hold
      - refill_rate: tokens added per second

    A request consumes 1 token. If no tokens are available, the
    request is rejected.
    """

    def __init__(self, capacity: int, refill_rate_per_second: float):
        self.capacity = capacity
        self.refill_rate = refill_rate_per_second
        # key -> {"tokens": float, "last_refill": float}
        self.store = defaultdict(
            lambda: {"tokens": float(capacity), "last_refill": time.time()}
        )

    def _refill(self, key: str) -> None:
        now = time.time()
        data = self.store[key]
        elapsed = now - data["last_refill"]
        if elapsed <= 0:
            return

        # Add tokens based on elapsed time
        added = elapsed * self.refill_rate
        data["tokens"] = min(self.capacity, data["tokens"] + added)
        data["last_refill"] = now

    def allow_request(self, key: str) -> bool:
        self._refill(key)
        data = self.store[key]

        if data["tokens"] < 1:
            return False

        data["tokens"] -= 1
        return True
