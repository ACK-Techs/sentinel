"""Pydantic models for layered Sentinel CLI configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


ProviderKind = Literal["openai", "anthropic"]
ContextStrategy = Literal["warn", "truncate"]


class RetryPolicySettings(BaseModel):
    """Retry policy for outbound LLM HTTP calls."""

    model_config = ConfigDict(extra="forbid")

    max_attempts: int = 3
    backoff_base_sec: float = 0.5
    max_backoff_sec: float = 4.0
    total_budget_sec: float = 20.0
    retryable_status_codes: list[int] = Field(default_factory=lambda: [429, 500, 502, 503, 504])


class HttpSettings(BaseModel):
    """Transport level settings shared by providers."""

    model_config = ConfigDict(extra="forbid")

    connect_timeout_sec: float = 10.0
    read_timeout_sec: float = 120.0
    retry: RetryPolicySettings = Field(default_factory=RetryPolicySettings)


class ContextWindowSettings(BaseModel):
    """Heuristic context window controls."""

    model_config = ConfigDict(extra="forbid")

    max_input_tokens: int = 32000
    warn_ratio: float = 0.85
    strategy: ContextStrategy = "truncate"
    preserve_recent_messages: int = 8


class ProfileSettings(BaseModel):
    """Per-profile provider selection and endpoint defaults."""

    model_config = ConfigDict(extra="forbid")

    provider: ProviderKind
    model: str
    base_url: str
    api_key_env: str | None = None
    timeout_sec: float | None = None
    supports_tools: bool = True


class AppConfig(BaseModel):
    """Top-level application configuration."""

    model_config = ConfigDict(extra="forbid")

    profile: str = "local"
    config_path: Path | None = None
    profiles: dict[str, ProfileSettings] = Field(
        default_factory=lambda: {
            "cloud": ProfileSettings(
                provider="openai",
                model="provider-model-placeholder",
                base_url="https://api.openai.com/v1",
                api_key_env="SENTINEL_API_KEY",
                timeout_sec=120.0,
            ),
            "local": ProfileSettings(
                provider="openai",
                model="local_model_placeholder",
                base_url="http://127.0.0.1:11434/v1",
                api_key_env=None,
                timeout_sec=120.0,
            ),
            "anthropic": ProfileSettings(
                provider="anthropic",
                model="anthropic_model_placeholder",
                base_url="https://api.anthropic.com/v1/messages",
                api_key_env="ANTHROPIC_API_KEY",
                timeout_sec=120.0,
            ),
        }
    )
    http: HttpSettings = Field(default_factory=HttpSettings)
    context_window: ContextWindowSettings = Field(default_factory=ContextWindowSettings)

    def sanitized_summary(self) -> dict[str, object]:
        """Return a secret-safe summary for debug output."""

        return {
            "profile": self.profile,
            "config_path": str(self.config_path) if self.config_path else None,
            "profiles": {
                name: {
                    "provider": profile.provider,
                    "model": profile.model,
                    "base_url": profile.base_url,
                    "api_key_env": profile.api_key_env,
                    "timeout_sec": profile.timeout_sec,
                    "supports_tools": profile.supports_tools,
                }
                for name, profile in self.profiles.items()
            },
            "http": self.http.model_dump(),
            "context_window": self.context_window.model_dump(),
            "list_merge_strategy": "replace",
        }


class CliOverrides(BaseModel):
    """Supported CLI overrides for Phase 2.B."""

    model_config = ConfigDict(extra="forbid")

    config_path: Path | None = None
    profile: str | None = None
    model: str | None = None
    base_url: str | None = None
    provider: ProviderKind | None = None
    connect_timeout_sec: float | None = None
    read_timeout_sec: float | None = None


class ResolvedProfile(BaseModel):
    """An active profile after config + env resolution."""

    model_config = ConfigDict(extra="forbid")

    name: str
    provider: ProviderKind
    model: str
    base_url: str
    api_key: str | None = None
    api_key_env: str | None = None
    timeout_sec: float
    supports_tools: bool

    def sanitized_summary(self) -> dict[str, object]:
        return {
            "name": self.name,
            "provider": self.provider,
            "model": self.model,
            "base_url": self.base_url,
            "api_key_env": self.api_key_env,
            "api_key_present": bool(self.api_key),
            "timeout_sec": self.timeout_sec,
            "supports_tools": self.supports_tools,
        }
