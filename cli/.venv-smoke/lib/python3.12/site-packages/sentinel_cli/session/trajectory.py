"""Trajectory recording with simple redaction."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
TOKEN_RE = re.compile(r"\b(?:sk|api|token)[A-Za-z0-9._-]{8,}\b", re.IGNORECASE)


def redact_text(value: str) -> str:
    value = EMAIL_RE.sub("[redacted-email]", value)
    value = TOKEN_RE.sub("[redacted-token]", value)
    return value


class TrajectoryRecorder:
    """Append redacted trajectory events to JSONL."""

    def __init__(self, directory: Path, *, enabled: bool) -> None:
        self._directory = directory
        self._enabled = enabled
        self._directory.mkdir(parents=True, exist_ok=True)

    def append(self, session_id: str, event: dict[str, Any]) -> None:
        if not self._enabled:
            return
        safe_event = json.loads(json.dumps(event, ensure_ascii=True))
        for key, value in list(safe_event.items()):
            if isinstance(value, str):
                safe_event[key] = redact_text(value)
        path = self._directory / f"{session_id}.jsonl"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(safe_event, ensure_ascii=True) + "\n")
