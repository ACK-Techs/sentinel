from __future__ import annotations

import os

import pytest

from sentinel_cli.config.models import ObservabilityGatewaySettings
from sentinel_cli.observability.gateway import GatewayClientError
from sentinel_cli.tools.base import ToolContext
from sentinel_cli.tools.observability import (
    ObsLogsQueryTool,
    ObsMetricQueryTool,
    ObsTraceGetTool,
    ObsTracesSearchTool,
)


@pytest.fixture
def tool_context(tmp_path):
    return ToolContext(
        cwd=str(tmp_path),
        session_id="sess",
        interactive=False,
        auto_approve=True,
    )


@pytest.fixture
def gateway_settings():
    return ObservabilityGatewaySettings(base_url="https://gateway.example.test")


def test_metric_tool_returns_gateway_payload(monkeypatch: pytest.MonkeyPatch, gateway_settings, tool_context) -> None:
    class FakeClient:
        def __init__(self, settings, *, env):
            assert settings.base_url == "https://gateway.example.test"
            assert isinstance(env, dict)

        def query_metric(self, query: str):
            assert query == "up"
            return {"backend": "prometheus", "query": query, "series": []}

    monkeypatch.setattr("sentinel_cli.tools.observability.GatewayClient", FakeClient)
    tool = ObsMetricQueryTool(gateway_settings)
    args = tool.args_model(query="up")

    result = tool.execute(args, tool_context)

    assert result.ok is True
    assert result.data == {"backend": "prometheus", "query": "up", "series": []}


def test_logs_tool_maps_gateway_errors(monkeypatch: pytest.MonkeyPatch, gateway_settings, tool_context) -> None:
    class FakeClient:
        def __init__(self, settings, *, env):
            del settings, env

        def query_logs(self, *, service=None, query=None, limit=20):
            del service, query, limit
            raise GatewayClientError("Observability gateway kimlik dogrulamasi reddedildi.")

    monkeypatch.setattr("sentinel_cli.tools.observability.GatewayClient", FakeClient)
    tool = ObsLogsQueryTool(gateway_settings)
    args = tool.args_model(service="gateway")

    result = tool.execute(args, tool_context)

    assert result.ok is False
    assert result.code == "GATEWAY_ERROR"
    assert "kimlik dogrulamasi" in result.message


def test_traces_search_tool_uses_minimal_contract(
    monkeypatch: pytest.MonkeyPatch, gateway_settings, tool_context
) -> None:
    class FakeClient:
        def __init__(self, settings, *, env):
            del settings, env

        def search_traces(self, *, service=None, query=None, limit=20):
            assert service == "orders"
            assert query is None
            assert limit == 7
            return {"backend": "tempo", "traces": [{"trace_id": "trace-1"}]}

    monkeypatch.setattr("sentinel_cli.tools.observability.GatewayClient", FakeClient)
    tool = ObsTracesSearchTool(gateway_settings)
    args = tool.args_model(service="orders", limit=7)

    result = tool.execute(args, tool_context)

    assert result.ok is True
    assert result.data["traces"][0]["trace_id"] == "trace-1"


def test_trace_get_tool_fetches_trace_detail(
    monkeypatch: pytest.MonkeyPatch, gateway_settings, tool_context
) -> None:
    class FakeClient:
        def __init__(self, settings, *, env):
            del settings, env

        def get_trace(self, trace_id: str):
            assert trace_id == "trace-123"
            return {"backend": "tempo", "trace": {"trace_id": trace_id}}

    monkeypatch.setattr("sentinel_cli.tools.observability.GatewayClient", FakeClient)
    tool = ObsTraceGetTool(gateway_settings)
    args = tool.args_model(trace_id="trace-123")

    result = tool.execute(args, tool_context)

    assert result.ok is True
    assert result.data["trace"]["trace_id"] == "trace-123"


def test_tool_client_reads_gateway_token_from_environment(
    monkeypatch: pytest.MonkeyPatch, gateway_settings, tool_context
) -> None:
    captured = {}

    class FakeClient:
        def __init__(self, settings, *, env):
            del settings
            captured.update(env)

        def query_metric(self, query: str):
            del query
            return {"backend": "prometheus", "series": []}

    monkeypatch.setenv("SENTINEL_OBSERVABILITY_GATEWAY_TOKEN", "secret-token")
    monkeypatch.setattr("sentinel_cli.tools.observability.GatewayClient", FakeClient)
    tool = ObsMetricQueryTool(gateway_settings)

    result = tool.execute(tool.args_model(query="up"), tool_context)

    assert result.ok is True
    assert captured["SENTINEL_OBSERVABILITY_GATEWAY_TOKEN"] == "secret-token"
    assert "secret-token" == os.environ["SENTINEL_OBSERVABILITY_GATEWAY_TOKEN"]
