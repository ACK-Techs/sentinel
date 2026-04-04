"""LLM provider errors with user-facing safe messages."""

from __future__ import annotations


class LLMError(RuntimeError):
    """Base class for provider failures."""


class ProviderConnectionError(LLMError):
    """Raised when the CLI cannot reach a provider endpoint."""


class AuthenticationError(LLMError):
    """Raised for missing or invalid credentials."""


class RateLimitError(LLMError):
    """Raised when the provider asks the client to slow down."""


class ProviderResponseError(LLMError):
    """Raised for non-auth provider response failures."""
