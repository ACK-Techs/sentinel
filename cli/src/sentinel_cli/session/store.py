"""File-based session persistence."""

from __future__ import annotations

import json
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from sentinel_cli.config import SessionSettings
from sentinel_cli.llm.types import ChatMessage


@dataclass(slots=True)
class SessionState:
    session_id: str
    profile: str
    provider: str
    messages: list[ChatMessage]
    created_at: str
    grafana_context_snapshot: str | None = None
    observability_context_snapshot: str | None = None
    away_summary: str | None = None
    compaction_note: str | None = None


class SessionStore:
    """Persist sessions as JSON files."""

    def __init__(self, settings: SessionSettings) -> None:
        self._settings = settings
        self._settings.directory.mkdir(parents=True, exist_ok=True)
        self._settings.trajectory_directory.mkdir(parents=True, exist_ok=True)

    def create(self, *, profile: str, provider: str) -> SessionState:
        session = SessionState(
            session_id=uuid.uuid4().hex[:12],
            profile=profile,
            provider=provider,
            messages=[],
            created_at=datetime.now(UTC).isoformat(),
            grafana_context_snapshot=None,
            observability_context_snapshot=None,
        )
        self.save(session)
        return session

    def path_for(self, session_id: str) -> Path:
        return self._settings.directory / f"{session_id}.json"

    def save(self, session: SessionState) -> None:
        path = self.path_for(session.session_id)
        payload = {
            "session_id": session.session_id,
            "profile": session.profile,
            "provider": session.provider,
            "created_at": session.created_at,
            "grafana_context_snapshot": session.grafana_context_snapshot,
            "observability_context_snapshot": session.observability_context_snapshot,
            "away_summary": session.away_summary,
            "compaction_note": session.compaction_note,
            "messages": [message.model_dump(mode="json") for message in session.messages],
        }
        path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")

    def load(self, session_id: str) -> SessionState:
        path = self.path_for(session_id)
        payload = json.loads(path.read_text(encoding="utf-8"))
        return SessionState(
            session_id=payload["session_id"],
            profile=payload["profile"],
            provider=payload["provider"],
            created_at=payload["created_at"],
            grafana_context_snapshot=payload.get("grafana_context_snapshot", None),
            observability_context_snapshot=payload.get("observability_context_snapshot", None),
            away_summary=payload.get("away_summary", None),
            compaction_note=payload.get("compaction_note", None),
            messages=[ChatMessage.model_validate(item) for item in payload.get("messages", [])],
        )
