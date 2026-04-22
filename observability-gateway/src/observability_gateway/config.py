"""Configuration models and loading helpers for the observability gateway."""

from __future__ import annotations

import os
from collections.abc import Mapping
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field

ENV_PREFIX = "SENTINEL_OBSERVABILITY_"


class RetrySettings(BaseModel):
    """Retry policy shared by outbound backend requests."""

    model_config = ConfigDict(extra="forbid")

    max_attempts: int = 3
    backoff_base_sec: float = 0.5
    retryable_status_codes: list[int] = Field(
        default_factory=lambda: [408, 429, 500, 502, 503, 504]
    )


class HttpSettings(BaseModel):
    """Common transport settings shared by all backends."""

    model_config = ConfigDict(extra="forbid")

    timeout_sec: float = 10.0
    retry: RetrySettings = Field(default_factory=RetrySettings)


class BackendSettings(BaseModel):
    """Read-only backend connection settings."""

    model_config = ConfigDict(extra="forbid")

    base_url: str | None = None
    token_env: str | None = None


class GatewaySettings(BaseModel):
    """Top-level gateway configuration."""

    model_config = ConfigDict(extra="forbid")

    service_name: str = "sentinel-observability-gateway"
    service_version: str = "0.1.0"
    prometheus: BackendSettings = Field(default_factory=BackendSettings)
    loki: BackendSettings = Field(default_factory=BackendSettings)
    tempo: BackendSettings = Field(default_factory=BackendSettings)
    http: HttpSettings = Field(default_factory=HttpSettings)
    auth_token_env: str | None = "SENTINEL_OBSERVABILITY_GATEWAY_TOKEN"

    def sanitized_summary(self, env: Mapping[str, str] | None = None) -> dict[str, Any]:
        """Return a secret-safe summary for status responses."""

        resolved_env = dict(env or os.environ)
        return {
            "service_name": self.service_name,
            "service_version": self.service_version,
            "http": self.http.model_dump(),
            "auth": {
                "token_env": self.auth_token_env,
                "token_present": bool(
                    self.auth_token_env and resolved_env.get(self.auth_token_env)
                ),
            },
            "prometheus": _backend_summary(self.prometheus, resolved_env),
            "loki": _backend_summary(self.loki, resolved_env),
            "tempo": _backend_summary(self.tempo, resolved_env),
        }


def load_settings(
    *,
    config_path: str | Path | None = None,
    env: Mapping[str, str] | None = None,
) -> GatewaySettings:
    """Load gateway settings from YAML and environment overrides."""

    resolved_env = dict(env or os.environ)
    path_value = config_path or resolved_env.get(f"{ENV_PREFIX}CONFIG_PATH")
    data: dict[str, Any] = {}
    if path_value:
        data = _load_yaml(Path(path_value))

    merged = _deep_merge(data, _env_overrides(resolved_env))
    return GatewaySettings.model_validate(merged)


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")

    loaded = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(loaded, dict):
        raise ValueError("Configuration root must be a mapping.")
    return loaded


def _env_overrides(env: Mapping[str, str]) -> dict[str, Any]:
    overrides: dict[str, Any] = {}
    for key, value in env.items():
        if not key.startswith(ENV_PREFIX) or key in {
            f"{ENV_PREFIX}CONFIG_PATH",
            f"{ENV_PREFIX}GATEWAY_TOKEN",
        }:
            continue

        path = key[len(ENV_PREFIX) :].lower().split("__")
        current = overrides
        for part in path[:-1]:
            current = current.setdefault(part, {})
        current[path[-1]] = value
    return overrides


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged = dict(base)
    for key, value in override.items():
        existing = merged.get(key)
        if isinstance(existing, dict) and isinstance(value, dict):
            merged[key] = _deep_merge(existing, value)
            continue
        merged[key] = value
    return merged


def _backend_summary(settings: BackendSettings, env: Mapping[str, str]) -> dict[str, Any]:
    token_present = bool(settings.token_env and env.get(settings.token_env))
    return {
        "configured": bool(settings.base_url),
        "base_url": settings.base_url,
        "token_env": settings.token_env,
        "token_present": token_present,
    }
