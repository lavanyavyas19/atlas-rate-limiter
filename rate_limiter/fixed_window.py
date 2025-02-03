import time
from collections import defaultdict
from .base import RateLimiter

class FixedWindowRateLimiter(RateLimiter):
    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.store = defaultdict(lambda: {"count": 0, "window_start": time.time()})

    def allow_request(self, key: str) -> bool:
        now = time.time()
        data = self.store[key]

        if now - data["window_start"] > self.window:
            data["window_start"] = now
            data["count"] = 0

        data["count"] += 1
        return data["count"] <= self.limit
