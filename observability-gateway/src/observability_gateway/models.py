"""Request, response and error models for the observability gateway."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field


class ErrorModel(BaseModel):
    """Secret-safe backend error surface."""

    model_config = ConfigDict(extra="forbid")

    backend: Literal["gateway", "prometheus", "loki", "tempo"]
    status: int
    message: str
    retryable: bool


class ErrorResponse(BaseModel):
    """Envelope for error responses."""

    model_config = ConfigDict(extra="forbid")

    error: ErrorModel


class HealthResponse(BaseModel):
    """Basic service liveness response."""

    model_config = ConfigDict(extra="forbid")

    status: Literal["ok"] = "ok"
    service: str
    version: str


class BackendStatusModel(BaseModel):
    """Backend readiness summary."""

    model_config = ConfigDict(extra="forbid")

    configured: bool
    reachable: bool | None = None
    status: str
    message: str
    token_present: bool = False


class StatusResponse(BaseModel):
    """Gateway status response."""

    model_config = ConfigDict(extra="forbid")

    service: str
    version: str
    http: dict[str, Any]
    backends: dict[str, BackendStatusModel]


class MetricsQueryRequest(BaseModel):
    """Prometheus instant query request."""

    model_config = ConfigDict(extra="forbid")

    query: str
    time: str | None = None
    timeout: str | None = None
    limit: int | None = Field(default=None, ge=1)


class LogsQueryRangeRequest(BaseModel):
    """Loki range query request."""

    model_config = ConfigDict(extra="forbid")

    query: str
    start: str | None = None
    end: str | None = None
    limit: int = Field(default=100, ge=1, le=5000)
    direction: Literal["backward", "forward"] = "backward"


class TracesSearchRequest(BaseModel):
    """Tempo trace search request."""

    model_config = ConfigDict(extra="forbid")

    query: str | None = None
    start: str | None = None
    end: str | None = None
    since: str | None = None
    min_duration: str | None = None
    max_duration: str | None = None
    limit: int = Field(default=20, ge=1, le=500)
    tags: dict[str, str] = Field(default_factory=dict)


class MetricsSeriesPoint(BaseModel):
    """A normalized Prometheus sample."""

    model_config = ConfigDict(extra="forbid")

    unix_sec: float
    value: str


class MetricsSeries(BaseModel):
    """A normalized Prometheus series."""

    model_config = ConfigDict(extra="forbid")

    labels: dict[str, str]
    values: list[MetricsSeriesPoint]


class MetricsQueryResponse(BaseModel):
    """Backend-independent metric query response."""

    model_config = ConfigDict(extra="forbid")

    backend: Literal["prometheus"] = "prometheus"
    query: str
    result_type: str
    series: list[MetricsSeries]


class LogEntry(BaseModel):
    """A normalized Loki log entry."""

    model_config = ConfigDict(extra="forbid")

    timestamp_ns: str
    line: str


class LogStream(BaseModel):
    """A normalized Loki log stream."""

    model_config = ConfigDict(extra="forbid")

    labels: dict[str, str]
    entries: list[LogEntry]


class LogsQueryRangeResponse(BaseModel):
    """Backend-independent log query response."""

    model_config = ConfigDict(extra="forbid")

    backend: Literal["loki"] = "loki"
    query: str
    streams: list[LogStream]


class TraceSearchHit(BaseModel):
    """A normalized Tempo search hit."""

    model_config = ConfigDict(extra="forbid")

    trace_id: str
    root_service_name: str | None = None
    root_trace_name: str | None = None
    start_time_unix_nano: str | None = None
    duration_ms: int | None = None
    matched_spans: int | None = None


class TracesSearchResponse(BaseModel):
    """Backend-independent trace search response."""

    model_config = ConfigDict(extra="forbid")

    backend: Literal["tempo"] = "tempo"
    traces: list[TraceSearchHit]


class TraceSpan(BaseModel):
    """A normalized span view extracted from Tempo."""

    model_config = ConfigDict(extra="forbid")

    span_id: str | None = None
    parent_span_id: str | None = None
    name: str | None = None
    service_name: str | None = None
    start_time_unix_nano: str | None = None
    end_time_unix_nano: str | None = None
    attributes: dict[str, str] = Field(default_factory=dict)


class TraceDetail(BaseModel):
    """A normalized trace detail payload."""

    model_config = ConfigDict(extra="forbid")

    trace_id: str
    span_count: int
    services: list[str]
    root_span_name: str | None = None
    spans: list[TraceSpan]


class TraceDetailResponse(BaseModel):
    """Backend-independent trace detail response."""

    model_config = ConfigDict(extra="forbid")

    backend: Literal["tempo"] = "tempo"
    trace: TraceDetail
