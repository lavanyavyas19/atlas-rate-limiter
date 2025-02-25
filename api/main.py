from fastapi import FastAPI, Request, HTTPException
from rate_limiter.fixed_window import FixedWindowRateLimiter
from monitoring.usage_log import UsageLogger

app = FastAPI(
    title="Atlas Rate Limiter",
    description="Intelligent API rate limiting and usage monitoring service",
    version="0.1.0"
)

usage_logger = UsageLogger()

# Per-client rate limit configuration
CLIENT_RATE_LIMITS = {
    "anonymous": {"limit": 100, "window_seconds": 60},
    "client_basic": {"limit": 50, "window_seconds": 60},
    "client_premium": {"limit": 200, "window_seconds": 60},
}

# Store a separate rate limiter for each client
rate_limiters = {}

def get_client_id(request: Request) -> str:
    return request.headers.get("x-client-id", "anonymous")

def get_or_create_rate_limiter(client_id: str) -> FixedWindowRateLimiter:
    config = CLIENT_RATE_LIMITS.get(client_id, CLIENT_RATE_LIMITS["anonymous"])

    if client_id not in rate_limiters:
        rate_limiters[client_id] = FixedWindowRateLimiter(
            limit=config["limit"],
            window_seconds=config["window_seconds"]
        )

    return rate_limiters[client_id]

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_id(request)

    limiter = get_or_create_rate_limiter(client_id)
    allowed = limiter.allow_request(client_id)

    usage_logger.log_request(client_id)

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
    return usage_logger.get_stats()

@app.get("/demo")
async def demo():
    return {"message": "You're inside a rate-limited endpoint!"}
