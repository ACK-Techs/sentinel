import json

import sentinel_cli.cli.app as app
from sentinel_cli.cli.app import main
from sentinel_cli.observability.gateway import GatewayCheckResult
from sentinel_cli.observability.grafana import GrafanaCheckResult


def test_config_command_returns_zero(capsys) -> None:
    code = main(["config", "--profile", "local"])
    captured = capsys.readouterr()
    assert code == 0
    assert '"active_profile"' in captured.out


def test_doctor_command_returns_zero(capsys) -> None:
    code = main(["doctor", "--profile", "local"])
    captured = capsys.readouterr()
    assert code == 0
    assert '"mcp"' in captured.out
    assert '"observability_gateway"' in captured.out
    assert '"grafana"' in captured.out


def test_doctor_output_contains_grafana_shape_without_token(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        app,
        "check_grafana_connection",
        lambda *args, **kwargs: GrafanaCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="unauthorized",
            message="Grafana erisiyor ancak kimlik dogrulama reddedildi.",
            http_status=401,
            health_path="/api/health",
            token_present=True,
            base_url_present=True,
            verify_ssl=True,
        ),
    )
    monkeypatch.setenv("SENTINEL_GRAFANA_TOKEN", "super-secret-token")

    code = main(["doctor", "--profile", "local"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert code == 0
    assert "grafana" in payload
    assert payload["grafana"]["troubleshoot_skill"] == "skills/agentic-troubleshoot-grafana/SKILL.md"
    assert payload["grafana"]["token_present"] is True
    assert "super-secret-token" not in captured.out


def test_doctor_output_contains_gateway_shape_without_token(monkeypatch, capsys) -> None:
    monkeypatch.setattr(
        app,
        "check_gateway_connection",
        lambda *args, **kwargs: GatewayCheckResult(
            configured=True,
            attempted=True,
            ok=False,
            status="unauthorized",
            message="Observability gateway kimlik dogrulamasi reddedildi.",
            http_status=401,
            token_present=True,
            base_url_present=True,
        ),
    )
    monkeypatch.setenv("SENTINEL_OBSERVABILITY_GATEWAY_TOKEN", "super-secret-token")

    code = main(["doctor", "--profile", "local"])
    captured = capsys.readouterr()
    payload = json.loads(captured.out)

    assert code == 0
    assert payload["observability_gateway"]["token_present"] is True
    assert payload["observability_gateway"]["status"] == "unauthorized"
    assert "super-secret-token" not in captured.out
