from __future__ import annotations

from pathlib import Path

from observability_gateway.config import load_settings


def test_load_settings_merges_yaml_and_env(tmp_path: Path) -> None:
    config_path = tmp_path / "gateway.yaml"
    config_path.write_text(
        "\n".join(
            [
                "service_name: sentinel-observability-gateway",
                "prometheus:",
                "  base_url: http://prometheus-from-yaml:9090",
                "loki:",
                "  base_url: http://loki-from-yaml:3100",
                "http:",
                "  timeout_sec: 7",
            ]
        ),
        encoding="ascii",
    )

    settings = load_settings(
        config_path=config_path,
        env={
            "SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL": "http://prometheus-from-env:9090",
            "SENTINEL_OBSERVABILITY_TEMPO__BASE_URL": "http://tempo-from-env:3200",
            "SENTINEL_OBSERVABILITY_HTTP__RETRY__MAX_ATTEMPTS": "5",
        },
    )

    assert settings.prometheus.base_url == "http://prometheus-from-env:9090"
    assert settings.loki.base_url == "http://loki-from-yaml:3100"
    assert settings.tempo.base_url == "http://tempo-from-env:3200"
    assert settings.http.timeout_sec == 7
    assert settings.http.retry.max_attempts == 5


def test_sanitized_summary_reports_token_presence() -> None:
    settings = load_settings(
        env={
            "SENTINEL_OBSERVABILITY_PROMETHEUS__BASE_URL": "http://prometheus:9090",
            "SENTINEL_OBSERVABILITY_PROMETHEUS__TOKEN_ENV": "PROM_TOKEN",
            "PROM_TOKEN": "secret-value",
        }
    )

    summary = settings.sanitized_summary(env={"PROM_TOKEN": "secret-value"})

    assert summary["prometheus"]["configured"] is True
    assert summary["prometheus"]["token_env"] == "PROM_TOKEN"
    assert summary["prometheus"]["token_present"] is True
