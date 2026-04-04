"""Provider factory bound to the active config profile."""

from __future__ import annotations

import httpx

from sentinel_cli.config import AppConfig, ResolvedProfile, resolve_profile
from sentinel_cli.llm.anthropic import AnthropicProvider
from sentinel_cli.llm.openai_compatible import OpenAICompatibleProvider
from sentinel_cli.llm.types import LLMProvider


def build_provider(
    config: AppConfig,
    *,
    transport: httpx.BaseTransport | None = None,
    resolved_profile: ResolvedProfile | None = None,
) -> LLMProvider:
    profile = resolved_profile or resolve_profile(config)
    if profile.provider == "openai":
        return OpenAICompatibleProvider(config=config, profile=profile, transport=transport)
    if profile.provider == "anthropic":
        return AnthropicProvider(config=config, profile=profile, transport=transport)
    raise ValueError(f"Desteklenmeyen provider: {profile.provider}")
