"""Provider contracts and implementations for Sentinel CLI."""

from sentinel_cli.llm.context import ContextWindowPolicy, ContextWindowResult
from sentinel_cli.llm.errors import (
    AuthenticationError,
    LLMError,
    ProviderConnectionError,
    ProviderResponseError,
    RateLimitError,
)
from sentinel_cli.llm.factory import build_provider
from sentinel_cli.llm.types import (
    ChatMessage,
    ChatRequest,
    CompletionResult,
    MessageRole,
    ModelUsage,
    StreamEvent,
    ToolCall,
    ToolDefinition,
)

__all__ = [
    "AuthenticationError",
    "ChatMessage",
    "ChatRequest",
    "CompletionResult",
    "ContextWindowPolicy",
    "ContextWindowResult",
    "LLMError",
    "MessageRole",
    "ModelUsage",
    "ProviderConnectionError",
    "ProviderResponseError",
    "RateLimitError",
    "StreamEvent",
    "ToolCall",
    "ToolDefinition",
    "build_provider",
]
