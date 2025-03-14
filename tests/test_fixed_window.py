import time
from rate_limiter.fixed_window import FixedWindowRateLimiter

def test_fixed_window_allows_within_limit():
    limiter = FixedWindowRateLimiter(limit=3, window_seconds=60)
    key = "user1"

    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    assert not limiter.allow_request(key)  # 4th should be blocked

def test_fixed_window_resets_after_window():
    limiter = FixedWindowRateLimiter(limit=1, window_seconds=1)
    key = "user2"

    assert limiter.allow_request(key)
    assert not limiter.allow_request(key)

    time.sleep(1.1)

    assert limiter.allow_request(key)
