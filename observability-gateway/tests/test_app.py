from __future__ import annotations

import httpx
from fastapi.testclient import TestClient

from observability_gateway.config import GatewaySettings
from observability_gateway.main import create_app


def test_health_and_status_are_secret_safe() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        if request.url.host == "prometheus":
            assert request.headers["Authorization"] == "Bearer top-secret"
        else:
            assert "Authorization" not in request.headers
        if request.url.path == "/-/ready":
            return httpx.Response(200, text="ready")
        if request.url.path == "/ready":
            return httpx.Response(200, text="ready")
        raise AssertionError(f"Unexpected path: {request.url.path}")

    settings = GatewaySettings.model_validate(
        {
            "prometheus": {"base_url": "http://prometheus:9090", "token_env": "PROM_TOKEN"},
            "loki": {"base_url": "http://loki:3100"},
            "tempo": {"base_url": "http://tempo:3200"},
        }
    )
    app = create_app(
        settings,
        env={
            "PROM_TOKEN": "top-secret",
            "SENTINEL_OBSERVABILITY_GATEWAY_TOKEN": "gateway-secret",
        },
        transport=httpx.MockTransport(handler),
    )
    client = TestClient(app)

    health = client.get("/health", headers={"Authorization": "Bearer gateway-secret"})
    status = client.get("/api/v1/status", headers={"Authorization": "Bearer gateway-secret"})

    assert health.status_code == 200
    assert health.json()["status"] == "ok"
    assert status.status_code == 200
    payload = status.json()
    assert payload["backends"]["prometheus"]["token_present"] is True
    assert "top-secret" not in status.text


def test_gateway_auth_rejects_missing_token_when_configured() -> None:
    app = create_app(
        GatewaySettings(),
        env={"SENTINEL_OBSERVABILITY_GATEWAY_TOKEN": "gateway-secret"},
    )
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 401
    assert response.json() == {
        "error": {
            "backend": "gateway",
            "status": 401,
            "message": "Gateway authentication failed.",
            "retryable": False,
        }
    }


def test_metrics_query_adapts_prometheus_response() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/v1/query"
        assert request.url.params["query"] == "up"
        return httpx.Response(
            200,
            json={
                "status": "success",
                "data": {
                    "resultType": "vector",
                    "result": [
                        {
                            "metric": {"job": "gateway"},
                            "value": [1710000000, "1"],
                        }
                    ],
                },
            },
        )

    app = create_app(
        GatewaySettings.model_validate({"prometheus": {"base_url": "http://prometheus:9090"}}),
        transport=httpx.MockTransport(handler),
    )
    client = TestClient(app)

    response = client.post("/api/v1/metrics/query", json={"query": "up"})

    assert response.status_code == 200
    payload = response.json()
    assert payload["backend"] == "prometheus"
    assert payload["series"][0]["labels"]["job"] == "gateway"
    assert payload["series"][0]["values"][0]["value"] == "1"


def test_loki_errors_use_common_error_model() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/loki/api/v1/query_range"
        assert request.url.params["query"] == '{job="gateway"}'
        return httpx.Response(503, json={"error": "upstream unavailable"})

    app = create_app(
        GatewaySettings.model_validate({"loki": {"base_url": "http://loki:3100"}}),
        transport=httpx.MockTransport(handler),
    )
    client = TestClient(app)

    response = client.post("/api/v1/logs/query_range", json={"service": "gateway"})

    assert response.status_code == 503
    assert response.json() == {
        "error": {
            "backend": "loki",
            "status": 503,
            "message": "upstream unavailable",
            "retryable": True,
        }
    }


def test_trace_detail_normalizes_otlp_payload() -> None:
    async def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/traces/trace-123"
        return httpx.Response(
            200,
            json={
                "resourceSpans": [
                    {
                        "resource": {
                            "attributes": [
                                {
                                    "key": "service.name",
                                    "value": {"stringValue": "orders"},
                                }
                            ]
                        },
                        "scopeSpans": [
                            {
                                "spans": [
                                    {
                                        "spanId": "span-1",
                                        "parentSpanId": "",
                                        "name": "GET /orders",
                                        "startTimeUnixNano": "100",
                                        "endTimeUnixNano": "200",
                                        "attributes": [
                                            {
                                                "key": "http.method",
                                                "value": {"stringValue": "GET"},
                                            }
                                        ],
                                    }
                                ]
                            }
                        ],
                    }
                ]
            },
        )

    app = create_app(
        GatewaySettings.model_validate({"tempo": {"base_url": "http://tempo:3200"}}),
        transport=httpx.MockTransport(handler),
    )
    client = TestClient(app)

    response = client.get("/api/v1/traces/trace-123")

    assert response.status_code == 200
    payload = response.json()
    assert payload["trace"]["trace_id"] == "trace-123"
    assert payload["trace"]["span_count"] == 1
    assert payload["trace"]["services"] == ["orders"]
    assert payload["trace"]["root_span_name"] == "GET /orders"
