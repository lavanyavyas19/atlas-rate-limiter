import time
from tests.test_sliding_window import SlidingWindowRateLimiter


def _make_limiter(limit: int, window_seconds: int) -> SlidingWindowRateLimiter:
    """Factory helper used across sliding window tests."""
    return SlidingWindowRateLimiter(limit=limit, window_seconds=window_seconds)


def test_sliding_window_allows_within_limit():
    limiter = _make_limiter(limit=3, window_seconds=2)
    key = "client1"

    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    assert not limiter.allow_request(key)  # 4th call should be blocked

def test_sliding_window_is_isolated_per_key():
    limiter = _make_limiter(limit=2, window_seconds=2)

    assert limiter.allow_request("client_a")
    assert limiter.allow_request("client_a")
    assert not limiter.allow_request("client_a")

    # Other key should still be allowed independently
    assert limiter.allow_request("client_b")
    assert limiter.allow_request("client_b")
    assert not limiter.allow_request("client_b")


def test_sliding_window_recovers_after_window():
    limiter = _make_limiter(limit=2, window_seconds=1)
    key = "client2"

    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    assert not limiter.allow_request(key)

    time.sleep(1.1)

    assert limiter.allow_request(key)
