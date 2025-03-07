import time
from collections import defaultdict, deque
from .base import RateLimiter

class SlidingWindowRateLimiter(RateLimiter):
    """
    Sliding window rate limiter.

    Allows up to `limit` requests within the last `window_seconds`
    for each key. Uses a deque of timestamps per key.
    """

    def __init__(self, limit: int, window_seconds: int):
        self.limit = limit
        self.window = window_seconds
        self.store = defaultdict(deque)  # key -> deque[timestamps]

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
