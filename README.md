# 🚀 Atlas – Intelligent API Rate Limiter & Usage Monitoring Framework

Atlas is a complete backend service designed to enforce API rate limits, protect services from abuse, and provide real-time visibility into API usage patterns.

Built using **FastAPI**, Atlas includes:

- Multiple rate limiting algorithms (fixed window, sliding window, token bucket)
- Per-client dynamic limit configuration
- Request and violation analytics
- Monitoring endpoints for operators
- Clean architecture for extensibility
- Test coverage for the core rate limiting engine
- Ready-to-run Docker setup

Atlas can be embedded into existing microservices or run as a standalone rate-limiting gateway.

---

## 🔧 Key Features

### ⚙️ Rate Limiting Algorithms

Atlas implements three strategies behind a shared `RateLimiter` interface:

- **Fixed Window** – Simple, predictable per-window limits  
- **Sliding Window** – Smooth distribution of requests over time  
- **Token Bucket** – Allows short bursts while enforcing an overall rate

---

### 👥 Per-Client Configurable Limits

Each client (from header `x-client-id`) can have its own configuration.

Example:

| Client Type      | Algorithm      | Limit                      |
|------------------|----------------|----------------------------|
| anonymous        | fixed window   | 100 requests / minute      |
| client_basic     | fixed window   | 50 requests / minute       |
| client_premium   | sliding window | 200 requests / minute      |
| internal_service | token bucket   | 500 req/min with bursting  |

If `x-client-id` is missing, the client is treated as **anonymous**.

---

### 📊 Monitoring & Metrics

Atlas tracks:

- Total requests
- Total violations
- Per-client statistics
- “Hot” clients with high violation rates

Endpoints expose:

- Global stats (`/stats`)
- Per-client stats (`/stats/{client_id}`)
- Optional Prometheus-style metrics at `/metrics` (for integration with Grafana).

---

## 🧱 Project Structure

```text
atlas-rate-limiter/
├── api/
│   └── main.py
├── rate_limiter/
│   ├── base.py
│   ├── fixed_window.py
│   ├── sliding_window.py
│   └── token_bucket.py
├── monitoring/
│   └── usage_log.py
├── tests/
│   ├── test_fixed_window.py
│   ├── test_sliding_window.py
│   └── test_token_bucket.py
├── config/
│   └── rate_limits.yaml
├── Dockerfile
├── docker-compose.yml
├── README.md
└── TODO.md

Running Atlas
1. Install dependencies
pip install -r requirements.txt

2. Start the API locally
uvicorn api.main:app --reload


Open the interactive docs at:

http://127.0.0.1:8000/docs

Architecture

Atlas is built around:

FastAPI middleware for request interception

Pluggable rate limiter backends implementing a common interface

Config-driven per-client behavior

Monitoring layer for stats and potential alerting

This separation makes it easy to add new algorithms or swap storage backends (e.g., in-memory vs Redis) without changing the API layer.