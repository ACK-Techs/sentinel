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
