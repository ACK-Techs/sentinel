from sentinel_cli.config import load_config, resolve_profile
from sentinel_cli.llm.anthropic import AnthropicProvider
from sentinel_cli.llm.factory import build_provider
from sentinel_cli.llm.openai_compatible import OpenAICompatibleProvider


def test_build_provider_selects_openai_for_local_profile() -> None:
    config = load_config(env={"SENTINEL_PROFILE": "local"})
    provider = build_provider(config, resolved_profile=resolve_profile(config, env={}))
    assert isinstance(provider, OpenAICompatibleProvider)


def test_build_provider_selects_anthropic_adapter() -> None:
    config = load_config(env={"SENTINEL_PROFILE": "anthropic"})
    provider = build_provider(config, resolved_profile=resolve_profile(config, env={}))
    assert isinstance(provider, AnthropicProvider)
