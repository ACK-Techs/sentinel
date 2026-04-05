from __future__ import annotations

from pathlib import Path

import httpx

from sentinel_cli.config import load_config
from sentinel_cli.observability import check_grafana_connection
from sentinel_cli.observability.grafana import _join_url


def _transport(status_code: int) -> httpx.MockTransport:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/health"
        assert request.headers["Authorization"] == "Bearer secret-token"
        return httpx.Response(status_code, json={"status": "ok"})

    return httpx.MockTransport(handler)


def test_join_url_normalizes_missing_leading_slash() -> None:
    assert _join_url("https://grafana.example.test/", "api/health") == (
        "https://grafana.example.test/api/health"
    )


def test_grafana_connection_skips_when_base_url_missing() -> None:
    config = load_config(env={"SENTINEL_GRAFANA_ENABLED": "true"})

    result = check_grafana_connection(config.grafana, env={})

    assert result.configured is True
    assert result.attempted is False
    assert result.status == "skipped"
    assert result.base_url_present is False


def test_grafana_connection_ok() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_BASE_URL": "https://grafana.example.test",
            "SENTINEL_GRAFANA_TOKEN": "secret-token",
        }
    )

    result = check_grafana_connection(
        config.grafana,
        env={"SENTINEL_GRAFANA_TOKEN": "secret-token"},
        transport=_transport(200),
    )

    assert result.ok is True
    assert result.status == "ok"
    assert result.http_status == 200


def test_grafana_connection_unauthorized() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_BASE_URL": "https://grafana.example.test",
            "SENTINEL_GRAFANA_TOKEN": "secret-token",
        }
    )

    result = check_grafana_connection(
        config.grafana,
        env={"SENTINEL_GRAFANA_TOKEN": "secret-token"},
        transport=_transport(401),
    )

    assert result.ok is False
    assert result.status == "unauthorized"
    assert result.http_status == 401


def test_grafana_connection_forbidden_maps_to_unauthorized() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_BASE_URL": "https://grafana.example.test",
            "SENTINEL_GRAFANA_TOKEN": "secret-token",
        }
    )

    result = check_grafana_connection(
        config.grafana,
        env={"SENTINEL_GRAFANA_TOKEN": "secret-token"},
        transport=_transport(403),
    )

    assert result.ok is False
    assert result.status == "unauthorized"
    assert result.http_status == 403


def test_grafana_connection_timeout() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_BASE_URL": "https://grafana.example.test",
            "SENTINEL_GRAFANA_TOKEN": "secret-token",
        }
    )

    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.ReadTimeout("timed out")

    result = check_grafana_connection(
        config.grafana,
        env={"SENTINEL_GRAFANA_TOKEN": "secret-token"},
        transport=httpx.MockTransport(handler),
    )

    assert result.ok is False
    assert result.status == "timeout"
    assert result.http_status is None


def test_grafana_connection_uses_custom_token_env_and_health_path() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_BASE_URL": "https://grafana.example.test",
            "SENTINEL_GRAFANA_TOKEN_ENV": "CUSTOM_GRAFANA_TOKEN",
            "SENTINEL_GRAFANA_HEALTH_PATH": "ready",
        }
    )

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/ready"
        assert request.headers["Authorization"] == "Bearer custom-secret"
        return httpx.Response(200)

    result = check_grafana_connection(
        config.grafana,
        env={"CUSTOM_GRAFANA_TOKEN": "custom-secret"},
        transport=httpx.MockTransport(handler),
    )

    assert result.ok is True
    assert result.health_path == "ready"
    assert result.token_present is True


def test_grafana_connection_reports_tls_like_http_errors() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_BASE_URL": "https://grafana.example.test",
            "SENTINEL_GRAFANA_VERIFY_SSL": "false",
        }
    )

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("certificate verify failed", request=request)

    result = check_grafana_connection(
        config.grafana,
        env={},
        transport=httpx.MockTransport(handler),
    )

    assert result.ok is False
    assert result.status == "error"
    assert result.verify_ssl is False


def test_grafana_example_yaml_matches_runtime_defaults() -> None:
    example_path = Path(__file__).resolve().parents[2] / "config" / "sentinel.example.yaml"

    config = load_config(config_path=example_path, env={})

    assert config.grafana.enabled is False
    assert config.grafana.base_url is None
    assert config.grafana.health_path == "/api/health"
    assert config.grafana.timeout_sec == 5
    assert config.grafana.token_env == "SENTINEL_GRAFANA_TOKEN"
    assert config.grafana.verify_ssl is True
