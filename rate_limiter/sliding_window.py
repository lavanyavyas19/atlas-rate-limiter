import time
from collections import defaultdict, deque
from .base import RateLimiter

class SlidingWindowRateLimiter(RateLimiter):
    """
    Sliding window rate limiter.

    For each key, keeps timestamps of recent requests and enforces
    a maximum of `limit` requests within the last `window_seconds`.
    """

    def __init__(self, limit: int, window_seconds: int):
        self.limit: int = limit
        self.window: int = window_seconds
        self.store: dict[str, deque[float]] = defaultdict(deque)

    def allow_request(self, key: str) -> bool:
        now = time.time()
        window_start = now - self.window
        timestamps = self.store[key]

        # Remove timestamps outside the window
        while timestamps and timestamps[0] < window_start:
            timestamps.popleft()

        if len(timestamps) >= self.limit:
            return False

        timestamps.append(now)
        return True
