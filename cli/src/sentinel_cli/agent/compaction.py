"""Minimal history compaction for long sessions."""

from __future__ import annotations

from sentinel_cli.config import AppConfig
from sentinel_cli.llm.context import ContextWindowPolicy
from sentinel_cli.llm.types import ChatMessage, MessageRole
from sentinel_cli.session import SessionState


class HistoryCompactor:
    """Keep the first user goal plus recent messages when thresholds are exceeded."""

    def __init__(self, config: AppConfig) -> None:
        self._config = config
        self._policy = ContextWindowPolicy(config.context_window)

    def compact(
        self,
        messages: list[ChatMessage],
        *,
        session: SessionState | None = None,
    ) -> list[ChatMessage]:
        result = self._policy.apply(messages)
        if not result.trimmed:
            return messages[-self._config.session.max_history_messages :]

        preserved = result.messages
        first_user = next((message for message in messages if message.role == MessageRole.USER), None)
        compacted: list[ChatMessage] = []
        if first_user and first_user not in preserved:
            compacted.append(first_user)
        if self._config.semantic_compaction.inject_trim_notice:
            compacted.append(
                ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content="Eski mesajlar baglam siniri nedeniyle ozetlenmeden kirpildi.",
                )
            )
        compacted.extend(preserved)
        trimmed = compacted[-self._config.session.max_history_messages :]
        if session is not None and self._config.semantic_compaction.inject_trim_notice:
            session.compaction_note = "Baglam siniri nedeniyle eski mesajlar kirpildi; son tur korunur."
        return trimmed
