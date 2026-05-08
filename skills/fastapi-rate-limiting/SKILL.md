---
name: fastapi-rate-limiting
description: "FastAPI'de rate limiting (slowapi, token bucket) — Sentinel API abuse koruması ve kullanım kotası"
---

## Purpose
Sentinel'in public API'si kötüye kullanım ve kaynak tükenmesine karşı rate limit uygulaması gerektirir. Hem per-user hem per-IP limitleme, limit aşıldığında standart 429 yanıtı ve Retry-After header'ı bu skill'in kapsamındadır.

## Workflow

### 1. slowapi entegrasyonu

```python
# app/rate_limiting.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from fastapi import Request

def get_rate_limit_key(request: Request) -> str:
    """API key varsa key'e, yoksa IP'ye göre limitlir."""
    api_key = request.headers.get("X-API-Key")
    if api_key:
        return f"apikey:{api_key}"
    return f"ip:{get_remote_address(request)}"

limiter = Limiter(
    key_func=get_rate_limit_key,
    default_limits=["100/minute", "1000/hour"],
    storage_uri="redis://redis:6379/1",
)

# main.py
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
```

### 2. Endpoint bazlı limit

```python
# app/api/v1/traces.py
from app.rate_limiting import limiter

@router.get("/traces/{trace_id}")
@limiter.limit("50/minute")  # Endpoint özel limit
async def get_trace(request: Request, trace_id: str):
    ...

@router.post("/traces/bulk-export")
@limiter.limit("5/minute;10/hour")  # Birden fazla pencere
async def bulk_export(request: Request):
    ...
```

### 3. Özelleştirilmiş 429 yanıtı

```python
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded

async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded) -> JSONResponse:
    return JSONResponse(
        status_code=429,
        content={
            "error": "RATE_LIMIT_EXCEEDED",
            "message": f"İstek limiti aşıldı. Limit: {exc.limit.limit}",
            "retry_after": exc.limit.reset_at,
        },
        headers={
            "Retry-After": str(int(exc.limit.reset_at - time.time())),
            "X-RateLimit-Limit": str(exc.limit.limit.amount),
            "X-RateLimit-Reset": str(exc.limit.reset_at),
        },
    )
```

### 4. Token bucket (Redis tabanlı özel implementasyon)

```python
import redis.asyncio as aioredis
import time

class TokenBucketLimiter:
    def __init__(self, redis: aioredis.Redis, capacity: int = 100, refill_rate: float = 1.0):
        self.redis = redis
        self.capacity = capacity
        self.refill_rate = refill_rate  # token/saniye

    async def is_allowed(self, key: str) -> tuple[bool, int]:
        """(allowed, remaining) döndürür."""
        now = time.time()
        pipe = self.redis.pipeline()
        bucket_key = f"tb:{key}"

        pipe.hgetall(bucket_key)
        tokens_data, = await pipe.execute()

        tokens = float(tokens_data.get(b"tokens", self.capacity))
        last_refill = float(tokens_data.get(b"last_refill", now))

        # Refill
        elapsed = now - last_refill
        tokens = min(self.capacity, tokens + elapsed * self.refill_rate)

        if tokens < 1:
            return False, 0

        tokens -= 1
        await self.redis.hset(bucket_key, mapping={"tokens": tokens, "last_refill": now})
        await self.redis.expire(bucket_key, 3600)
        return True, int(tokens)
```

### 5. Tier bazlı limit

```python
TIER_LIMITS = {
    "free": "20/minute",
    "pro": "200/minute",
    "enterprise": "2000/minute",
}

def get_user_tier_limit(request: Request) -> str:
    user = getattr(request.state, "current_user", None)
    tier = getattr(user, "tier", "free") if user else "free"
    return TIER_LIMITS.get(tier, TIER_LIMITS["free"])
```

## Common mistakes

- `request: Request` parametresini route signature'dan çıkarmak — slowapi decorator'ı Request nesnesine ihtiyaç duyar
- Redis bağlantısı olmadan in-memory limiter kullanmak — birden fazla pod'da limit paylaşılmaz
- `RateLimitExceeded` exception handler kaydetmemek — 500 Internal Server Error döner
- `@limiter.limit` decorator'ını `@router.get` altına koymak — slowapi için her zaman üstte olmalı

## References
- `skills/fastapi-security-apikey`
- `skills/fastapi-middleware`
- `skills/fastapi-observability`
