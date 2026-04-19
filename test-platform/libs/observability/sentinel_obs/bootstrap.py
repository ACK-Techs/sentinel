from __future__ import annotations

import logging
import os
import socket
import sys
from threading import Lock

from opentelemetry import metrics, trace
from opentelemetry._logs import set_logger_provider
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.logging import LoggingInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

_READY = False
_LOCK = Lock()


def _required_endpoint() -> str:
    endpoint = os.getenv("OTEL_EXPORTER_OTLP_ENDPOINT")
    if not endpoint:
        print("OTEL_EXPORTER_OTLP_ENDPOINT is required", file=sys.stderr)
        raise SystemExit(1)
    os.environ["OTEL_EXPORTER_OTLP_PROTOCOL"] = "grpc"
    return endpoint


def init_telemetry(
    service_name: str,
    service_version: str = "0.1.0",
    environment: str | None = None,
) -> None:
    global _READY
    with _LOCK:
        if _READY:
            return

        endpoint = _required_endpoint()
        environment_value = environment or os.getenv("DEPLOYMENT_ENV", "dev") or "dev"
        resource = Resource.create(
            {
                "service.name": service_name,
                "service.version": service_version,
                "deployment.environment": environment_value,
                "service.instance.id": socket.gethostname(),
            }
        )

        tracer_provider = TracerProvider(resource=resource)
        tracer_provider.add_span_processor(
            BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True))
        )
        trace.set_tracer_provider(tracer_provider)

        reader = PeriodicExportingMetricReader(
            OTLPMetricExporter(endpoint=endpoint, insecure=True),
            export_interval_millis=15000,
        )
        metrics.set_meter_provider(MeterProvider(resource=resource, metric_readers=[reader]))

        logger_provider = LoggerProvider(resource=resource)
        logger_provider.add_log_record_processor(
            BatchLogRecordProcessor(OTLPLogExporter(endpoint=endpoint, insecure=True))
        )
        set_logger_provider(logger_provider)
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.INFO)
        root_logger.addHandler(LoggingHandler(level=logging.INFO, logger_provider=logger_provider))
        LoggingInstrumentor().instrument(set_logging_format=True)
        _READY = True


def get_tracer(name: str):
    return trace.get_tracer(name)


def get_meter(name: str):
    return metrics.get_meter(name)
