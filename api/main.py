from fastapi import FastAPI, Request, HTTPException
from rate_limiter.fixed_window import FixedWindowRateLimiter
from monitoring.usage_log import UsageLogger

app = FastAPI(
    title="Atlas Rate Limiter",
    description="Intelligent API rate limiting and usage monitoring service",
    version="0.1.0"
)

rate_limiter = FixedWindowRateLimiter(limit=100, window_seconds=60)
usage_logger = UsageLogger()

def get_client_id(request: Request) -> str:
    return request.headers.get("x-client-id", "anonymous")

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    client_id = get_client_id(request)
    allowed = rate_limiter.allow_request(client_id)

    usage_logger.log_request(client_id)

    if not allowed:
        usage_logger.log_violation(client_id)
        raise HTTPException(status_code=429, detail="Too Many Requests")

    return await call_next(request)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/stats")
async def stats():
    return usage_logger.get_stats()

@app.get("/demo")
async def demo():
    return {"message": "You're inside a rate-limited endpoint!"}
