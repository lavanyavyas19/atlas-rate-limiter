from rate_limiter.fixed_window import FixedWindowRateLimiter
import time

def test_fixed_window_allows_within_limit():
    limiter = FixedWindowRateLimiter(limit=3, window_seconds=60)
    assert limiter.allow_request("u1")
    assert limiter.allow_request("u1")
    assert limiter.allow_request("u1")
    assert not limiter.allow_request("u1")

def test_fixed_window_resets_after_window():
    limiter = FixedWindowRateLimiter(limit=1, window_seconds=1)
    assert limiter.allow_request("u1")
    assert not limiter.allow_request("u1")
    time.sleep(1.1)
    assert limiter.allow_request("u1")
