---
name: fastapi-middleware
description: "FastAPI middleware yazımı (CORS, logging, auth) — Sentinel gateway'in çapraz kesim ihtiyaçları için"
---

## Purpose
Middleware, her HTTP isteğini ve yanıtını yakalayarak merkezi logging, CORS, trace propagation ve süre ölçümü sağlar. Sentinel'in gateway'i tüm upstream isteklerini bu katmandan geçirir; böylece her endpoint tekrar tekrar aynı kodları yazmak zorunda kalmaz.

## Workflow

### 1. Middleware kayıt fonksiyonu

```python
# app/middleware.py
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.trace import TraceContextMiddleware
from app.middleware.timing import TimingMiddleware

def register_middleware(app: FastAPI) -> None:
    # Sıra önemli: dıştan içe uygulanır (son eklenen ilk çalışır)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],   # production'da kısıtla
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(TraceContextMiddleware)
    app.add_middleware(TimingMiddleware)
    app.add_middleware(RequestLoggingMiddleware)
```

### 2. Logging middleware

```python
# app/middleware/logging.py
import structlog
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

log = structlog.get_logger()

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        log.info(
            "http_request",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            client_ip=request.client.host if request.client else "unknown",
        )
        return response
```

### 3. Trace context propagation

```python
# app/middleware/trace.py
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from structlog.contextvars import bind_contextvars, clear_contextvars

class TraceContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        clear_contextvars()
        trace_id = (
            request.headers.get("X-Trace-ID")
            or request.headers.get("traceparent", "").split("-")[1] if "traceparent" in request.headers else None
            or str(uuid.uuid4())
        )
        bind_contextvars(trace_id=trace_id, service="sentinel-gateway")

        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id
        return response
```

### 4. Timing middleware

```python
# app/middleware/timing.py
import time
from starlette.middleware.base import BaseHTTPMiddleware
from prometheus_client import Histogram

REQUEST_DURATION = Histogram(
    "http_request_duration_seconds",
    "HTTP request duration",
    labelnames=["method", "path", "status_code"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5],
)

class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        REQUEST_DURATION.labels(
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
        ).observe(duration)

        response.headers["X-Response-Time"] = f"{duration * 1000:.2f}ms"
        return response
```

### 5. Pure ASGI middleware (BaseHTTPMiddleware yerine)

```python
# Daha performanslı, streaming response destekler
class RawTimingMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        start = time.perf_counter()
        await self.app(scope, receive, send)
        log.debug("request_duration", ms=(time.perf_counter() - start) * 1000)
```

## Common mistakes

- `BaseHTTPMiddleware` ile streaming response kullanmak — tüm body belleğe yüklenir; streaming gerekiyorsa pure ASGI middleware yaz
- Middleware sırasını yanlış kurmak — `add_middleware` ters sırayla uygulanır (son eklenen = ilk çalışan)
- Exception handler'dan önce middleware'in hatayı yakalaması — exception handler middleware'den sonra gelmeli
- `call_next` öncesinde response header ayarlamaya çalışmak — response henüz oluşmadı

## References
- `skills/fastapi-app-structure`
- `skills/fastapi-exception-handlers`
- `skills/fastapi-observability`
- `skills/python-logging-structlog`
