"""OpenAI-compatible HTTP provider used for cloud and local profiles."""

from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

import httpx

from sentinel_cli.config.models import AppConfig, ResolvedProfile
from sentinel_cli.llm.context import ContextWindowPolicy
from sentinel_cli.llm.errors import (
    AuthenticationError,
    ProviderConnectionError,
    ProviderResponseError,
    RateLimitError,
)
from sentinel_cli.llm.retry import bounded_retry, should_retry_status
from sentinel_cli.llm.streaming import StreamAccumulator, normalize_openai_chunk
from sentinel_cli.llm.types import ChatMessage, ChatRequest, CompletionResult, ModelUsage, StreamEvent, ToolCall


class OpenAICompatibleProvider:
    """Chat provider for remote or local OpenAI-style endpoints."""

    provider_name = "openai-compatible"

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
            base_url=profile.base_url,
            timeout=httpx.Timeout(
                connect=config.http.connect_timeout_sec,
                read=profile.timeout_sec,
                write=profile.timeout_sec,
                pool=config.http.connect_timeout_sec,
            ),
            transport=transport,
        )

    @staticmethod
    def _message_payload(messages: list[ChatMessage]) -> list[dict[str, Any]]:
        return [message.model_dump(mode="json", exclude_none=True) for message in messages]

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self._profile.api_key:
            headers["Authorization"] = f"Bearer {self._profile.api_key}"
        return headers

    def _build_payload(self, request: ChatRequest, *, stream: bool) -> dict[str, Any]:
        context = self._context_policy.apply(request.messages, system_prompt=request.system_prompt)
        payload: dict[str, Any] = {
            "model": self._profile.model,
            "messages": self._message_payload(context.messages),
            "stream": stream,
        }
        if request.temperature is not None:
            payload["temperature"] = request.temperature
        if request.max_output_tokens is not None:
            payload["max_tokens"] = request.max_output_tokens
        if request.tools and self._profile.supports_tools:
            payload["tools"] = [
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": tool.input_schema,
                    },
                }
                for tool in request.tools
            ]
        if request.system_prompt:
            payload["messages"] = [
                {"role": "system", "content": request.system_prompt},
                *payload["messages"],
            ]
        return payload

    def _handle_response_errors(self, response: httpx.Response) -> None:
        if response.status_code in {401, 403}:
            raise AuthenticationError("Kimlik dogrulama basarisiz. Profil ve API anahtarini kontrol et.")
        if response.status_code == 429:
            raise RateLimitError("Saglayici oran sinirina takildi. Daha sonra tekrar dene.")
        if response.status_code >= 400:
            raise ProviderResponseError(
                f"Saglayici HTTP hatasi: {response.status_code}. Yanit govdesi secret icermeden ozetlenmeli."
            )

    def _post(self, payload: dict[str, Any], *, stream: bool = False) -> httpx.Response:
        def operation(_: int) -> httpx.Response:
            try:
                response = self._client.post(
                    "/chat/completions",
                    json=payload,
                    headers=self._headers(),
                    timeout=None,
                )
            except httpx.ConnectError as exc:
                if self._profile.name == "local":
                    raise ProviderConnectionError(
                        "Lokal LLM servisine baglanilamadi. Kontrol listesi: servis ayakta mi, "
                        "base_url dogru mu, port acik mi?"
                    ) from exc
                raise ProviderConnectionError("Saglayiciya baglanilamadi. Ag ve base_url ayarlarini kontrol et.") from exc
            except httpx.TimeoutException as exc:
                raise ProviderConnectionError("Saglayici istegi zaman asimina ugradi.") from exc

            if should_retry_status(response.status_code, self._config.http.retry):
                raise httpx.ReadError(f"Retryable status: {response.status_code}")
            self._handle_response_errors(response)
            return response

        return bounded_retry(operation, settings=self._config.http.retry)

    @staticmethod
    def _parse_completion(data: dict[str, Any]) -> CompletionResult:
        message = data.get("choices", [{}])[0].get("message", {})
        tool_calls = []
        for tool_call in message.get("tool_calls", []):
            function = tool_call.get("function", {})
            tool_calls.append(
                ToolCall(
                    id=tool_call.get("id", ""),
                    name=function.get("name", ""),
                    arguments_json=function.get("arguments", ""),
                )
            )
        usage = data.get("usage")
        usage_obj = None
        if usage:
            usage_obj = ModelUsage(
                input_tokens=usage.get("prompt_tokens"),
                output_tokens=usage.get("completion_tokens"),
                total_tokens=usage.get("total_tokens"),
            )
        return CompletionResult(
            text=message.get("content") or "",
            tool_calls=tool_calls,
            usage=usage_obj,
            stop_reason=data.get("choices", [{}])[0].get("finish_reason"),
            provider_name="openai-compatible",
            raw=data,
        )

    def complete(self, request: ChatRequest) -> CompletionResult:
        payload = self._build_payload(request, stream=False)
        response = self._post(payload)
        return self._parse_completion(response.json())

    def _iter_sse_events(self, response: httpx.Response) -> Iterator[dict[str, Any]]:
        for line in response.iter_lines():
            if not line:
                continue
            if isinstance(line, bytes):
                decoded = line.decode("utf-8", errors="replace")
            else:
                decoded = line
            if not decoded.startswith("data:"):
                continue
            data = decoded[5:].strip()
            if data == "[DONE]":
                yield {"choices": [{"finish_reason": "stop"}]}
                continue
            yield json.loads(data)

    def stream(self, request: ChatRequest) -> list[StreamEvent]:
        payload = self._build_payload(request, stream=True)
        emitted_events: list[StreamEvent] = []
        accumulator = StreamAccumulator()
        stream_started = False

        for attempt in range(1, self._config.http.retry.max_attempts + 1):
            try:
                with self._client.stream(
                    "POST",
                    "/chat/completions",
                    json=payload,
                    headers=self._headers(),
                    timeout=None,
                ) as response:
                    self._handle_response_errors(response)
                    for chunk in self._iter_sse_events(response):
                        stream_started = True
                        for event in normalize_openai_chunk(chunk):
                            emitted_events.extend(accumulator.add(event))
                    return emitted_events
            except (httpx.ConnectError, httpx.ReadError, httpx.TimeoutException) as exc:
                if stream_started or attempt >= self._config.http.retry.max_attempts:
                    if self._profile.name == "local":
                        raise ProviderConnectionError(
                            "Lokal stream baglantisi kesildi. Servis loglarini, modeli ve portu kontrol et."
                        ) from exc
                    raise ProviderConnectionError("Saglayici stream baglantisi kesildi veya zaman asimina ugradi.") from exc
                continue

        return emitted_events
