---
name: fastapi-exception-handlers
description: "FastAPI özel exception handler ve hata yanıt formatı — Sentinel'de tutarlı API hata envelope'u"
---

## Purpose
FastAPI varsayılan hata yanıtları Pydantic ValidationError ve HTTPException için farklı formatlar kullanır. Sentinel'de tüm hataların aynı envelope yapısında döndürülmesi için merkezi exception handler sistemi kurulur; böylece istemci tek bir format beklentisiyle çalışabilir.

## Workflow

### 1. Standart hata envelope

```python
# app/models/error.py
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    field: str | None = None
    message: str

class ErrorResponse(BaseModel):
    error: str          # hata kodu: TRACE_NOT_FOUND
    message: str        # insan okunabilir mesaj
    details: list[ErrorDetail] = []
    request_id: str | None = None
```

### 2. Exception handler kayıt fonksiyonu

```python
# app/exceptions.py
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.exceptions.base import SentinelError
from app.models.error import ErrorResponse, ErrorDetail
import structlog

log = structlog.get_logger()

def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(SentinelError, sentinel_error_handler)
    app.add_exception_handler(RequestValidationError, validation_error_handler)
    app.add_exception_handler(StarletteHTTPException, http_exception_handler)
    app.add_exception_handler(Exception, unhandled_error_handler)
```

### 3. Handler implementasyonları

```python
async def sentinel_error_handler(request: Request, exc: SentinelError) -> JSONResponse:
    log.warning("sentinel_error", error_code=exc.code, **exc.context)
    return JSONResponse(
        status_code=exc.http_status,
        content=ErrorResponse(
            error=exc.code,
            message=exc.message,
            request_id=request.headers.get("X-Request-ID"),
        ).model_dump(),
    )

async def validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    details = [
        ErrorDetail(
            field=".".join(str(loc) for loc in error["loc"][1:]),
            message=error["msg"],
        )
        for error in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content=ErrorResponse(
            error="VALIDATION_ERROR",
            message="İstek doğrulama başarısız.",
            details=details,
        ).model_dump(),
    )

async def http_exception_handler(
    request: Request, exc: StarletteHTTPException
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=ErrorResponse(
            error=f"HTTP_{exc.status_code}",
            message=exc.detail,
        ).model_dump(),
    )

async def unhandled_error_handler(request: Request, exc: Exception) -> JSONResponse:
    log.error("unhandled_error", exc_type=type(exc).__name__, exc=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="INTERNAL_ERROR",
            message="Beklenmedik bir hata oluştu.",
        ).model_dump(),
    )
```

### 4. Test

```python
async def test_validation_error_format(client):
    response = await client.post("/api/v1/traces", json={"invalid": "payload"})
    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "VALIDATION_ERROR"
    assert "details" in body
    assert isinstance(body["details"], list)
```

## Common mistakes

- `HTTPException` ile `StarletteHTTPException` handler'larını karıştırmak — FastAPI HTTPException, Starlette'inkinin alt sınıfıdır; `StarletteHTTPException` handler her ikisini de yakalar
- `RequestValidationError` handler kaydetmemek — Pydantic validation hataları varsayılan 422 formatında döner, envelope bozulur
- `unhandled_error_handler` içinde stack trace döndürmek — production'da internal bilgi sızdırır
- Exception handler'ları middleware'den sonra `add_exception_handler` ile kaydetmek — sıra önemlidir, `register_middleware` öncesinde çağır

## References
- `skills/python-error-hierarchy`
- `skills/fastapi-app-structure`
- `skills/fastapi-pydantic-v2`
