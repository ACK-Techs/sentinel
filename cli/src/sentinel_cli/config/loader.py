"""Layered config loading with defaults < file < env < CLI."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from pydantic import ValidationError

from sentinel_cli.config.models import AppConfig, CliOverrides, ResolvedProfile


class ConfigError(ValueError):
    """Raised when config sources cannot be parsed or validated."""


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        if value is None:
            continue
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
            continue
        # Phase 2.B list strategy is replace; the higher precedence layer wins.
        merged[key] = value
    return merged


def _parse_csv_ints(value: str) -> list[int]:
    return [int(item.strip()) for item in value.split(",") if item.strip()]


def _load_yaml_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return {}
    if not path.exists():
        raise ConfigError(f"Config dosyasi bulunamadi: {path}")
    try:
        loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        raise ConfigError(f"Config YAML parse hatasi ({path}): {exc}") from exc
    if not isinstance(loaded, dict):
        raise ConfigError(f"Config dosyasi bir nesne olmali: {path}")
    return loaded


def _env_overlay(env: dict[str, str]) -> dict[str, Any]:
    overlay: dict[str, Any] = {}

    def assign(path: tuple[str, ...], value: Any) -> None:
        cursor = overlay
        for segment in path[:-1]:
            cursor = cursor.setdefault(segment, {})
        cursor[path[-1]] = value

    profile = env.get("SENTINEL_PROFILE")
    if profile:
        assign(("profile",), profile)

    config_path = env.get("SENTINEL_CONFIG")
    if config_path:
        assign(("config_path",), config_path)

    project_openai_base = env.get("SENTINEL_OPENAI_BASE_URL")
    fallback_openai_base = env.get("OPENAI_BASE_URL")
    openai_base = project_openai_base or fallback_openai_base
    if openai_base:
        assign(("profiles", "cloud", "base_url"), openai_base)

    cloud_model = env.get("SENTINEL_MODEL")
    if cloud_model:
        assign(("profiles", "cloud", "model"), cloud_model)

    local_base = env.get("SENTINEL_LOCAL_BASE_URL")
    if local_base:
        assign(("profiles", "local", "base_url"), local_base)

    local_model = env.get("SENTINEL_LOCAL_MODEL")
    if local_model:
        assign(("profiles", "local", "model"), local_model)

    local_timeout = env.get("SENTINEL_LOCAL_TIMEOUT_SEC")
    if local_timeout:
        assign(("profiles", "local", "timeout_sec"), float(local_timeout))

    anthropic_model = env.get("SENTINEL_ANTHROPIC_MODEL")
    if anthropic_model:
        assign(("profiles", "anthropic", "model"), anthropic_model)

    connect_timeout = env.get("SENTINEL_HTTP_CONNECT_TIMEOUT_SEC")
    if connect_timeout:
        assign(("http", "connect_timeout_sec"), float(connect_timeout))

    read_timeout = env.get("SENTINEL_HTTP_TIMEOUT_SEC")
    if read_timeout:
        assign(("http", "read_timeout_sec"), float(read_timeout))

    retry_attempts = env.get("SENTINEL_HTTP_MAX_RETRIES")
    if retry_attempts:
        assign(("http", "retry", "max_attempts"), int(retry_attempts))

    retry_statuses = env.get("SENTINEL_HTTP_RETRY_STATUSES")
    if retry_statuses:
        assign(("http", "retry", "retryable_status_codes"), _parse_csv_ints(retry_statuses))

    context_window = env.get("SENTINEL_CONTEXT_WINDOW_TOKENS")
    if context_window:
        assign(("context_window", "max_input_tokens"), int(context_window))

    context_warn = env.get("SENTINEL_CONTEXT_WARN_AT")
    if context_warn:
        assign(("context_window", "warn_ratio"), float(context_warn))

    context_strategy = env.get("SENTINEL_CONTEXT_STRATEGY")
    if context_strategy:
        assign(("context_window", "strategy"), context_strategy)

    log_level = env.get("SENTINEL_LOG_LEVEL")
    if log_level:
        assign(("logging", "level"), log_level.upper())

    max_turns = env.get("SENTINEL_MAX_TURNS")
    if max_turns:
        assign(("agent", "max_turns"), int(max_turns))

    auto_approve = env.get("SENTINEL_AUTO_APPROVE")
    if auto_approve:
        normalized = auto_approve.lower() in {"1", "true", "yes", "on"}
        assign(("tools", "auto_approve"), normalized)
        assign(("tools", "approval_mode"), "auto" if normalized else "interactive")

    session_dir = env.get("SENTINEL_SESSION_DIR")
    if session_dir:
        assign(("session", "directory"), session_dir)

    trajectory_dir = env.get("SENTINEL_TRAJECTORY_DIR")
    if trajectory_dir:
        assign(("session", "trajectory_directory"), trajectory_dir)

    trajectory_enabled = env.get("SENTINEL_TRAJECTORY_ENABLED")
    if trajectory_enabled:
        assign(
            ("session", "trajectory_enabled"),
            trajectory_enabled.lower() in {"1", "true", "yes", "on"},
        )

    return overlay


def _cli_overlay(overrides: CliOverrides | None) -> dict[str, Any]:
    if overrides is None:
        return {}
    overlay: dict[str, Any] = {}

    if overrides.config_path:
        overlay["config_path"] = str(overrides.config_path)
    if overrides.profile:
        overlay["profile"] = overrides.profile
    if overrides.connect_timeout_sec is not None:
        overlay.setdefault("http", {})["connect_timeout_sec"] = overrides.connect_timeout_sec
    if overrides.read_timeout_sec is not None:
        overlay.setdefault("http", {})["read_timeout_sec"] = overrides.read_timeout_sec
    if overrides.log_level is not None:
        overlay.setdefault("logging", {})["level"] = overrides.log_level
    if overrides.max_turns is not None:
        overlay.setdefault("agent", {})["max_turns"] = overrides.max_turns
    if overrides.auto_approve is not None:
        overlay.setdefault("tools", {})["auto_approve"] = overrides.auto_approve
        overlay.setdefault("tools", {})["approval_mode"] = (
            "auto" if overrides.auto_approve else "interactive"
        )
    if overrides.trajectory_enabled is not None:
        overlay.setdefault("session", {})["trajectory_enabled"] = overrides.trajectory_enabled

    active_profile = overrides.profile
    if active_profile:
        profile_overlay: dict[str, Any] = {}
        if overrides.model:
            profile_overlay["model"] = overrides.model
        if overrides.base_url:
            profile_overlay["base_url"] = overrides.base_url
        if overrides.provider:
            profile_overlay["provider"] = overrides.provider
        if profile_overlay:
            overlay.setdefault("profiles", {})[active_profile] = profile_overlay

    return overlay


def load_config(
    *,
    config_path: Path | None = None,
    cli_overrides: CliOverrides | None = None,
    env: dict[str, str] | None = None,
) -> AppConfig:
    """Load the effective config using the documented precedence."""

    source_env = dict(os.environ if env is None else env)
    effective_path = config_path or cli_overrides and cli_overrides.config_path
    if effective_path is None and source_env.get("SENTINEL_CONFIG"):
        effective_path = Path(source_env["SENTINEL_CONFIG"])

    defaults = AppConfig().model_dump(mode="python")
    file_data = _load_yaml_config(effective_path)
    env_data = _env_overlay(source_env)
    cli_data = _cli_overlay(cli_overrides)

    try:
        merged = _deep_merge(defaults, file_data)
        merged = _deep_merge(merged, env_data)
        merged = _deep_merge(merged, cli_data)
        if effective_path is not None:
            merged["config_path"] = effective_path
        return AppConfig.model_validate(merged)
    except ValidationError as exc:
        raise ConfigError(f"Config dogrulama hatasi: {exc}") from exc


def resolve_profile(config: AppConfig, env: dict[str, str] | None = None) -> ResolvedProfile:
    """Resolve the active profile into concrete runtime settings."""

    source_env = os.environ if env is None else env
    profile_name = config.profile
    if profile_name not in config.profiles:
        available = ", ".join(sorted(config.profiles))
        raise ConfigError(
            f"Bilinmeyen profil: {profile_name}. Gecerli profiller: {available}."
        )

    profile = config.profiles[profile_name]
    api_key = source_env.get(profile.api_key_env) if profile.api_key_env else None
    timeout_sec = profile.timeout_sec or config.http.read_timeout_sec

    return ResolvedProfile(
        name=profile_name,
        provider=profile.provider,
        model=profile.model,
        base_url=profile.base_url.rstrip("/"),
        api_key=api_key,
        api_key_env=profile.api_key_env,
        timeout_sec=timeout_sec,
        supports_tools=profile.supports_tools,
    )
