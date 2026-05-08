---
name: fastapi-streaming-response
description: "FastAPI StreamingResponse ile büyük veri akışı — Sentinel log/trace export ve bulk query sonuçları için"
---

## Purpose
Büyük trace export'ları veya uzun log sorguları belleğe tamamen yüklenmeden chunk halinde istemciye gönderilmelidir. FastAPI `StreamingResponse` ve async generator kombinezonuyla bellek kısıtlaması olmaksızın GB boyutunda yanıtlar üretilebilir.

## Workflow

### 1. Temel StreamingResponse

```python
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json

router = APIRouter()

async def generate_traces(query: TraceQuery):
    """Trace'leri sayfalayarak async generator olarak üretir."""
    page = 0
    while True:
        batch = await tempo_client.query_traces(query, offset=page * 100, limit=100)
        if not batch:
            break
        for trace in batch:
            yield json.dumps(trace.model_dump()) + "\n"
        page += 1
        await asyncio.sleep(0)  # Event loop'a kontrol ver

@router.get("/traces/export")
async def export_traces(query: TraceQuery = Depends()):
    return StreamingResponse(
        generate_traces(query),
        media_type="application/x-ndjson",
        headers={
            "Content-Disposition": "attachment; filename=traces.ndjson",
            "X-Content-Type-Options": "nosniff",
        },
    )
```

### 2. NDJSON ile structured streaming

```python
async def stream_metric_series(promql: str, start: str, end: str):
    """PromQL range query'yi satır satır akıtır."""
    async with prometheus_client.stream_range(promql, start, end) as stream:
        async for chunk in stream:
            if chunk:
                yield json.dumps({"data": chunk}) + "\n"
```

### 3. ZIP streaming (büyük dosya export)

```python
import zipstream
from fastapi.responses import StreamingResponse

async def export_traces_zip(trace_ids: list[str]):
    zf = zipstream.ZipFile(mode="w", compression=zipstream.ZIP_DEFLATED)

    async def _add_traces():
        for trace_id in trace_ids:
            trace = await tempo_client.get_trace(trace_id)
            data = json.dumps(trace.model_dump(), indent=2).encode()
            zf.write_iter(f"{trace_id}.json", iter([data]))
        yield from zf

    return StreamingResponse(
        _add_traces(),
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=traces.zip"},
    )
```

### 4. Server-Sent Events (SSE)

```python
async def alert_event_stream(org_id: str):
    """Alert olaylarını SSE formatında akıtır."""
    queue = asyncio.Queue()
    await alert_broadcaster.subscribe(org_id, queue)
    try:
        while True:
            try:
                event = await asyncio.wait_for(queue.get(), timeout=30.0)
                yield f"data: {json.dumps(event)}\n\n"
            except asyncio.TimeoutError:
                yield ": heartbeat\n\n"  # keep-alive
    finally:
        await alert_broadcaster.unsubscribe(org_id, queue)

@router.get("/alerts/stream")
async def stream_alerts(
    org_id: str,
    _: CurrentUser = Depends(get_current_user),
):
    return StreamingResponse(
        alert_event_stream(org_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",  # Nginx proxy için
        },
    )
```

### 5. Progress tracking

```python
async def generate_with_progress(items: list):
    total = len(items)
    for i, item in enumerate(items):
        result = await process_item(item)
        yield json.dumps({
            "progress": round((i + 1) / total * 100),
            "item": result,
        }) + "\n"
```

## Common mistakes

- Generator içinde unhandled exception — client bağlantısı kesilir ama hata görünmez; try/except ekle, hata event'i stream et
- `BaseHTTPMiddleware` ile StreamingResponse kombinasyonu — tüm body buffer'a alınır; pure ASGI middleware kullan
- SSE için `X-Accel-Buffering: no` header'ı eklememek — Nginx buffer nedeniyle eventler gecikir
- Async generator'ı `asyncio.sleep(0)` yield etmeden CPU-bound işlemle doldurmak — event loop bloklanır

## References
- `skills/fastapi-websocket`
- `skills/fastapi-middleware`
- `skills/fastapi-observability`
