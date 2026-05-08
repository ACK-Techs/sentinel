---
name: python-error-hierarchy
description: "Python hata hiyerarşisi tasarımı ve özel exception sınıfları — Sentinel servislerinde tutarlı hata yönetimi için"
---

## Purpose
İyi tasarlanmış bir exception hiyerarşisi, servis katmanlarının birbirinden bağımsız hata fırlatmasını ve üst katmanların genel `except` bloklarıyla yakalamasını sağlar. Sentinel'de her domain (auth, observability, agent) kendi taban exception sınıfına sahiptir; bu sayede FastAPI exception handler'lar spesifik HTTP kodu döndürebilir.

## Workflow

### 1. Taban hiyerarşi

```python
# exceptions/base.py
from dataclasses import dataclass, field
from typing import Any

class SentinelError(Exception):
    """Tüm Sentinel hataları için kök sınıf."""
    message: str = "Beklenmedik bir hata oluştu."
    code: str = "SENTINEL_ERROR"
    http_status: int = 500

    def __init__(self, message: str | None = None, **context: Any):
        self.message = message or self.__class__.message
        self.context = context
        super().__init__(self.message)

    def to_dict(self) -> dict:
        return {
            "error": self.code,
            "message": self.message,
            "context": self.context,
        }
```

### 2. Domain hiyerarşisi

```python
# exceptions/auth.py
class AuthError(SentinelError):
    code = "AUTH_ERROR"
    http_status = 401

class TokenExpiredError(AuthError):
    code = "TOKEN_EXPIRED"
    message = "Oturum süresi doldu."

class InsufficientPermissionsError(AuthError):
    code = "INSUFFICIENT_PERMISSIONS"
    http_status = 403
    message = "Bu işlem için yetkiniz yok."

# exceptions/observability.py
class ObservabilityError(SentinelError):
    code = "OBS_ERROR"
    http_status = 502

class MetricQueryError(ObservabilityError):
    code = "METRIC_QUERY_FAILED"

class TraceNotFoundError(ObservabilityError):
    code = "TRACE_NOT_FOUND"
    http_status = 404
```

### 3. FastAPI handler entegrasyonu

```python
from fastapi import Request
from fastapi.responses import JSONResponse
from exceptions.base import SentinelError

@app.exception_handler(SentinelError)
async def sentinel_error_handler(request: Request, exc: SentinelError):
    return JSONResponse(
        status_code=exc.http_status,
        content=exc.to_dict(),
    )
```

### 4. Servis katmanında kullanım

```python
async def get_trace(trace_id: str) -> Trace:
    result = await tempo_client.fetch(trace_id)
    if result is None:
        raise TraceNotFoundError(
            f"Trace {trace_id} bulunamadı.",
            trace_id=trace_id,
            backend="tempo",
        )
    return result
```

### 5. Hiyerarşi şeması

```
SentinelError (500)
├── AuthError (401)
│   ├── TokenExpiredError
│   └── InsufficientPermissionsError (403)
├── ValidationError (422)
│   └── SchemaValidationError
└── ObservabilityError (502)
    ├── MetricQueryError
    └── TraceNotFoundError (404)
```

## Common mistakes

- `Exception` yerine doğrudan `SentinelError`'dan türetmemek — catch-all `except SentinelError` çalışmaz
- `http_status` sınıf değişkenini instance üzerinde override etmeyi unutmak — kalıtımda `http_status = 404` class-level tanımlanmalı
- Context bilgisini exception mesajına gömmek yerine `**context` kwarg olarak geçmemek — loglarda kaybolur
- `to_dict()` metodunu serialization için override etmemek — JSON response'ta iç Python nesneleri göründüğünde TypeError

## References
- `skills/fastapi-exception-handlers`
- `skills/python-logging-structlog`
- `skills/fastapi-app-structure`
