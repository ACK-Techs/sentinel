from __future__ import annotations

import json

import httpx

from sentinel_cli.config import load_config, resolve_profile
from sentinel_cli.llm.errors import ProviderConnectionError
from sentinel_cli.llm.openai_compatible import OpenAICompatibleProvider
from sentinel_cli.llm.types import ChatMessage, ChatRequest, MessageRole


def test_openai_complete_mock_roundtrip() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/chat/completions"
        payload = json.loads(request.content.decode("utf-8"))
        assert payload["model"] == "mock-model"
        return httpx.Response(
            200,
            json={
                "choices": [
                    {
                        "message": {"content": "merhaba"},
                        "finish_reason": "stop",
                    }
                ],
                "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
            },
        )

    config = load_config(env={"SENTINEL_PROFILE": "cloud", "SENTINEL_MODEL": "mock-model"})
    provider = OpenAICompatibleProvider(
        config=config,
        profile=resolve_profile(config, env={"SENTINEL_API_KEY": "x"}),
        transport=httpx.MockTransport(handler),
    )

    result = provider.complete(
        ChatRequest(messages=[ChatMessage(role=MessageRole.USER, content="selam")])
    )

    assert result.text == "merhaba"
    assert result.usage is not None
    assert result.usage.total_tokens == 12


def test_openai_stream_assembles_text_and_tool_calls() -> None:
    stream_body = "\n\n".join(
        [
            'data: {"choices":[{"delta":{"content":"Mer"}}]}',
            'data: {"choices":[{"delta":{"content":"haba"}}]}',
            'data: {"choices":[{"delta":{"tool_calls":[{"index":0,"id":"call_1","function":{"name":"inspect","arguments":"{\\"target\\":"}}]}}]}',
            'data: {"choices":[{"delta":{"tool_calls":[{"index":0,"function":{"arguments":"\\"grafana\\"}"}}]}}',
            "data: [DONE]",
            "",
        ]
    )

    def handler(_: httpx.Request) -> httpx.Response:
        return httpx.Response(200, text=stream_body)

    config = load_config(env={"SENTINEL_PROFILE": "cloud"})
    provider = OpenAICompatibleProvider(
        config=config,
        profile=resolve_profile(config, env={"SENTINEL_API_KEY": "x"}),
        transport=httpx.MockTransport(handler),
    )

    events = provider.stream(
        ChatRequest(messages=[ChatMessage(role=MessageRole.USER, content="selam")])
    )

    text = "".join(event.text or "" for event in events if event.kind == "text_delta")
    ready = [event for event in events if event.kind == "tool_call_ready"]
    assert text == "Merhaba"
    assert ready[0].tool_name == "inspect"
    assert ready[0].arguments_json == '{"target":"grafana"}'


def test_local_connection_error_shows_checklist() -> None:
    def handler(_: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("no listener")

    config = load_config(env={"SENTINEL_PROFILE": "local"})
    provider = OpenAICompatibleProvider(
        config=config,
        profile=resolve_profile(config, env={}),
        transport=httpx.MockTransport(handler),
    )

    try:
        provider.complete(ChatRequest(messages=[ChatMessage(role=MessageRole.USER, content="selam")]))
    except ProviderConnectionError as exc:
        assert "Kontrol listesi" in str(exc)
    else:
        raise AssertionError("ProviderConnectionError bekleniyordu")
