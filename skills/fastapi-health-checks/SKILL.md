---
name: fastapi-health-checks
description: "FastAPI health, readiness ve liveness endpoint tasarımı — Kubernetes probe'ları için Sentinel servis sağlık kontrolleri"
---

## Purpose
Kubernetes liveness ve readiness probe'ları farklı soruları yanıtlar: "uygulama çalışıyor mu?" vs "trafik alabilecek durumda mı?". Sentinel'de her servis üç endpoint açar: `/health` (liveness), `/ready` (readiness), `/startup` (startup probe). Readiness upstream bağımlılıkları da kontrol eder.

## Workflow

### 1. Health endpoint modelleri

```python
# app/models/health.py
from enum import Enum
from pydantic import BaseModel

class HealthStatus(str, Enum):
    healthy = "healthy"
    degraded = "degraded"
    unhealthy = "unhealthy"

class ComponentHealth(BaseModel):
    name: str
    status: HealthStatus
    latency_ms: float | None = None
    error: str | None = None

class HealthResponse(BaseModel):
    status: HealthStatus
    version: str
    uptime_seconds: float
    components: list[ComponentHealth] = []
```

### 2. Health check router

```python
# app/api/health.py
import time
from fastapi import APIRouter, Response
from app.models.health import HealthResponse, ComponentHealth, HealthStatus
from app.state import startup_time

health_router = APIRouter(tags=["Health"])

@health_router.get("/health", response_model=dict)
async def liveness():
    """Kubernetes liveness probe — uygulama çalışıyor mu?"""
    return {"status": "alive"}

@health_router.get("/ready", response_model=HealthResponse)
async def readiness(response: Response):
    """Kubernetes readiness probe — trafik alabilir mi?"""
    checks = await run_readiness_checks()

    overall = HealthStatus.healthy
    if any(c.status == HealthStatus.unhealthy for c in checks):
        overall = HealthStatus.unhealthy
        response.status_code = 503
    elif any(c.status == HealthStatus.degraded for c in checks):
        overall = HealthStatus.degraded

    return HealthResponse(
        status=overall,
        version=settings.app_version,
        uptime_seconds=time.time() - startup_time,
        components=checks,
    )

@health_router.get("/startup")
async def startup_probe():
    """Kubernetes startup probe — ilk başlatma tamamlandı mı?"""
    if not startup_state.ready:
        return Response(status_code=503, content="Starting up...")
    return {"status": "started"}
```

### 3. Bağımlılık sağlık kontrolleri

```python
import httpx
import asyncpg

async def run_readiness_checks() -> list[ComponentHealth]:
    checks = await asyncio.gather(
        check_tempo(),
        check_prometheus(),
        check_db(),
        return_exceptions=True,
    )
    return [c if isinstance(c, ComponentHealth) else ComponentHealth(
        name="unknown", status=HealthStatus.unhealthy, error=str(c)
    ) for c in checks]

async def check_tempo() -> ComponentHealth:
    start = time.perf_counter()
    try:
        async with httpx.AsyncClient(timeout=2.0) as client:
            r = await client.get(f"{settings.tempo_url}/ready")
            r.raise_for_status()
        return ComponentHealth(
            name="tempo",
            status=HealthStatus.healthy,
            latency_ms=(time.perf_counter() - start) * 1000,
        )
    except Exception as e:
        return ComponentHealth(name="tempo", status=HealthStatus.unhealthy, error=str(e))

async def check_db() -> ComponentHealth:
    start = time.perf_counter()
    try:
        async with app.state.db_pool.acquire() as conn:
            await conn.fetchval("SELECT 1")
        return ComponentHealth(
            name="postgres",
            status=HealthStatus.healthy,
            latency_ms=(time.perf_counter() - start) * 1000,
        )
    except Exception as e:
        return ComponentHealth(name="postgres", status=HealthStatus.unhealthy, error=str(e))
```

### 4. Kubernetes probe konfigürasyonu

```yaml
# deployment.yaml
livenessProbe:
  httpGet:
    path: /health
    port: 8000
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3

readinessProbe:
  httpGet:
    path: /ready
    port: 8000
  initialDelaySeconds: 10
  periodSeconds: 15
  failureThreshold: 2

startupProbe:
  httpGet:
    path: /startup
    port: 8000
  failureThreshold: 30
  periodSeconds: 5
```

## Common mistakes

- Liveness probe'dan upstream bağımlılık kontrol etmek — upstream geçici bağlanamıyorsa pod restart loop'a girer
- Readiness check için timeout koymamak — yavaş upstream yanıtı probe timeout'a neden olur, pod trafik almayı durdurur
- `/ready` endpoint'ini auth middleware'in arkasına koymak — Kubernetes probe token kullanmaz, auth bypass gerekli
- `degraded` durumda 200 dönmek — Kubernetes sadece 2xx'e readiness verir; degraded için 503 dön veya özel davranış tanımla

## References
- `skills/fastapi-lifespan`
- `skills/fastapi-observability`
- `skills/fastapi-app-structure`
