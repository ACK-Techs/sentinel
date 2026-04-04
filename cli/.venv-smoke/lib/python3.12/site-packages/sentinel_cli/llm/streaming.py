"""Streaming event normalization and assembly."""

from __future__ import annotations

from sentinel_cli.llm.types import StreamEvent


class StreamAccumulator:
    """Accumulate provider deltas into stable tool call events."""

    def __init__(self) -> None:
        self.text_parts: list[str] = []
        self.tool_calls: dict[int, dict[str, str]] = {}

    def add(self, event: StreamEvent) -> list[StreamEvent]:
        emitted = [event]
        if event.kind == "text_delta" and event.text:
            self.text_parts.append(event.text)
        if event.kind == "tool_call_delta":
            call_index = event.call_index or 0
            buffer = self.tool_calls.setdefault(
                call_index,
                {"id": event.tool_call_id or f"call_{call_index}", "name": event.tool_name or "", "args": ""},
            )
            if event.tool_call_id:
                buffer["id"] = event.tool_call_id
            if event.tool_name:
                buffer["name"] = event.tool_name
            if event.arguments_delta:
                buffer["args"] += event.arguments_delta
        if event.kind == "done":
            for index in sorted(self.tool_calls):
                payload = self.tool_calls[index]
                emitted.insert(
                    -1 if emitted else 0,
                    StreamEvent(
                        kind="tool_call_ready",
                        call_index=index,
                        tool_call_id=payload["id"],
                        tool_name=payload["name"],
                        arguments_json=payload["args"],
                    ),
                )
        return emitted


def normalize_openai_chunk(chunk: dict) -> list[StreamEvent]:
    """Convert one OpenAI-compatible stream chunk into internal events."""

    events: list[StreamEvent] = []
    usage = chunk.get("usage")
    if usage:
        events.append(
            StreamEvent(
                kind="usage",
                usage={
                    "input_tokens": usage.get("prompt_tokens"),
                    "output_tokens": usage.get("completion_tokens"),
                    "total_tokens": usage.get("total_tokens"),
                },
            )
        )

    for choice in chunk.get("choices", []):
        delta = choice.get("delta", {})
        if delta.get("content"):
            events.append(StreamEvent(kind="text_delta", text=delta["content"]))
        for tool_call in delta.get("tool_calls", []):
            function = tool_call.get("function", {})
            events.append(
                StreamEvent(
                    kind="tool_call_delta",
                    call_index=tool_call.get("index", 0),
                    tool_call_id=tool_call.get("id"),
                    tool_name=function.get("name"),
                    arguments_delta=function.get("arguments"),
                )
            )
        finish_reason = choice.get("finish_reason")
        if finish_reason:
            events.append(StreamEvent(kind="done", stop_reason=finish_reason))

    return events


def normalize_anthropic_event(payload: dict) -> list[StreamEvent]:
    """Convert one Anthropic stream event into internal events."""

    event_type = payload.get("type")
    if event_type == "content_block_delta":
        delta = payload.get("delta", {})
        if delta.get("type") == "text_delta":
            return [StreamEvent(kind="text_delta", text=delta.get("text", ""))]
        if delta.get("type") == "input_json_delta":
            return [
                StreamEvent(
                    kind="tool_call_delta",
                    call_index=payload.get("index", 0),
                    arguments_delta=delta.get("partial_json", ""),
                )
            ]
    if event_type == "content_block_start":
        block = payload.get("content_block", {})
        if block.get("type") == "tool_use":
            return [
                StreamEvent(
                    kind="tool_call_delta",
                    call_index=payload.get("index", 0),
                    tool_call_id=block.get("id"),
                    tool_name=block.get("name"),
                )
            ]
    if event_type == "message_delta":
        return [StreamEvent(kind="done", stop_reason=payload.get("delta", {}).get("stop_reason"))]
    if event_type == "message_stop":
        return [StreamEvent(kind="done", stop_reason="stop")]
    return []
