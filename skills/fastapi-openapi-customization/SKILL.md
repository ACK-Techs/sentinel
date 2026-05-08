---
name: fastapi-openapi-customization
description: "FastAPI OpenAPI/Swagger özelleştirme — Sentinel API dokümantasyonu için şema, tag ve güvenlik tanımları"
---

## Purpose
Varsayılan FastAPI OpenAPI şeması genellikle eksik tag açıklamaları, güvenlik tanımları ve örnek değerler içerir. Sentinel'in gateway API'si Swagger UI üzerinden iç ekiplere sunulur; özelleştirilmiş şema ile operasyonel rehber entegre edilir.

## Workflow

### 1. App metadata ve tag tanımları

```python
# app/main.py
tags_metadata = [
    {
        "name": "Traces",
        "description": "Grafana Tempo'dan distributed trace sorgulama ve analiz.",
        "externalDocs": {
            "description": "Tempo API Docs",
            "url": "https://grafana.com/docs/tempo/",
        },
    },
    {
        "name": "Metrics",
        "description": "Prometheus metrik sorgulama (instant ve range query).",
    },
    {
        "name": "Alerts",
        "description": "Alertmanager alert yönetimi ve silencing.",
    },
    {"name": "Health", "description": "Kubernetes health probe endpoint'leri."},
]

app = FastAPI(
    title="Sentinel Observability Gateway",
    description="""
## Sentinel API

Sentinel'in tüm observability backend'lerine (Tempo, Prometheus, Alertmanager)
tek noktadan erişim sağlar.

### Kimlik Doğrulama
`Authorization: Bearer <JWT>` header'ı gereklidir.
    """,
    version="1.0.0",
    openapi_tags=tags_metadata,
    contact={
        "name": "Platform Team",
        "email": "platform@example.com",
    },
    license_info={"name": "Apache 2.0"},
)
```

### 2. Güvenlik şeması

```python
from fastapi.security import OAuth2PasswordBearer, HTTPBearer

# JWT Bearer Security tanımı
security_scheme = HTTPBearer(description="JWT token (Authorization: Bearer <token>)")

# OpenAPI'ye security requirement ekle
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    from fastapi.openapi.utils import get_openapi
    schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    # Tüm endpoint'lere global security uygula
    for path in schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"BearerAuth": []}])
    app.openapi_schema = schema
    return schema

app.openapi = custom_openapi
```

### 3. Pydantic model örnekleri

```python
from pydantic import BaseModel, Field

class TraceQueryRequest(BaseModel):
    service: str = Field(..., example="sentinel-gateway", description="Servis adı")
    start: str = Field("now-1h", example="2026-05-09T10:00:00Z")
    end: str = Field("now", example="2026-05-09T11:00:00Z")
    limit: int = Field(20, ge=1, le=100, example=20)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "summary": "Son 1 saat gateway trace",
                    "value": {"service": "sentinel-gateway", "start": "now-1h", "limit": 10},
                }
            ]
        }
    }
```

### 4. Response örnekleri ve openapi_extra

```python
@router.get(
    "/traces/{trace_id}",
    response_model=TraceResponse,
    summary="Trace detayı getir",
    description="Belirtilen trace ID için tüm span'ları döndürür.",
    responses={
        404: {"description": "Trace bulunamadı", "model": ErrorResponse},
        504: {"description": "Tempo yanıt vermedi", "model": ErrorResponse},
    },
    openapi_extra={
        "x-sentinel-tier": "observability",
        "x-rate-limit": "100/min",
    },
)
async def get_trace(trace_id: str): ...
```

## Common mistakes

- `docs_url=None` yaparken `openapi_url=None` yapmamak — raw şema hâlâ erişilebilir kalır
- `custom_openapi` fonksiyonunu her seferinde cache'lememek — her `/openapi.json` isteğinde yeniden üretilir, pahalı
- Tag'leri `openapi_tags` yerine yalnızca router'da tanımlamak — açıklama ve externalDocs gösterilemez
- `Field(example=...)` ile `model_config json_schema_extra` örneklerini karıştırmak — Pydantic v2'de `example` field deprecated, `examples` kullan

## References
- `skills/fastapi-app-structure`
- `skills/fastapi-security-oauth2`
- `skills/fastapi-pydantic-v2`
