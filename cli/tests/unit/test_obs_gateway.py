from __future__ import annotations

import json

import httpx
import pytest

import sentinel_cli.cli.app as app
from sentinel_cli.cli.app import main
from sentinel_cli.config.models import ObservabilityGatewaySettings
from sentinel_cli.observability.gateway import GatewayClient, check_gateway_connection


def test_gateway_health_check_ok() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/health"
        assert request.headers["Authorization"] == "Bearer secret-token"
        return httpx.Response(200, json={"status": "ok"})

    result = check_gateway_connection(
        ObservabilityGatewaySettings(
            enabled=True,
            base_url="https://gateway.example.test",
            token_env="GW_TOKEN",
        ),
        env={"GW_TOKEN": "secret-token"},
        transport=httpx.MockTransport(handler),
    )

    assert result.ok is True
    assert result.status == "ok"
    assert result.token_present is True


def test_gateway_client_uses_secret_safe_error_message() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            503,
            json={
                "error": {
                    "backend": "loki",
                    "status": 503,
                    "message": "upstream unavailable",
                    "retryable": True,
                }
            },
        )

    client = GatewayClient(
        ObservabilityGatewaySettings(base_url="https://gateway.example.test"),
        env={},
        transport=httpx.MockTransport(handler),
    )

    with pytest.raises(Exception, match="upstream unavailable"):
        client.query_logs(service="gateway")


def test_obs_metric_command_uses_gateway_client(monkeypatch, capsys) -> None:
    class FakeGatewayClient:
        def __init__(self, settings, *, env):
            assert settings.base_url == "http://gateway.example.test"
            assert env["SENTINEL_OBSERVABILITY_GATEWAY_TOKEN"] == "secret"

        def query_metric(self, query: str) -> dict[str, object]:
            assert query == "up"
            return {"backend": "prometheus", "query": query, "series": []}

    monkeypatch.setattr(app, "GatewayClient", FakeGatewayClient)
    monkeypatch.setenv("SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL", "http://gateway.example.test")
    monkeypatch.setenv("SENTINEL_OBSERVABILITY_GATEWAY_TOKEN", "secret")

    code = main(["obs", "metric", "up"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert code == 0
    assert payload["backend"] == "prometheus"
    assert payload["query"] == "up"
    assert "secret" not in captured.out


def test_obs_logs_command_sends_service_to_gateway(monkeypatch, capsys) -> None:
    class FakeGatewayClient:
        def __init__(self, settings, *, env):
            del settings, env

        def query_logs(self, *, service: str | None, query: str | None, limit: int) -> dict[str, object]:
            assert service == "gateway"
            assert query is None
            assert limit == 20
            return {"backend": "loki", "query": "gateway-managed-query", "streams": []}

    monkeypatch.setattr(app, "GatewayClient", FakeGatewayClient)
    monkeypatch.setenv("SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL", "http://gateway.example.test")

    code = main(["obs", "logs", "--service", "gateway"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert code == 0
    assert payload["backend"] == "loki"
    assert payload["query"] == "gateway-managed-query"


def test_gateway_client_sends_service_without_loki_syntax() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["service"] == "gateway"
        assert payload["query"] is None
        return httpx.Response(200, json={"backend": "loki", "query": "gateway-managed-query"})

    client = GatewayClient(
        ObservabilityGatewaySettings(base_url="https://gateway.example.test"),
        env={},
        transport=httpx.MockTransport(handler),
    )

    payload = client.query_logs(service="gateway")

    assert payload["query"] == "gateway-managed-query"


def test_obs_traces_command_builds_service_search(monkeypatch, capsys) -> None:
    class FakeGatewayClient:
        def __init__(self, settings, *, env):
            del settings, env

        def search_traces(
            self,
            *,
            service: str | None,
            query: str | None,
            limit: int,
        ) -> dict[str, object]:
            assert service == "orders"
            assert query is None
            assert limit == 20
            return {"backend": "tempo", "traces": [{"trace_id": "trace-1"}]}

    monkeypatch.setattr(app, "GatewayClient", FakeGatewayClient)
    monkeypatch.setenv("SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL", "http://gateway.example.test")

    code = main(["obs", "traces", "--service", "orders"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert code == 0
    assert payload["backend"] == "tempo"
    assert payload["traces"][0]["trace_id"] == "trace-1"
