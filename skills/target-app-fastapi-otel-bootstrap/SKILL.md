---
name: target-app-fastapi-otel-bootstrap
description: Her FastAPI servisinde OTEL auto-instrumentation + custom business metrics için standart bootstrap pattern.
---

## Purpose
FastAPI servislerinin `main.py` dosyasında OTEL'i **doğru sırayla** devreye almak, tüm I/O kütüphanelerini auto-instrument etmek ve kısıtlı sayıda **business metric**'i Meter API üzerinden yayınlamak.

## When to Use
- Yeni servis iskelesi kurulduğunda (`gateway`, `orders`, `payments`, `inventory`).
- Mevcut servise yeni bir client (ör. kafka, grpc) eklendiğinde — ilgili instrumentor burada aktifleştirilir.
- Business counter/histogram eklemek gerektiğinde.

## Contract / Interface
Bootstrap sırası (değiştirilemez):
1. `from libs.observability import setup_observability`
2. `setup_observability("<service>")` — **import edilen router/client'lardan önce**.
3. `FastAPIInstrumentor`, `HTTPXClientInstrumentor`, `SQLAlchemyInstrumentor`, `RedisInstrumentor` çağrıları.
4. `app = FastAPI()` ve route include.

Business metric isimlendirme (OTEL semantic conv ile çakışmayacak, `app.` prefix):
- `app.orders.created` (Counter)
- `app.payments.failed` (Counter, attribute: `reason`)
- `app.http.server.active` (UpDownCounter)
- `app.order.latency` (Histogram, unit=`ms`)

## Implementation Notes
- `FastAPIInstrumentor.instrument_app(app)` **app yaratıldıktan sonra** çağrılır; auto tracer zaten middleware ekler.
- `HTTPXClientInstrumentor().instrument()` global olup tüm `httpx.AsyncClient`'ları kapsar — W3C traceparent propagation otomatik.
- SQLAlchemy için `engine` oluşturulduktan sonra `SQLAlchemyInstrumentor().instrument(engine=engine)`.
- Span attribute'larına **sadece düşük-kardinaliteli** alanlar: `http.route`, `order.status` (enum). `order_id`, `user_id` konmaz.
- Metric attribute kardinalitesi: `reason ∈ {timeout, declined, insufficient_funds, unknown}` gibi kapalı küme.
- `/health` endpoint'inin tracing'den muaf tutulması için `OTEL_PYTHON_FASTAPI_EXCLUDED_URLS=health` env ayarlanır.

## Anti-patterns
1. `setup_observability` çağrısını `@app.on_event("startup")` içine koymak — routerlar zaten import edilmiş olur, enstrümantasyon yarı-çalışır.
2. Her request'te `meter.create_counter(...)` çağırmak — counter bir kere module-scope oluşturulur.
3. Span içinde `span.set_attribute("user_id", uid)` — unbounded cardinality, Tempo/metric dropping'e yol açar.
4. Birden fazla instrumentor'u tekrar tekrar `instrument()` çağırmak (idempotent değildir, duplicate span).
5. `/health`'i exclude etmeyi unutmak — liveness probe'lar trace quota'yı tüketir.

## Example Snippet
```python
# services/orders/app/main.py
from libs.observability import setup_observability, get_meter
setup_observability("orders", service_version="0.3.1")

from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor

from app.routes.orders import router as orders_router
from app.routes.admin_chaos import router as chaos_router
from app.db import engine

app = FastAPI(title="orders")
FastAPIInstrumentor.instrument_app(app, excluded_urls="health")
HTTPXClientInstrumentor().instrument()
SQLAlchemyInstrumentor().instrument(engine=engine)
RedisInstrumentor().instrument()

meter = get_meter("orders")
ORDERS_CREATED = meter.create_counter("app.orders.created", unit="1")
ORDER_LATENCY = meter.create_histogram("app.order.latency", unit="ms")

app.include_router(orders_router)
app.include_router(chaos_router, prefix="/admin")

@app.get("/health")
def health(): return {"ok": True}
```
