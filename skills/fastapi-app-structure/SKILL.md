---
name: fastapi-app-structure
description: "FastAPI uygulama klasör yapısı ve modül organizasyonu — Sentinel gateway ve servislerinin proje iskeleti"
---

## Purpose
Düzgün organize edilmiş bir FastAPI projesi, router'ların, model katmanlarının, dependency'lerin ve konfigurasyon dosyalarının nereden import edileceğini netleştirir. Sentinel'in gateway servisi bu yapıya uyar; yeni servisler aynı iskeleti kullanarak hızlıca kurulabilir.

## Workflow

### 1. Dizin yapısı

```
sentinel-gateway/
├── src/
│   └── app/
│       ├── __init__.py
│       ├── main.py              # FastAPI app factory
│       ├── config.py            # Pydantic Settings
│       ├── dependencies.py      # Ortak Depends() factory'leri
│       ├── exceptions.py        # Custom exception sınıfları
│       ├── middleware.py        # CORS, logging, trace middleware
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   ├── v1/
│       │   │   ├── __init__.py
│       │   │   ├── router.py    # v1 router aggregate
│       │   │   ├── traces.py    # /traces endpoint'leri
│       │   │   ├── metrics.py   # /metrics endpoint'leri
│       │   │   └── alerts.py    # /alerts endpoint'leri
│       │   └── health.py        # /health, /ready, /live
│       │
│       ├── services/
│       │   ├── tempo_service.py
│       │   ├── prometheus_service.py
│       │   └── alert_service.py
│       │
│       ├── clients/
│       │   ├── tempo_client.py
│       │   └── prometheus_client.py
│       │
│       └── models/
│           ├── trace.py         # Pydantic request/response modelleri
│           ├── metric.py
│           └── alert.py
├── tests/
│   ├── conftest.py
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── Dockerfile
```

### 2. App factory (main.py)

```python
# src/app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.api.v1.router import v1_router
from app.api.health import health_router
from app.middleware import register_middleware
from app.exceptions import register_exception_handlers
from app.config import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await startup()
    yield
    # Shutdown
    await shutdown()

def create_app() -> FastAPI:
    app = FastAPI(
        title="Sentinel Gateway",
        version=settings.app_version,
        docs_url="/docs" if settings.docs_enabled else None,
        redoc_url=None,
        lifespan=lifespan,
    )
    register_middleware(app)
    register_exception_handlers(app)
    app.include_router(health_router)
    app.include_router(v1_router, prefix="/api/v1")
    return app

app = create_app()
```

### 3. Router aggregate (api/v1/router.py)

```python
from fastapi import APIRouter
from app.api.v1 import traces, metrics, alerts

v1_router = APIRouter()
v1_router.include_router(traces.router, prefix="/traces", tags=["Traces"])
v1_router.include_router(metrics.router, prefix="/metrics", tags=["Metrics"])
v1_router.include_router(alerts.router, prefix="/alerts", tags=["Alerts"])
```

### 4. Endpoint modülü (api/v1/traces.py)

```python
from fastapi import APIRouter, Depends, Query
from app.services.tempo_service import TempoService
from app.dependencies import get_tempo_service
from app.models.trace import TraceResponse, TraceListResponse

router = APIRouter()

@router.get("/{trace_id}", response_model=TraceResponse)
async def get_trace(
    trace_id: str,
    service: str | None = Query(None),
    tempo: TempoService = Depends(get_tempo_service),
) -> TraceResponse:
    return await tempo.get_trace(trace_id, service_filter=service)
```

## Common mistakes

- Servis mantığını doğrudan router fonksiyonuna yazmak — service katmanı mutlaka ayrılmalı
- `app = FastAPI()` yerine factory kullanmamak — test sırasında override edilemez
- `models/` içine ORM modellerini koymak — Pydantic (request/response) ve ORM modelleri ayrı klasörlerde olmalı
- Router'ları `main.py`'de inline tanımlamak — 3 endpoint sonrası yönetilemez hale gelir

## References
- `skills/fastapi-dependency-injection`
- `skills/fastapi-exception-handlers`
- `skills/fastapi-middleware`
- `skills/fastapi-lifespan`
