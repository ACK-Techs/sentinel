---
name: fastapi-observability
description: "FastAPI OpenTelemetry enstrümantasyonu ve Prometheus metrikleri — Sentinel gateway'in tam observability entegrasyonu"
---

## Purpose
Sentinel'in gateway servisi hem trace (OpenTelemetry → Tempo) hem de metrik (Prometheus) üretir. Bu skill otomatik enstrümantasyon, span enrichment, custom metrik tanımları ve Grafana dashboard için gerekli label stratejisini kapsar.

## Workflow

### 1. OpenTelemetry kurulumu

```python
# app/observability.py
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.sdk.resources import Resource

def setup_tracing(service_name: str, otlp_endpoint: str) -> None:
    resource = Resource.create({
        "service.name": service_name,
        "service.version": settings.app_version,
        "deployment.environment": settings.environment,
    })

    provider = TracerProvider(resource=resource)
    exporter = OTLPSpanExporter(endpoint=otlp_endpoint, insecure=True)
    provider.add_span_processor(BatchSpanProcessor(exporter))
    trace.set_tracer_provider(provider)

    FastAPIInstrumentor.instrument(
        tracer_provider=provider,
        excluded_urls="health,ready,metrics",
    )
    HTTPXClientInstrumentor().instrument(tracer_provider=provider)
```

### 2. Prometheus metrikleri

```python
# app/metrics.py
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import APIRouter, Response

REQUEST_COUNT = Counter(
    "sentinel_gateway_requests_total",
    "Toplam HTTP istek sayısı",
    labelnames=["method", "path", "status_code"],
)

REQUEST_DURATION = Histogram(
    "sentinel_gateway_request_duration_seconds",
    "HTTP istek süresi dağılımı",
    labelnames=["method", "path"],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5, 5.0],
)

ACTIVE_CONNECTIONS = Gauge(
    "sentinel_gateway_active_connections",
    "Anlık aktif bağlantı sayısı",
)

UPSTREAM_LATENCY = Histogram(
    "sentinel_upstream_latency_seconds",
    "Upstream servis latency",
    labelnames=["service"],
)

metrics_router = APIRouter()

@metrics_router.get("/metrics")
async def prometheus_metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
```

### 3. Manuel span enrichment

```python
from opentelemetry import trace

tracer = trace.get_tracer("sentinel.gateway")

async def get_trace_with_span(trace_id: str):
    with tracer.start_as_current_span("tempo.get_trace") as span:
        span.set_attribute("trace.id", trace_id)
        span.set_attribute("upstream.service", "tempo")

        start = time.perf_counter()
        try:
            result = await tempo_client.get_trace(trace_id)
            span.set_attribute("trace.span_count", len(result.spans))
            return result
        except Exception as e:
            span.record_exception(e)
            span.set_status(trace.StatusCode.ERROR, str(e))
            raise
        finally:
            UPSTREAM_LATENCY.labels(service="tempo").observe(time.perf_counter() - start)
```

### 4. Middleware ile otomatik metrik toplama

```python
import time
from starlette.middleware.base import BaseHTTPMiddleware

class MetricsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        ACTIVE_CONNECTIONS.inc()
        start = time.perf_counter()
        try:
            response = await call_next(request)
            REQUEST_COUNT.labels(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
            ).inc()
            REQUEST_DURATION.labels(
                method=request.method,
                path=request.url.path,
            ).observe(time.perf_counter() - start)
            return response
        finally:
            ACTIVE_CONNECTIONS.dec()
```

## Common mistakes

- `excluded_urls` olmadan health endpoint'leri enstrümanlamak — Prometheus scrape trace doldurur
- OTLP endpoint'ini `http://` prefix ile gRPC exporter'a vermek — gRPC `host:port` formatı bekler
- `BatchSpanProcessor` yerine `SimpleSpanProcessor` production'da kullanmak — her span network round-trip yapar
- Metrik label'larında yüksek kardinalite — `path=/traces/abc123` yerine `path=/traces/{id}` kullan

## References
- `skills/fastapi-middleware`
- `skills/cos-deploy-tempo`
- `skills/cos-deploy-prometheus`
- `skills/fastapi-health-checks`
