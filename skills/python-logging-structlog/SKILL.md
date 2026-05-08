---
name: python-logging-structlog
description: "structlog ile yapılandırılmış JSON log üretimi — Sentinel servislerinde makine-okunabilir log formatı için kullanılır"
---

## Purpose
structlog, Python'un standart `logging` modülünün üzerine oturan ve her log satırını anahtar-değer çiftleriyle zenginleştiren bir kütüphanedir. Sentinel'in Loki/OpenTelemetry stack'iyle uyumlu JSON log çıktısı üretmek için tercih edilir. Her log kaydı trace_id, service_name, environment gibi bağlamsal alanlar taşır ve log aggregation sistemlerinde filtreleme/arama maliyetini düşürür.

## Workflow

### 1. Kurulum ve temel yapılandırma

```python
# logging_config.py
import logging
import structlog

def configure_logging(service_name: str, level: str = "INFO") -> None:
    shared_processors = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.stdlib.add_logger_name,
        structlog.processors.StackInfoRenderer(),
    ]

    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processors=[
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            structlog.processors.JSONRenderer(),
        ],
        foreign_pre_chain=shared_processors,
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(getattr(logging, level.upper()))
```

### 2. Bağlam değişkeni ile log zenginleştirme

```python
import structlog
from structlog.contextvars import bind_contextvars, clear_contextvars

log = structlog.get_logger(__name__)

async def handle_request(request_id: str, user_id: str):
    clear_contextvars()
    bind_contextvars(request_id=request_id, user_id=user_id)

    log.info("request_started", path=request.url.path)
    # Her log satırı otomatik olarak request_id ve user_id içerir
    result = await process(request)
    log.info("request_completed", status_code=200, duration_ms=42)
    return result
```

### 3. FastAPI middleware ile otomatik bağlam

```python
import uuid
from fastapi import Request
from structlog.contextvars import bind_contextvars, clear_contextvars

@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    clear_contextvars()
    bind_contextvars(
        trace_id=request.headers.get("X-Trace-ID", str(uuid.uuid4())),
        method=request.method,
        path=request.url.path,
    )
    response = await call_next(request)
    log.info("http_request", status_code=response.status_code)
    return response
```

### 4. Sentinel log formatı (Loki uyumlu)

```json
{
  "timestamp": "2026-05-09T12:00:00Z",
  "level": "info",
  "logger": "sentinel.gateway",
  "event": "request_completed",
  "trace_id": "abc123",
  "user_id": "u-42",
  "duration_ms": 17,
  "status_code": 200
}
```

## Common mistakes

- `logging.basicConfig()` ile structlog birlikte yapılandırılırsa çift log satırı oluşur — sadece structlog formatter kullan
- `bind_contextvars` thread-local değil contextvars tabanlıdır; async ortamda her request başında `clear_contextvars()` çağrılmazsa önceki isteğin bağlamı sızar
- `JSONRenderer` yerine `ConsoleRenderer` production'da kullanılırsa Loki parse edemez
- `cache_logger_on_first_use=True` ile yapılandırma sonradan değiştirilemez — test sırasında `False` yap

## References
- `skills/fastapi-middleware`
- `skills/fastapi-observability`
- `skills/python-error-hierarchy`
