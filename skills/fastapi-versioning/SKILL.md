---
name: fastapi-versioning
description: "FastAPI API versioning stratejileri (/v1, header, query) — Sentinel gateway'de geriye dönük uyumluluk yönetimi"
---

## Purpose
API versioning, mevcut istemcileri bozmadan yeni özellik ve breaking change'leri yayınlamayı sağlar. Sentinel'de URL path versioning (`/api/v1/`) tercih edilir; header-based versioning opsiyonel olarak desteklenir.

## Workflow

### 1. URL path versioning (birincil strateji)

```
/api/v1/traces/{id}    → mevcut
/api/v2/traces/{id}    → yeni format, v1 paralel çalışır
```

```python
# app/api/v1/router.py
from fastapi import APIRouter
from app.api.v1 import traces, metrics, alerts

v1_router = APIRouter(prefix="/api/v1")
v1_router.include_router(traces.router, prefix="/traces")
v1_router.include_router(metrics.router, prefix="/metrics")

# app/api/v2/router.py
v2_router = APIRouter(prefix="/api/v2")
v2_router.include_router(traces_v2.router, prefix="/traces")

# main.py
app.include_router(v1_router)
app.include_router(v2_router)
```

### 2. Header-based versioning

```python
from fastapi import Header, HTTPException

async def get_api_version(
    accept_version: str | None = Header(None, alias="X-API-Version"),
) -> str:
    supported = {"1.0", "2.0"}
    version = accept_version or "1.0"
    if version not in supported:
        raise HTTPException(
            400,
            f"Desteklenmeyen API versiyonu: {version}. Geçerliler: {supported}",
        )
    return version

@router.get("/traces/{trace_id}")
async def get_trace(
    trace_id: str,
    api_version: str = Depends(get_api_version),
):
    if api_version == "2.0":
        return await tempo_service.get_trace_v2(trace_id)
    return await tempo_service.get_trace(trace_id)
```

### 3. Deprecation header

```python
from datetime import date
from starlette.middleware.base import BaseHTTPMiddleware

DEPRECATED_PATHS = {
    "/api/v1/traces": {
        "deprecated": True,
        "sunset": "2027-01-01",
        "successor": "/api/v2/traces",
    }
}

class DeprecationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        response = await call_next(request)
        for path, info in DEPRECATED_PATHS.items():
            if request.url.path.startswith(path):
                response.headers["Deprecation"] = info["sunset"]
                response.headers["Sunset"] = info["sunset"]
                response.headers["Link"] = f'<{info["successor"]}>; rel="successor-version"'
        return response
```

### 4. Versiyonlu response model

```python
# v1: basit model
class TraceResponseV1(BaseModel):
    trace_id: str
    spans: list[dict]

# v2: zengin model, backwards compatible değil
class TraceResponseV2(BaseModel):
    trace_id: str
    root_service: str
    duration_ms: float
    spans: list[SpanModel]      # detaylı SpanModel
    resource_attributes: dict   # yeni alan

# Router'da ayrı endpoint
@v2_router.get("/traces/{id}", response_model=TraceResponseV2)
async def get_trace_v2(trace_id: str):
    ...
```

### 5. OpenAPI versiyona göre ayrı docs

```python
v1_app = FastAPI(title="Sentinel API v1", version="1.0.0", docs_url="/api/v1/docs")
v2_app = FastAPI(title="Sentinel API v2", version="2.0.0", docs_url="/api/v2/docs")

app.mount("/api/v1", v1_app)
app.mount("/api/v2", v2_app)
```

## Common mistakes

- V1 ve V2'yi aynı router'dan `if version ==` ile yönetmek — kod karmaşıklaşır, ayrı modüller kullan
- V1'i anında kaldırmak — en az 6 ay deprecation notice ver
- Versiyonu query param olarak tutmak (`?version=2`) — REST pratiğinde URL path veya header tercih edilir
- V2 response modelini V1 ile geriye dönük uyumlu yapmaya çalışmak — amacı bozar, clean break yap

## References
- `skills/fastapi-app-structure`
- `skills/fastapi-middleware`
- `skills/fastapi-openapi-customization`
