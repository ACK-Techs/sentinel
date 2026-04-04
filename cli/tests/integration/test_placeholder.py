from __future__ import annotations

import httpx

from sentinel_cli.config import CliOverrides, load_config, resolve_profile
from sentinel_cli.llm.factory import build_provider
from sentinel_cli.llm.types import ChatMessage, ChatRequest, MessageRole


def test_cloud_profile_mock_stream_integration() -> None:
    stream_body = "\n\n".join(
        [
            'data: {"choices":[{"delta":{"content":"COS"}}]}',
            'data: {"choices":[{"delta":{"content":" hazir"}}]}',
            "data: [DONE]",
            "",
        ]
    )

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=stream_body)

    config = load_config(
        cli_overrides=CliOverrides(profile="cloud", model="mock-cloud"),
        env={"SENTINEL_API_KEY": "redacted"},
    )
    provider = build_provider(
        config,
        transport=httpx.MockTransport(handler),
        resolved_profile=resolve_profile(config, env={"SENTINEL_API_KEY": "redacted"}),
    )

    events = provider.stream(
        ChatRequest(messages=[ChatMessage(role=MessageRole.USER, content="durum")])
    )
    text = "".join(event.text or "" for event in events if event.kind == "text_delta")
    assert text == "COS hazir"
