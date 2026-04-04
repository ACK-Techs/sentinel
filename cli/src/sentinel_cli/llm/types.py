"""Shared provider contract types."""

from __future__ import annotations

from enum import StrEnum
from typing import Any, Literal, Protocol

from pydantic import BaseModel, ConfigDict, Field


class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


class ToolDefinition(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    description: str
    input_schema: dict[str, Any] = Field(default_factory=dict)


class ToolCall(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    arguments_json: str


class ChatMessage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    role: MessageRole
    content: str
    name: str | None = None
    tool_call_id: str | None = None


class ChatRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    messages: list[ChatMessage]
    system_prompt: str | None = None
    tools: list[ToolDefinition] = Field(default_factory=list)
    temperature: float | None = None
    max_output_tokens: int | None = None


class ModelUsage(BaseModel):
    model_config = ConfigDict(extra="forbid")

    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None


class CompletionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    text: str = ""
    tool_calls: list[ToolCall] = Field(default_factory=list)
    usage: ModelUsage | None = None
    stop_reason: str | None = None
    provider_name: str
    raw: dict[str, Any] = Field(default_factory=dict)


class StreamEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")

    kind: Literal[
        "text_delta",
        "tool_call_delta",
        "tool_call_ready",
        "usage",
        "done",
        "error",
    ]
    text: str | None = None
    call_index: int | None = None
    tool_call_id: str | None = None
    tool_name: str | None = None
    arguments_delta: str | None = None
    arguments_json: str | None = None
    usage: ModelUsage | None = None
    stop_reason: str | None = None
    error: str | None = None


class LLMProvider(Protocol):
    """Synchronous provider interface with completion and streaming."""

    def complete(self, request: ChatRequest) -> CompletionResult:
        ...

    def stream(self, request: ChatRequest) -> list[StreamEvent]:
        ...
