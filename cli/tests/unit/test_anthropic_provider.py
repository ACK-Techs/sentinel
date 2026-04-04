from __future__ import annotations

import json

import httpx

from sentinel_cli.config import load_config, resolve_profile
from sentinel_cli.llm.anthropic import AnthropicProvider
from sentinel_cli.llm.types import ChatMessage, ChatRequest, MessageRole, ToolDefinition


def test_anthropic_complete_maps_tool_use() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["model"] == "anthropic-test-model"
        assert payload["tools"][0]["name"] == "inspect"
        return httpx.Response(
            200,
            json={
                "content": [
                    {"type": "text", "text": "Durumu inceledim."},
                    {"type": "tool_use", "id": "tool_1", "name": "inspect", "input": {"target": "loki"}},
                ],
                "stop_reason": "tool_use",
                "usage": {"input_tokens": 10, "output_tokens": 20},
            },
        )

    config = load_config(
        env={
            "SENTINEL_PROFILE": "anthropic",
            "SENTINEL_ANTHROPIC_MODEL": "anthropic-test-model",
        }
    )
    provider = AnthropicProvider(
        config=config,
        profile=resolve_profile(config, env={"ANTHROPIC_API_KEY": "secret"}),
        transport=httpx.MockTransport(handler),
    )

    result = provider.complete(
        ChatRequest(
            messages=[ChatMessage(role=MessageRole.USER, content="Loki durumunu kontrol et")],
            tools=[ToolDefinition(name="inspect", description="Inspect stack", input_schema={"type": "object"})],
        )
    )

    assert result.text == "Durumu inceledim."
    assert result.tool_calls[0].name == "inspect"
    assert result.tool_calls[0].arguments_json == '{"target":"loki"}'
