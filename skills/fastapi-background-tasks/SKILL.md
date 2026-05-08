---
name: fastapi-background-tasks
description: "FastAPI BackgroundTasks ve async job queue — Sentinel'de yanıt sonrası asenkron iş yürütme"
---

## Purpose
FastAPI'nin yerleşik `BackgroundTasks` mekanizması, response döndükten sonra yan etkileri (log yazma, metrik gönderme, bildirim) çalıştırır. Ağır veya güvenilirlik gerektiren işler için Celery/ARQ tabanlı kuyruk kullanılır. Sentinel'de alert tetiklendiğinde bildirim gönderme ve trace örnekleme kararları background task olarak işlenir.

## Workflow

### 1. BackgroundTasks — basit kullanım

```python
from fastapi import APIRouter, BackgroundTasks
from app.services.notification_service import send_alert_notification

router = APIRouter()

@router.post("/alerts/{alert_id}/fire")
async def fire_alert(
    alert_id: str,
    background_tasks: BackgroundTasks,
    alert_service: AlertService = Depends(get_alert_service),
):
    alert = await alert_service.fire(alert_id)

    # Response hemen döner, bildirim arka planda gönderilir
    background_tasks.add_task(
        send_alert_notification,
        alert_id=alert_id,
        severity=alert.severity,
        message=alert.message,
    )
    return {"status": "fired", "alert_id": alert_id}
```

### 2. Dependency içinde background task

```python
async def track_usage(
    request: Request,
    background_tasks: BackgroundTasks,
    user: CurrentUser = Depends(get_current_user),
):
    background_tasks.add_task(
        record_api_usage,
        user_id=user.id,
        endpoint=request.url.path,
        method=request.method,
    )
    return user
```

### 3. ARQ ile güvenilir iş kuyruğu

```python
# worker/tasks.py
import arq

async def process_trace_sample(ctx: dict, trace_id: str, sample_rate: float):
    """Tempo'dan trace çeker ve sample kararı verir."""
    tempo = ctx["tempo_client"]
    trace = await tempo.get_trace(trace_id)
    decision = evaluate_sample(trace, sample_rate)
    await ctx["db"].save_sample_decision(trace_id, decision)
    return decision

# worker/main.py
async def startup(ctx: dict):
    ctx["tempo_client"] = TempoClient(settings.tempo_url)
    ctx["db"] = await create_db_pool()

class WorkerSettings:
    functions = [process_trace_sample]
    on_startup = startup
    redis_settings = arq.connections.RedisSettings(host="redis", port=6379)
    max_jobs = 10
    job_timeout = 60
```

### 4. FastAPI → ARQ enqueue

```python
from arq import create_pool
from arq.connections import RedisSettings

@app.on_event("startup")
async def init_arq():
    app.state.arq = await create_pool(RedisSettings(host="redis"))

@router.post("/traces/{trace_id}/analyze")
async def enqueue_analysis(trace_id: str, request: Request):
    await request.app.state.arq.enqueue_job(
        "process_trace_sample",
        trace_id,
        0.1,  # 10% sample rate
    )
    return {"queued": True, "trace_id": trace_id}
```

### 5. Background task hata yönetimi

```python
import structlog

log = structlog.get_logger()

async def safe_send_notification(alert_id: str, **kwargs):
    try:
        await send_alert_notification(alert_id, **kwargs)
    except Exception as exc:
        # Background task exception'ı response'u etkilemez
        # ama loglanmalı
        log.error("notification_failed", alert_id=alert_id, error=str(exc))
        # Retry için kuyruk kullan
        await metrics.increment("notification.failed")
```

## Common mistakes

- `BackgroundTasks`'ı database rollback gerektiren işler için kullanmak — response döndükten sonra DB session kapanır
- ARQ job'larında ctx nesnelerini serialize etmeye çalışmak — sadece primitive değerleri job parametresi olarak geçir
- `add_task` sonrasını await etmeye çalışmak — BackgroundTasks coroutine değil, return değeri yok
- Worker hata loglarını izlememek — ARQ job failure metrikleri Prometheus'a gönderilmeli

## References
- `skills/fastapi-app-structure`
- `skills/fastapi-lifespan`
- `skills/fastapi-observability`
