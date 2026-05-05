from __future__ import annotations

from pathlib import Path

import pytest

from sentinel_cli.config import CliOverrides, ConfigError, load_config, resolve_profile


def test_config_merge_precedence_and_list_replace(tmp_path: Path) -> None:
    config_path = tmp_path / "sentinel.yaml"
    config_path.write_text(
        """
profile: cloud
profiles:
  cloud:
    model: file-model
    base_url: https://file.example/v1
http:
  retry:
    retryable_status_codes: [500]
""".strip(),
        encoding="utf-8",
    )

    config = load_config(
        config_path=config_path,
        cli_overrides=CliOverrides(profile="local", model="cli-local-model"),
        env={
            "SENTINEL_PROFILE": "cloud",
            "SENTINEL_MODEL": "env-cloud-model",
            "SENTINEL_HTTP_RETRY_STATUSES": "429,503",
        },
    )

    assert config.profile == "local"
    assert config.profiles["cloud"].model == "env-cloud-model"
    assert config.profiles["cloud"].base_url == "https://file.example/v1"
    assert config.profiles["local"].model == "cli-local-model"
    assert config.http.retry.retryable_status_codes == [429, 503]


def test_unknown_profile_has_meaningful_error() -> None:
    config = load_config(cli_overrides=CliOverrides(profile="cloud"), env={})
    config.profile = "does-not-exist"

    with pytest.raises(ConfigError, match="Bilinmeyen profil"):
        resolve_profile(config, env={})


def test_project_openai_base_url_wins_over_fallback() -> None:
    config = load_config(
        env={
            "SENTINEL_PROFILE": "cloud",
            "SENTINEL_OPENAI_BASE_URL": "https://project.example/v1",
            "OPENAI_BASE_URL": "https://fallback.example/v1",
        }
    )

    profile = resolve_profile(config, env={})
    assert profile.base_url == "https://project.example/v1"


def test_experimental_mcp_flag_defaults_off_and_can_be_enabled() -> None:
    default_config = load_config(env={})
    enabled_config = load_config(env={"SENTINEL_EXPERIMENTAL_MCP": "true"})

    assert default_config.experimental.mcp_stdio_client is False
    assert enabled_config.experimental.mcp_stdio_client is True


def test_default_profile_is_cloud_with_gemini_defaults() -> None:
    config = load_config(env={})

    assert config.profile == "cloud"
    assert config.profiles["cloud"].model == "gemini-2.5-flash"
    assert (
        config.profiles["cloud"].base_url
        == "https://generativelanguage.googleapis.com/v1beta/openai/"
    )
    assert config.profiles["cloud"].supports_tools is False
    assert config.profiles["local"].model == "gemma4:latest"


def test_cloud_supports_tools_env_overrides_profile() -> None:
    off = load_config(
        env={
            "SENTINEL_PROFILE": "cloud",
            "SENTINEL_CLOUD_SUPPORTS_TOOLS": "false",
        }
    )
    on = load_config(
        env={
            "SENTINEL_PROFILE": "cloud",
            "SENTINEL_CLOUD_SUPPORTS_TOOLS": "true",
        }
    )
    assert off.profiles["cloud"].supports_tools is False
    assert on.profiles["cloud"].supports_tools is True


def test_grafana_env_overlay_enables_and_configures_section() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_BASE_URL": "https://grafana.example.test",
            "SENTINEL_GRAFANA_TIMEOUT_SEC": "9",
            "SENTINEL_GRAFANA_VERIFY_SSL": "false",
            "SENTINEL_GRAFANA_TOKEN_ENV": "CUSTOM_GRAFANA_TOKEN",
        }
    )

    assert config.grafana.enabled is True
    assert config.grafana.base_url == "https://grafana.example.test"
    assert config.grafana.timeout_sec == 9
    assert config.grafana.verify_ssl is False
    assert config.grafana.token_env == "CUSTOM_GRAFANA_TOKEN"


def test_grafana_explicit_enabled_without_base_url_is_preserved() -> None:
    config = load_config(
        env={
            "SENTINEL_GRAFANA_ENABLED": "true",
            "SENTINEL_GRAFANA_HEALTH_PATH": "ready",
        }
    )

    assert config.grafana.enabled is True
    assert config.grafana.base_url is None
    assert config.grafana.health_path == "ready"


def test_grafana_context_in_repl_defaults_true_and_env_can_disable() -> None:
    default_config = load_config(env={})
    disabled = load_config(env={"SENTINEL_GRAFANA_CONTEXT_IN_REPL": "false"})

    assert default_config.agent.grafana_context_in_repl is True
    assert disabled.agent.grafana_context_in_repl is False


def test_observability_gateway_env_overlay_enables_and_configures_section() -> None:
    config = load_config(
        env={
            "SENTINEL_OBSERVABILITY_GATEWAY_BASE_URL": "https://gateway.example.test",
            "SENTINEL_OBSERVABILITY_GATEWAY_TIMEOUT_SEC": "8",
            "SENTINEL_OBSERVABILITY_GATEWAY_TOKEN_ENV": "CUSTOM_GATEWAY_TOKEN",
        }
    )

    assert config.observability_gateway.enabled is True
    assert config.observability_gateway.base_url == "https://gateway.example.test"
    assert config.observability_gateway.timeout_sec == 8
    assert config.observability_gateway.token_env == "CUSTOM_GATEWAY_TOKEN"


def test_memory_enforce_write_jail_env() -> None:
    on = load_config(env={"SENTINEL_MEMORY_ENFORCE_WRITE_JAIL": "true"})
    off = load_config(env={"SENTINEL_MEMORY_ENFORCE_WRITE_JAIL": "false"})
    assert on.memory.enforce_write_jail is True
    assert off.memory.enforce_write_jail is False
