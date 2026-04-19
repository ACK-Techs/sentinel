---
name: target-app-service-topology
description: gateway → orders → (payments + inventory) + worker servislerinin HTTP kontratları ve inter-service çağrı kuralları.
---

## Purpose
Dört HTTP servisi + bir worker için **endpoint kontratı**, timeout/retry varsayılanları ve trace propagation kurallarını netleştirmek. Topoloji Sentinel'in çoklu-servis korelasyon yeteneğini test etmek için özellikle **paralel downstream**'ler içerir.

## When to Use
- Yeni endpoint eklerken kontrata uyduğunu doğrulamak için.
- Chaos/load senaryosu yazarken hangi path'in tetikleneceğini planlamak için.
- Alarm ve SLO tanımları yaparken (ör. `orders POST /orders` p99 < 500ms).

## Contract / Interface
**gateway** (public ingress; geri kalan hepsi cluster-internal):
- `GET /health` → 200 `{ok:true}`.
- `POST /api/orders` → `orders:/orders`'a forward; body pass-through.
- `GET /work?ms=<int>` → CPU busy loop (load testi için).
- `GET /flaky` → rastgele %30 `500`, %70 `200`.
- `GET /slow` → `asyncio.sleep(2)` sonrası 200.

**orders**:
- `POST /orders` body `{sku, qty}` →
  1. `payments:POST /charge` + `inventory:POST /reserve` **paralel** (`asyncio.gather`).
  2. İkisi de 2xx ise Postgres `orders` tablosuna `INSERT`, `201` döner.
  3. Biri 4xx/5xx ise `502` + compensating log.

**payments**:
- `POST /charge` `{order_id, amount}` → Redis idempotency key `charge:{order_id}` (TTL 10m).
- Chaos state'ine göre latency/error injection.

**inventory**:
- `POST /reserve` `{sku, qty}` → Postgres `SELECT ... FOR UPDATE`; stok yeterliyse `200`, değilse `409`.

**worker**:
- Her 5 saniyede bir `INFO` log + fake iş (`asyncio.sleep`).
- Chaos profili `outage` ise deliberate `ERROR` log/saniye.

Inter-service HTTP: `httpx.AsyncClient(timeout=httpx.Timeout(2.0, connect=0.5))`, 1 retry (sadece connect error), OTEL auto-propagation (`traceparent` header otomatik).

## Implementation Notes
- Paralel çağrı `asyncio.gather(..., return_exceptions=True)` — ilk hata tüm isteği düşürmez, business logic karar verir.
- Retry sadece **idempotent** çağrılar için (inventory reserve idempotent değildir → retry yok).
- Connection pooling: tek `AsyncClient` lifespan boyunca tutulur; per-request yaratmak anti-pattern.
- Client base URL'leri config'ten: `PAYMENTS_URL`, `INVENTORY_URL`, `ORDERS_URL` env.
- Worker FastAPI değildir ama `libs.observability.setup_observability` çağırır + `get_tracer` ile manuel span açar.

## Anti-patterns
1. Paralel downstream'leri `await a; await b` ile **sıralı** çağırmak — Faz-1'in kritik test senaryosu paralel fan-out.
2. `httpx` client'ı her request'te yeni yaratmak — TCP/TLS handshake latency ekler, metrikleri bozar.
3. Non-idempotent endpoint'lere (`/reserve`, `/charge`) retry koymak — double-charge / stok tüketimi.
4. `/health` endpoint'inde DB/Redis ping yapmak — liveness-readiness ayrımı bozulur, restart loop'a girer.
5. Trace propagation için manuel header kopyalamak — `HTTPXClientInstrumentor` zaten halleder; ikisi birden duplicate context yaratır.

## Example Snippet
```python
# services/orders/app/routes/orders.py
import asyncio, httpx
from fastapi import APIRouter, HTTPException
from app.clients import payments_client, inventory_client
from app.db import insert_order

router = APIRouter()

@router.post("/orders", status_code=201)
async def create_order(body: dict):
    sku, qty = body["sku"], body["qty"]
    order_id = body.get("order_id") or _gen_id()
    pay_task = payments_client.post("/charge", json={"order_id": order_id, "amount": body["amount"]})
    inv_task = inventory_client.post("/reserve", json={"sku": sku, "qty": qty})
    pay, inv = await asyncio.gather(pay_task, inv_task, return_exceptions=True)
    for r in (pay, inv):
        if isinstance(r, Exception) or r.status_code >= 400:
            raise HTTPException(502, "downstream failure")
    await insert_order(order_id, sku, qty)
    return {"order_id": order_id}
```
