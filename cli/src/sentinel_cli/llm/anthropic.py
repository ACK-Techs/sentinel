"""Anthropic Messages adapter mapped to the internal provider contract."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import httpx

from sentinel_cli.config.models import AppConfig, ResolvedProfile
from sentinel_cli.llm.context import ContextWindowPolicy
from sentinel_cli.llm.errors import AuthenticationError, ProviderConnectionError, ProviderResponseError, RateLimitError
from sentinel_cli.llm.retry import bounded_retry, should_retry_status
from sentinel_cli.llm.streaming import StreamAccumulator, normalize_anthropic_event
from sentinel_cli.llm.types import ChatMessage, ChatRequest, CompletionResult, ModelUsage, StreamEvent, ToolCall


class AnthropicProvider:
    """Anthropic Messages API adapter."""

    provider_name = "anthropic"

    def __init__(
        self,
        *,
        config: AppConfig,
        profile: ResolvedProfile,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self._config = config
        self._profile = profile
        self._context_policy = ContextWindowPolicy(config.context_window)
        self._client = httpx.Client(
            timeout=httpx.Timeout(
                connect=config.http.connect_timeout_sec,
                read=profile.timeout_sec,
                write=profile.timeout_sec,
                pool=config.http.connect_timeout_sec,
            ),
            transport=transport,
        )

    def _headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "anthropic-version": "2023-06-01",
        }
        if self._profile.api_key:
            headers["x-api-key"] = self._profile.api_key
        return headers

    @staticmethod
    def _split_messages(messages: list[ChatMessage]) -> tuple[str | None, list[dict[str, Any]]]:
        system_parts: list[str] = []
        result: list[dict[str, Any]] = []
        for message in messages:
            if message.role == "system":
                system_parts.append(message.content)
                continue
            result.append({"role": message.role.value, "content": message.content})
        system_prompt = "\n\n".join(system_parts) or None
        return system_prompt, result

    def _build_payload(self, request: ChatRequest, *, stream: bool) -> dict[str, Any]:
        context = self._context_policy.apply(request.messages, system_prompt=request.system_prompt)
        system_from_messages, anthropic_messages = self._split_messages(context.messages)
        payload: dict[str, Any] = {
            "model": self._profile.model,
            "messages": anthropic_messages,
            "stream": stream,
            "max_tokens": request.max_output_tokens or 1024,
        }
        system_prompt = request.system_prompt or system_from_messages
        if system_prompt:
            payload["system"] = system_prompt
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.tools:
            payload["tools"] = [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "input_schema": tool.input_schema,
                }
                for tool in request.tools
            ]
        return payload

    def _handle_response_errors(self, response: httpx.Response) -> None:
        if response.status_code in {401, 403}:
            raise AuthenticationError("Anthropic kimlik dogrulamasi basarisiz.")
        if response.status_code == 429:
            raise RateLimitError("Anthropic oran sinirina takildi.")
        if response.status_code >= 400:
            raise ProviderResponseError(f"Anthropic HTTP hatasi: {response.status_code}.")

    def _post(self, payload: dict[str, Any]) -> httpx.Response:
        def operation(_: int) -> httpx.Response:
            try:
                response = self._client.post(
                    self._profile.base_url,
                    json=payload,
                    headers=self._headers(),
                    timeout=None,
                )
            except httpx.ConnectError as exc:
                raise ProviderConnectionError("Anthropic servisine baglanilamadi.") from exc
            except httpx.TimeoutException as exc:
                raise ProviderConnectionError("Anthropic istegi zaman asimina ugradi.") from exc
            if should_retry_status(response.status_code, self._config.http.retry):
                raise httpx.ReadError(f"Retryable status: {response.status_code}")
            self._handle_response_errors(response)
            return response

        return bounded_retry(operation, settings=self._config.http.retry)

    @staticmethod
    def _parse_completion(data: dict[str, Any]) -> CompletionResult:
        text_parts: list[str] = []
        tool_calls: list[ToolCall] = []
        for item in data.get("content", []):
            if item.get("type") == "text":
                text_parts.append(item.get("text", ""))
            if item.get("type") == "tool_use":
                tool_calls.append(
                    ToolCall(
                        id=item.get("id", ""),
                        name=item.get("name", ""),
                        arguments_json=json.dumps(item.get("input", {}), separators=(",", ":")),
                    )
                )
        usage = data.get("usage")
        usage_obj = None
        if usage:
            output_tokens = usage.get("output_tokens")
            input_tokens = usage.get("input_tokens")
            total_tokens = None
            if input_tokens is not None and output_tokens is not None:
                total_tokens = input_tokens + output_tokens
            usage_obj = ModelUsage(
                input_tokens=input_tokens,
                output_tokens=output_tokens,
                total_tokens=total_tokens,
            )
        return CompletionResult(
            text="".join(text_parts),
            tool_calls=tool_calls,
            usage=usage_obj,
            stop_reason=data.get("stop_reason"),
            provider_name="anthropic",
            raw=data,
        )

    def complete(self, request: ChatRequest) -> CompletionResult:
        response = self._post(self._build_payload(request, stream=False))
        return self._parse_completion(response.json())

    def _iter_sse_events(self, response: httpx.Response) -> Iterator[dict[str, Any]]:
        for line in response.iter_lines():
            if not line:
                continue
            decoded = line.decode("utf-8", errors="replace") if isinstance(line, bytes) else line
            if not decoded.startswith("data:"):
                continue
            yield json.loads(decoded[5:].strip())

    def stream(self, request: ChatRequest) -> list[StreamEvent]:
        payload = self._build_payload(request, stream=True)
        emitted_events: list[StreamEvent] = []
        accumulator = StreamAccumulator()
        try:
            with self._client.stream(
                "POST",
                self._profile.base_url,
                json=payload,
                headers=self._headers(),
                timeout=None,
            ) as response:
                self._handle_response_errors(response)
                for item in self._iter_sse_events(response):
                    for event in normalize_anthropic_event(item):
                        emitted_events.extend(accumulator.add(event))
            return emitted_events
        except httpx.ConnectError as exc:
            raise ProviderConnectionError("Anthropic stream baglantisi kurulamadi.") from exc
        except httpx.TimeoutException as exc:
            raise ProviderConnectionError("Anthropic stream zaman asimina ugradi.") from exc
