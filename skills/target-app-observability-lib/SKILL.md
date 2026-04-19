---
name: target-app-observability-lib
description: libs/observability paylaşılan paketi — OTEL SDK kurulumu (traces+metrics+logs) OTLP/gRPC push ile, tek setup_observability() entrypoint.
---

## Purpose
Tüm servislerin **aynı semantic convention** ile OTEL SDK kurmasını sağlamak. `prometheus_client` yok, scrape yok — yalnız **OTLP/gRPC push** kullanılır. Loglara `trace_id` / `span_id` enjekte edilir ki Loki/Tempo korelasyonu mümkün olsun.

## When to Use
- Her yeni FastAPI servisinin ilk satırlarında.
- Worker gibi non-FastAPI Python prosesleri başlarken.
- Özel Meter/Tracer ihtiyacı çıktığında (business metric: `orders_created_total`).

## Contract / Interface
Public API:
```python
def setup_observability(
    service_name: str,
    service_version: str = "0.1.0",
    environment: str | None = None,  # defaults to env DEPLOYMENT_ENV
) -> None
def get_tracer(name: str) -> Tracer
def get_meter(name: str) -> Meter
```
Ortam değişkenleri (okunur, yazılmaz):
- `OTEL_EXPORTER_OTLP_ENDPOINT` (zorunlu; ör. `http://otel-collector.sentinel.svc:4317`)
- `OTEL_SERVICE_NAME`, `OTEL_RESOURCE_ATTRIBUTES` (opsiyonel override)
- `DEPLOYMENT_ENV` (ör. `dev`, `staging`)

Resource attributes (her zaman set edilir):
`service.name`, `service.version`, `deployment.environment`, `service.instance.id` (hostname).

## Implementation Notes
- **Üç provider**: `TracerProvider`, `MeterProvider` (PeriodicExportingMetricReader, 15s), `LoggerProvider`.
- Exporter: `OTLPSpanExporter` / `OTLPMetricExporter` / `OTLPLogExporter` (gRPC, insecure).
- `LoggingInstrumentor().instrument(set_logging_format=True)` → stdlib `logging` kayıtlarına `otelTraceID` / `otelSpanID` enjekte.
- structlog kullanılıyorsa `merge_contextvars` + custom processor ile trace_id eklenir.
- Idempotent: tekrar çağrılırsa no-op (global flag).
- Sampling: `ParentBased(TraceIdRatioBased(0.1))` varsayılan; env `OTEL_TRACES_SAMPLER_ARG` ile override.

## Anti-patterns
1. `prometheus_client` veya `/metrics` endpoint eklemek — Faz-1'de **tamamen yasak**, sadece OTLP push.
2. `setup_observability` çağrısını FastAPI startup event'te yapmak — import edilen modüller (routers) instrumentor'dan önce yüklenir ve yarı-enstrümante olur. **Her zaman `main.py`'nin en üstünde**, import'lardan hemen sonra.
3. Span attribute olarak `user.id`, `order.id`, `session.id` gibi **unbounded / PII** alanları koymak — cardinality patlamasına yol açar.
4. Her servisin kendi `TracerProvider`'ını set etmesi yerine global'i override etmek — double-export.
5. Log exporter'ı ekleyip stdlib logging'e handler bağlamamak — trace-log korelasyonu kopar.

## Example Snippet
```python
# libs/observability/setup.py
import logging, os, socket
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor

_READY = False

def setup_observability(service_name: str, service_version: str = "0.1.0",
                        environment: str | None = None) -> None:
    global _READY
    if _READY: return
    res = Resource.create({
        "service.name": service_name,
        "service.version": service_version,
        "deployment.environment": environment or os.getenv("DEPLOYMENT_ENV", "dev"),
        "service.instance.id": socket.gethostname(),
    })
    tp = TracerProvider(resource=res)
    tp.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(insecure=True)))
    trace.set_tracer_provider(tp)
    mp = MeterProvider(resource=res, metric_readers=[
        PeriodicExportingMetricReader(OTLPMetricExporter(insecure=True), export_interval_millis=15000)
    ])
    metrics.set_meter_provider(mp)
    lp = LoggerProvider(resource=res)
    lp.add_log_record_processor(BatchLogRecordProcessor(OTLPLogExporter(insecure=True)))
    logging.getLogger().addHandler(LoggingHandler(logger_provider=lp))
    LoggingInstrumentor().instrument(set_logging_format=True)
    _READY = True
```
