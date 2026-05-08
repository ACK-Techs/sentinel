---
name: fastapi-lifespan
description: "FastAPI lifespan event (startup/shutdown) yönetimi — Sentinel servislerinde connection pool ve kaynak yaşam döngüsü"
---

## Purpose
FastAPI'nin lifespan context manager'ı, uygulama başlangıcında kaynakları (DB pool, HTTP client, cache) oluşturur ve uygulama kapanışında temiz kapatmayı garantiler. Sentinel'de Tempo client, Prometheus client ve background task loop'ları lifespan'da yönetilir.

## Workflow

### 1. Temel lifespan pattern

```python
# app/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
import httpx
import structlog

log = structlog.get_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # === STARTUP ===
    log.info("startup_begin")

    # HTTP client pool (paylaşılan)
    app.state.http_client = httpx.AsyncClient(
        timeout=httpx.Timeout(10.0),
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )

    # DB pool
    app.state.db_pool = await create_db_pool(settings.database_url.get_secret_value())

    # Background task'ları başlat
    app.state.metric_push_task = asyncio.create_task(metric_push_loop())

    log.info("startup_complete")
    yield

    # === SHUTDOWN ===
    log.info("shutdown_begin")

    app.state.metric_push_task.cancel()
    try:
        await app.state.metric_push_task
    except asyncio.CancelledError:
        pass

    await app.state.http_client.aclose()
    await app.state.db_pool.close()

    log.info("shutdown_complete")

app = FastAPI(lifespan=lifespan)
```

### 2. State'ten dependency injection

```python
# app/dependencies.py
from fastapi import Request
import httpx

async def get_http_client(request: Request) -> httpx.AsyncClient:
    return request.app.state.http_client

async def get_db_pool(request: Request) -> asyncpg.Pool:
    return request.app.state.db_pool

# Kullanım
@router.get("/traces/{id}")
async def get_trace(
    trace_id: str,
    client: httpx.AsyncClient = Depends(get_http_client),
):
    response = await client.get(f"{settings.tempo_url}/api/traces/{trace_id}")
    ...
```

### 3. Plugin/extension lifespan

```python
# Her client kendi lifespan'ına sahip
@asynccontextmanager
async def tempo_client_lifespan():
    client = TempoClient(base_url=settings.tempo_url)
    await client.connect()
    try:
        yield client
    finally:
        await client.close()

# Ana lifespan içinde kullanım
@asynccontextmanager
async def lifespan(app: FastAPI):
    async with tempo_client_lifespan() as tempo:
        app.state.tempo = tempo
        yield
```

### 4. Health check state entegrasyonu

```python
class StartupState:
    ready: bool = False
    db_connected: bool = False
    tempo_reachable: bool = False

startup_state = StartupState()

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        app.state.db_pool = await create_db_pool(...)
        startup_state.db_connected = True

        await verify_tempo_connection()
        startup_state.tempo_reachable = True

        startup_state.ready = True
    except Exception as e:
        log.critical("startup_failed", error=str(e))
        raise
    yield
    startup_state.ready = False
    # cleanup...

@health_router.get("/ready")
async def readiness():
    if not startup_state.ready:
        raise HTTPException(503, "Service not ready")
    return {"status": "ready"}
```

### 5. Test ortamında lifespan

```python
# tests/conftest.py
@pytest_asyncio.fixture
async def client():
    app = create_app()
    # Lifespan ile birlikte çalıştır
    async with LifespanManager(app) as manager:
        async with AsyncClient(
            transport=ASGITransport(app=manager.app),
            base_url="http://test"
        ) as ac:
            yield ac
```

## Common mistakes

- `@app.on_event("startup")` decorator kullanmak — deprecated, lifespan kullan
- Lifespan'da exception yakalamazsa kaynak sızıntısı — `try/finally` ile cleanup her zaman çalışmalı
- `asyncio.create_task` ile başlatılan task'ları lifespan'da iptal etmemek — zombie task
- `app.state`'e test ortamında erişmeye çalışmak — `LifespanManager` veya `TestClient` lifespan'ı çalıştırmalı

## References
- `skills/fastapi-app-structure`
- `skills/fastapi-health-checks`
- `skills/fastapi-dependency-injection`
