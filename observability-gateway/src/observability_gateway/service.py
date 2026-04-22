"""HTTP adapter service for Prometheus, Loki and Tempo."""

from __future__ import annotations

import asyncio
import re
from collections.abc import Mapping
from typing import Any

import httpx

from observability_gateway.config import BackendSettings, GatewaySettings
from observability_gateway.models import (
    BackendStatusModel,
    LogsQueryRangeRequest,
    LogsQueryRangeResponse,
    MetricsQueryRequest,
    MetricsQueryResponse,
    TraceDetail,
    TraceDetailResponse,
    TraceSearchHit,
    TraceSpan,
    TracesSearchRequest,
    TracesSearchResponse,
)

LABEL_PATTERN = re.compile(r'([a-zA-Z0-9_.:-]+)="([^"]*)"')


class BackendRequestError(Exception):
    """Structured backend error used by the API layer."""

    def __init__(self, backend: str, status: int, message: str, retryable: bool) -> None:
        super().__init__(message)
        self.backend = backend
        self.status = status
        self.message = message
        self.retryable = retryable


class ObservabilityService:
    """Read-only adapter around Prometheus, Loki and Tempo APIs."""

    def __init__(
        self,
        settings: GatewaySettings,
        *,
        env: Mapping[str, str] | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self.settings = settings
        self.env = dict(env or {})
        self.transport = transport

    async def status(self) -> dict[str, BackendStatusModel]:
        return {
            "prometheus": await self._probe_backend("prometheus", "/-/ready"),
            "loki": await self._probe_backend("loki", "/ready"),
            "tempo": await self._probe_backend("tempo", "/ready"),
        }

    async def query_metrics(self, request: MetricsQueryRequest) -> MetricsQueryResponse:
        params = {
            "query": request.query,
            "time": request.time,
            "timeout": request.timeout,
            "limit": request.limit,
        }
        payload = await self._request_json("prometheus", "GET", "/api/v1/query", params=params)
        data = payload.get("data", {})
        result = data.get("result", [])
        series: list[dict[str, Any]] = []
        for item in result:
            values = []
            if "value" in item:
                values.append(_sample_point(item["value"]))
            for sample in item.get("values", []):
                values.append(_sample_point(sample))
            series.append({"labels": item.get("metric", {}), "values": values})

        return MetricsQueryResponse(
            query=request.query,
            result_type=str(data.get("resultType", "unknown")),
            series=series,
        )

    async def query_logs(self, request: LogsQueryRangeRequest) -> LogsQueryRangeResponse:
        params = {
            "query": request.query,
            "start": request.start,
            "end": request.end,
            "limit": request.limit,
            "direction": request.direction,
        }
        payload = await self._request_json("loki", "GET", "/loki/api/v1/query_range", params=params)
        data = payload.get("data", {})
        streams = []
        for item in data.get("result", []):
            labels = item.get("stream")
            if isinstance(labels, str):
                labels = _parse_label_string(labels)
            streams.append(
                {
                    "labels": labels or {},
                    "entries": [
                        {"timestamp_ns": str(value[0]), "line": str(value[1])}
                        for value in item.get("values", [])
                    ],
                }
            )

        return LogsQueryRangeResponse(query=request.query, streams=streams)

    async def search_traces(self, request: TracesSearchRequest) -> TracesSearchResponse:
        params = {
            "q": request.query,
            "start": request.start,
            "end": request.end,
            "since": request.since,
            "minDuration": request.min_duration,
            "maxDuration": request.max_duration,
            "limit": request.limit,
            "tags": _logfmt_tags(request.tags),
        }
        payload = await self._request_json("tempo", "GET", "/api/search", params=params)
        traces = []
        for item in payload.get("traces", []):
            traces.append(
                TraceSearchHit(
                    trace_id=str(
                        item.get("traceID") or item.get("traceId") or item.get("id") or ""
                    ),
                    root_service_name=_optional_str(
                        item.get("rootServiceName") or item.get("serviceName")
                    ),
                    root_trace_name=_optional_str(
                        item.get("rootTraceName") or item.get("traceName")
                    ),
                    start_time_unix_nano=_optional_str(
                        item.get("startTimeUnixNano") or item.get("startTime")
                    ),
                    duration_ms=_optional_int(item.get("durationMs")),
                    matched_spans=_optional_int(
                        item.get("spanSetCount") or item.get("matchedSpans")
                    ),
                )
            )
        return TracesSearchResponse(traces=traces)

    async def get_trace(self, trace_id: str) -> TraceDetailResponse:
        payload = await self._request_json("tempo", "GET", f"/api/traces/{trace_id}")
        trace_payload = payload.get("trace", payload)
        spans = _extract_spans(trace_payload)
        services = sorted({span.service_name for span in spans if span.service_name})
        root_span_name = next((span.name for span in spans if not span.parent_span_id), None)
        return TraceDetailResponse(
            trace=TraceDetail(
                trace_id=trace_id,
                span_count=len(spans),
                services=services,
                root_span_name=root_span_name,
                spans=spans,
            )
        )

    async def _probe_backend(self, backend: str, path: str) -> BackendStatusModel:
        backend_settings = self._backend_settings(backend)
        token_present = bool(
            backend_settings.token_env and self.env.get(backend_settings.token_env)
        )
        if not backend_settings.base_url:
            return BackendStatusModel(
                configured=False,
                reachable=None,
                status="skipped",
                message=f"{backend.capitalize()} is not configured.",
                token_present=token_present,
            )

        try:
            await self._request_json(backend, "GET", path, expect_json=False)
        except BackendRequestError as exc:
            return BackendStatusModel(
                configured=True,
                reachable=False,
                status="error",
                message=exc.message,
                token_present=token_present,
            )

        return BackendStatusModel(
            configured=True,
            reachable=True,
            status="ok",
            message=f"{backend.capitalize()} is reachable.",
            token_present=token_present,
        )

    async def _request_json(
        self,
        backend: str,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        expect_json: bool = True,
    ) -> dict[str, Any]:
        backend_settings = self._backend_settings(backend)
        if not backend_settings.base_url:
            raise BackendRequestError(
                backend,
                503,
                f"{backend.capitalize()} is not configured.",
                False,
            )

        url = _join_url(backend_settings.base_url, path)
        headers = _headers_for_backend(backend_settings, self.env)
        retryable_statuses = set(self.settings.http.retry.retryable_status_codes)
        max_attempts = self.settings.http.retry.max_attempts
        last_error: BackendRequestError | None = None

        for attempt in range(1, max_attempts + 1):
            try:
                async with httpx.AsyncClient(
                    timeout=self.settings.http.timeout_sec,
                    transport=self.transport,
                ) as client:
                    filtered_params = {
                        key: value for key, value in (params or {}).items() if value is not None
                    }
                    response = await client.request(
                        method,
                        url,
                        params=filtered_params,
                        headers=headers,
                    )
            except httpx.TimeoutException:
                last_error = BackendRequestError(
                    backend,
                    504,
                    f"{backend.capitalize()} request timed out.",
                    True,
                )
            except httpx.HTTPError as exc:
                last_error = BackendRequestError(
                    backend,
                    502,
                    f"{backend.capitalize()} request failed: {exc.__class__.__name__}.",
                    True,
                )
            else:
                if response.status_code >= 400:
                    last_error = BackendRequestError(
                        backend,
                        response.status_code,
                        _backend_error_message(backend, response),
                        response.status_code in retryable_statuses,
                    )
                elif not expect_json:
                    return {"ok": True}
                else:
                    try:
                        return response.json()
                    except ValueError as exc:
                        raise BackendRequestError(
                            backend,
                            502,
                            f"{backend.capitalize()} returned invalid JSON.",
                            False,
                        ) from exc

            if last_error is None:
                continue
            if attempt >= max_attempts or not last_error.retryable:
                break
            delay = self.settings.http.retry.backoff_base_sec * (2 ** (attempt - 1))
            await asyncio.sleep(delay)

        assert last_error is not None
        raise last_error

    def _backend_settings(self, backend: str) -> BackendSettings:
        if backend == "prometheus":
            return self.settings.prometheus
        if backend == "loki":
            return self.settings.loki
        if backend == "tempo":
            return self.settings.tempo
        raise ValueError(f"Unsupported backend: {backend}")


def _backend_error_message(backend: str, response: httpx.Response) -> str:
    if response.status_code in {401, 403}:
        return f"{backend.capitalize()} authentication failed."

    try:
        payload = response.json()
    except ValueError:
        return f"{backend.capitalize()} returned HTTP {response.status_code}."

    for key in ("error", "message"):
        value = payload.get(key)
        if isinstance(value, str) and value:
            return value[:160]
    return f"{backend.capitalize()} returned HTTP {response.status_code}."


def _headers_for_backend(settings: BackendSettings, env: Mapping[str, str]) -> dict[str, str]:
    if not settings.token_env:
        return {}

    token = env.get(settings.token_env)
    if not token:
        return {}
    return {"Authorization": f"Bearer {token}"}


def _join_url(base_url: str, path: str) -> str:
    normalized_path = path if path.startswith("/") else f"/{path}"
    return f"{base_url.rstrip('/')}{normalized_path}"


def _sample_point(sample: list[Any]) -> dict[str, Any]:
    return {
        "unix_sec": float(sample[0]),
        "value": str(sample[1]),
    }


def _parse_label_string(value: str) -> dict[str, str]:
    return {match.group(1): match.group(2) for match in LABEL_PATTERN.finditer(value)}


def _logfmt_tags(tags: Mapping[str, str]) -> str | None:
    if not tags:
        return None

    pairs = []
    for key, value in tags.items():
        escaped = value.replace('"', '\\"')
        if " " in escaped:
            escaped = f'"{escaped}"'
        pairs.append(f"{key}={escaped}")
    return " ".join(pairs)


def _extract_spans(payload: dict[str, Any]) -> list[TraceSpan]:
    resource_spans = payload.get("resourceSpans", [])
    spans: list[TraceSpan] = []
    for resource_span in resource_spans:
        resource_attributes = _attributes_to_dict(
            resource_span.get("resource", {}).get("attributes", [])
        )
        scope_spans = resource_span.get("scopeSpans") or resource_span.get(
            "instrumentationLibrarySpans", []
        )
        for scope_span in scope_spans:
            for span in scope_span.get("spans", []):
                span_attributes = _attributes_to_dict(span.get("attributes", []))
                spans.append(
                    TraceSpan(
                        span_id=_optional_str(span.get("spanId")),
                        parent_span_id=_optional_str(span.get("parentSpanId")),
                        name=_optional_str(span.get("name")),
                        service_name=_optional_str(resource_attributes.get("service.name")),
                        start_time_unix_nano=_optional_str(span.get("startTimeUnixNano")),
                        end_time_unix_nano=_optional_str(span.get("endTimeUnixNano")),
                        attributes=span_attributes,
                    )
                )
    return spans


def _attributes_to_dict(items: list[dict[str, Any]]) -> dict[str, str]:
    attributes: dict[str, str] = {}
    for item in items:
        key = item.get("key")
        value = item.get("value", {})
        if not key:
            continue
        attributes[str(key)] = _attribute_value(value)
    return attributes


def _attribute_value(value: dict[str, Any]) -> str:
    for key in (
        "stringValue",
        "boolValue",
        "intValue",
        "doubleValue",
        "bytesValue",
    ):
        if key in value:
            return str(value[key])
    return ""


def _optional_str(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value)
    return text or None


def _optional_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None
