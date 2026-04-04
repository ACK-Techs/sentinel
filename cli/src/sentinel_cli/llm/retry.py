"""Bounded retry helpers for LLM HTTP calls."""

from __future__ import annotations

import time
from collections.abc import Callable
from typing import TypeVar

import httpx

from sentinel_cli.config.models import RetryPolicySettings

T = TypeVar("T")


def should_retry_exception(exc: Exception) -> bool:
    return isinstance(exc, (httpx.ConnectError, httpx.ReadError, httpx.TimeoutException))


def should_retry_status(code: int, settings: RetryPolicySettings) -> bool:
    return code in settings.retryable_status_codes


def bounded_retry(
    operation: Callable[[int], T],
    *,
    settings: RetryPolicySettings,
    sleep_fn: Callable[[float], None] | None = None,
) -> T:
    """Execute an operation with bounded retries and no secret logging."""

    sleeper = time.sleep if sleep_fn is None else sleep_fn
    started = time.monotonic()
    last_error: Exception | None = None

    for attempt in range(1, settings.max_attempts + 1):
        try:
            return operation(attempt)
        except Exception as exc:  # noqa: BLE001
            last_error = exc
            if attempt >= settings.max_attempts or not should_retry_exception(exc):
                raise
            delay = min(settings.backoff_base_sec * (2 ** (attempt - 1)), settings.max_backoff_sec)
            elapsed = time.monotonic() - started
            if elapsed + delay > settings.total_budget_sec:
                raise
            sleeper(delay)

    assert last_error is not None
    raise last_error
