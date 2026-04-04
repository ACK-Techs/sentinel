"""Structured stderr logging with secret redaction."""

from __future__ import annotations

import json
import logging
import re
import sys
from typing import Any


SECRET_PATTERNS = [
    re.compile(r"(Bearer\s+)[A-Za-z0-9._-]+", re.IGNORECASE),
    re.compile(r"(sk-[A-Za-z0-9]+)"),
    re.compile(r"(api[_-]?key[\"'=:\s]+)([A-Za-z0-9._-]+)", re.IGNORECASE),
]


def redact_secrets(value: str) -> str:
    redacted = value
    for pattern in SECRET_PATTERNS:
        redacted = pattern.sub(lambda match: match.group(1) + "***" if match.lastindex else "***", redacted)
    return redacted


class JsonLogFormatter(logging.Formatter):
    """Emit one JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "level": record.levelname,
            "event": record.msg if isinstance(record.msg, str) else str(record.msg),
            "logger": record.name,
        }
        for field in ("session_id", "provider", "turn", "tool_name", "event_name", "duration_ms"):
            if hasattr(record, field):
                payload[field] = getattr(record, field)
        if record.exc_info:
            payload["error"] = self.formatException(record.exc_info)
        return redact_secrets(json.dumps(payload, ensure_ascii=True))


def configure_logging(level: str) -> logging.Logger:
    logger = logging.getLogger("sentinel_cli")
    logger.handlers.clear()
    logger.setLevel(getattr(logging, level.upper(), logging.INFO))
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonLogFormatter())
    logger.addHandler(handler)
    logger.propagate = False
    return logger
