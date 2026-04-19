---
name: target-app-chaos-api
description: Per-servis /admin/chaos endpoint + middleware ile runtime hata/latency enjeksiyonu; ConfigMap watch ile profil reload.
---

## Purpose
Sentinel'in anomali tespitini **kontrollü, tekrar-edilebilir** şekilde tetiklemek. Her servis cluster-internal bir `/admin/chaos` endpoint'i üzerinden canlı olarak hata oranı, latency, CPU yanma, DB yavaşlatma gibi parametreleri değiştirebilir.

## When to Use
- Scenario runner senaryo başlatırken profili push ederken.
- Manual debug / A-B test sırasında.
- CI'da chaos middleware'inin kendisinin regresyonunu doğrulamak için.

## Contract / Interface
State (process-global, thread-safe `Lock`):
```json
{
  "error_rate": 0.0,            // 0..1
  "latency_p50_ms": 0,
  "latency_p99_ms": 0,
  "cpu_burn": 0.0,              // fraction of requests that busy-loop N ms
  "memory_leak": false,         // append to a global list
  "db_slow": 0,                 // ms injected before DB call
  "downstream_timeout": false   // make httpx calls timeout
}
```
Endpoints (prefix `/admin`, NetworkPolicy ile dışa kapalı):
- `GET /admin/chaos` → current state.
- `POST /admin/chaos` body = partial state patch → merge + return new state.
- `POST /admin/chaos/profile` body `{"profile":"degraded"}` → named profile set.
- `POST /admin/chaos/reload` → ConfigMap'ten tekrar oku.

Named profiller:
- `normal`: tüm değerler sıfır.
- `degraded`: `error_rate=0.05`, `latency_p99_ms=800`.
- `outage`: `error_rate=0.9`, `downstream_timeout=true`.
- `slow-burn`: `latency_p50_ms=50`, `latency_p99_ms=1500`, `cpu_burn=0.1`.
- `spike`: 60 saniyelik `error_rate=0.5`, sonra `normal`'e döner (async task).

## Implementation Notes
- **Middleware**: her request'te (i) random < `error_rate` → `503` döner (ii) `latency_p50_ms`/`p99_ms` ile numpy.random bimodal sleep (iii) `cpu_burn` fraction için `while time < N: pass`.
- DB slow: SQLAlchemy `before_cursor_execute` event listener `db_slow > 0` ise `time.sleep`.
- ConfigMap `/etc/chaos/profile.yaml` olarak mount; `inotify` veya 5s polling loop ile reload.
- State değişiklikleri OTEL span event'i olarak log'lanır (`chaos.profile.changed`) — böylece Sentinel ground-truth'u trace'ten de çıkarabilir.
- `/admin/*` route'ları OTEL'de ayrı span name'i ile görünür; metric cardinality için `http.route` attribute set edilir.
- Kubernetes NetworkPolicy: sadece `namespace=sentinel-target` içinden DNS + scenario-runner pod'una izin.

## Anti-patterns
1. `/admin/chaos`'u public ingress (gateway) üzerinden expose etmek — yanlışlıkla dış dünya tetikler.
2. `error_rate` veya latency'yi **sadece business route'lara** uygulamak — middleware tüm path'lere uygulanmalı ki `/health` bile etkilensin (readiness fail → gerçekçi outage).
3. Chaos state'i her request'te ConfigMap'ten re-read etmek — IO overhead; watch/polling + in-memory cache kullan.
4. `cpu_burn` için `asyncio.sleep` — event loop'u bloklamaz, CPU metriklerini etkilemez; **senkron** busy loop şart.
5. Profile transition'ı OTEL'e yazmamak — ground-truth sadece scenario-runner log'una bağımlı kalır, trace korelasyonu kaybolur.

## Example Snippet
```python
# services/common/chaos.py
import asyncio, random, time, threading
from fastapi import Request, Response
from opentelemetry import trace

_tracer = trace.get_tracer("chaos")
_state = {"error_rate": 0.0, "latency_p50_ms": 0, "latency_p99_ms": 0,
          "cpu_burn": 0.0, "db_slow": 0, "downstream_timeout": False}
_lock = threading.Lock()

def get_state(): 
    with _lock: return dict(_state)

def set_state(patch: dict):
    with _lock:
        _state.update(patch)
        span = trace.get_current_span()
        span.add_event("chaos.profile.changed", attributes={k: str(v) for k, v in patch.items()})
        return dict(_state)

async def chaos_middleware(request: Request, call_next):
    s = get_state()
    if random.random() < s["error_rate"]:
        return Response("chaos:error", status_code=503)
    lat = s["latency_p99_ms"] if random.random() < 0.01 else s["latency_p50_ms"]
    if lat: await asyncio.sleep(lat / 1000)
    if random.random() < s["cpu_burn"]:
        end = time.time() + 0.05
        while time.time() < end: pass  # sync burn
    return await call_next(request)
```
