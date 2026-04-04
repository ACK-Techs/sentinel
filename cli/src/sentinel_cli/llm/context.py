"""Heuristic context window management for Phase 2.B."""

from __future__ import annotations

import math

from pydantic import BaseModel, ConfigDict, Field

from sentinel_cli.config.models import ContextWindowSettings
from sentinel_cli.llm.types import ChatMessage


class ContextWindowResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    messages: list[ChatMessage]
    estimated_tokens: int
    trimmed: bool = False
    warning: str | None = None


class ContextWindowPolicy:
    """A simple heuristic context window policy for provider requests."""

    def __init__(self, settings: ContextWindowSettings) -> None:
        self._settings = settings

    @staticmethod
    def estimate_tokens(messages: list[ChatMessage], system_prompt: str | None = None) -> int:
        text = "".join(message.content for message in messages)
        if system_prompt:
            text += system_prompt
        return max(1, math.ceil(len(text) / 4))

    def apply(
        self,
        messages: list[ChatMessage],
        *,
        system_prompt: str | None = None,
    ) -> ContextWindowResult:
        estimated = self.estimate_tokens(messages, system_prompt=system_prompt)
        threshold = int(self._settings.max_input_tokens * self._settings.warn_ratio)
        if estimated <= threshold:
            return ContextWindowResult(messages=messages, estimated_tokens=estimated)

        warning = (
            "Baglam penceresi sinirina yaklasildi. "
            f"Tahmini token: {estimated}/{self._settings.max_input_tokens}."
        )
        if self._settings.strategy == "warn":
            return ContextWindowResult(
                messages=messages,
                estimated_tokens=estimated,
                trimmed=False,
                warning=warning,
            )

        preserved = messages[-self._settings.preserve_recent_messages :]
        trimmed_estimate = self.estimate_tokens(preserved, system_prompt=system_prompt)
        return ContextWindowResult(
            messages=preserved,
            estimated_tokens=trimmed_estimate,
            trimmed=True,
            warning=f"{warning} Eski mesajlar kirpildi.",
        )
