"""Append-only memory extraction from completed turns."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sentinel_cli.config import AppConfig
from sentinel_cli.llm.types import ChatMessage, MessageRole
from sentinel_cli.memory.paths import ensure_within_memory_root, resolve_memory_root
from sentinel_cli.redaction import redact_text


def _summarize_messages(messages: list[ChatMessage]) -> dict[str, Any]:
    """Structured summary without full tool payloads (secret-safe)."""

    user_snippets: list[str] = []
    assistant_snippets: list[str] = []
    tool_names: list[str] = []

    for message in messages:
        if message.role == MessageRole.USER:
            text = message.content or ""
            user_snippets.append(redact_text(text[:400]))
        elif message.role == MessageRole.ASSISTANT:
            text = message.content or ""
            assistant_snippets.append(redact_text(text[:400]))
        elif message.role == MessageRole.TOOL:
            label = message.name if message.name else "tool"
            tool_names.append(redact_text(label)[:128])

    return {
        "user": user_snippets[-3:] if user_snippets else [],
        "assistant": assistant_snippets[-3:] if assistant_snippets else [],
        "tools": tool_names[-12:] if tool_names else [],
        "tool_turns": len(tool_names),
    }


def append_extract(
    config: AppConfig,
    *,
    cwd: str,
    session_id: str,
    messages: list[ChatMessage],
) -> Path | None:
    """Append one JSON line to memory/extract.jsonl. Returns path or None if skipped."""

    if not config.memory.enabled or not config.memory.extract_on_turn_end:
        return None

    root = resolve_memory_root(config.memory, cwd=cwd)
    root.mkdir(parents=True, exist_ok=True)
    target = ensure_within_memory_root(root, root / "extract.jsonl")

    payload = {
        "ts": datetime.now(UTC).isoformat(),
        "session_id": session_id,
        "summary": _summarize_messages(messages),
    }
    line = json.dumps(payload, ensure_ascii=True)
    with target.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")
    return target
