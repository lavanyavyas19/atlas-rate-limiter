from fastapi import FastAPI, Request, HTTPException
from typing import Dict

from rate_limiter.fixed_window import FixedWindowRateLimiter
from rate_limiter.sliding_window import SlidingWindowRateLimiter
from rate_limiter.token_bucket import TokenBucketRateLimiter
from monitoring.usage_log import UsageLogger

from rate_limiter.base import RateLimiter  # adjust import if your base path differs

app = FastAPI(
    title="Atlas Rate Limiter",
    description="Intelligent API rate limiting and usage monitoring service",
    version="1.0.0",
)

usage_logger = UsageLogger()

# Per-client rate limit configuration
CLIENT_RATE_LIMITS = {
    "anonymous": {
        "algo": "fixed",
        "limit": 100,
        "window_seconds": 60,
    },
    "client_basic": {
        "algo": "fixed",
        "limit": 50,
        "window_seconds": 60,
    },
    "client_premium": {
        "algo": "sliding",
        "limit": 200,
        "window_seconds": 60,
    },
    "internal_service": {
        "algo": "token",
        "capacity": 500,
        "refill_rate_per_second": 5.0,
    },
}

# Store a separate rate limiter instance per client
rate_limiters: Dict[str, RateLimiter] = {}


def get_client_id(request: Request) -> str:
    """
    Derive client identity from headers. Falls back to 'anonymous'.
    """
    return request.headers.get("x-client-id", "anonymous")


def get_or_create_rate_limiter(client_id: str) -> RateLimiter:
    """
    Lazily create a rate limiter instance appropriate for the given client
    based on CLIENT_RATE_LIMITS configuration.
    """
    config = CLIENT_RATE_LIMITS.get(client_id, CLIENT_RATE_LIMITS["anonymous"])
    algo = config.get("algo", "fixed")

    if client_id not in rate_limiters:
        if algo == "sliding":
            rate_limiters[client_id] = SlidingWindowRateLimiter(
                limit=config["limit"],
                window_seconds=config["window_seconds"],
            )
        elif algo == "token":
            rate_limiters[client_id] = TokenBucketRateLimiter(
                capacity=config["capacity"],
                refill_rate_per_second=config["refill_rate_per_second"],
            )
        else:
            rate_limiters[client_id] = FixedWindowRateLimiter(
                limit=config["limit"],
                window_seconds=config["window_seconds"],
            )

    return rate_limiters[client_id]


@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_id(request)
    limiter = get_or_create_rate_limiter(client_id)

    usage_logger.log_request(client_id)
    allowed = limiter.allow_request(client_id)

    if not allowed:
        usage_logger.log_violation(client_id)
        raise HTTPException(status_code=429, detail="Too Many Requests")

    response = await call_next(request)
    return response


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/stats")
async def stats():
    """
    Global statistics across all clients.
    """
    return usage_logger.get_stats()


@app.get("/stats/{client_id}")
async def stats_for_client(client_id: str):
    """
    Statistics for a specific client.
    """
    return usage_logger.get_client_stats(client_id)


@app.get("/demo")
async def demo():
    return {"message": "You're inside a rate-limited endpoint!"}
