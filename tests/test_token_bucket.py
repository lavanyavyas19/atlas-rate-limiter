# tests/test_token_bucket.py

import time
from rate_limiter.token_bucket import TokenBucketRateLimiter


def test_token_bucket_allows_within_capacity():
    limiter = TokenBucketRateLimiter(capacity=3, refill_rate_per_second=1000.0)
    key = "client1"

    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    # 4th request without refill should be blocked
    assert not limiter.allow_request(key)


def test_token_bucket_refills_over_time():
    limiter = TokenBucketRateLimiter(capacity=2, refill_rate_per_second=1.0)
    key = "client2"

    assert limiter.allow_request(key)
    assert limiter.allow_request(key)
    assert not limiter.allow_request(key)

    # Wait enough time for 1 token to refill
    time.sleep(1.1)

    assert limiter.allow_request(key)
