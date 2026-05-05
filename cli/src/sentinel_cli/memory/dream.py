"""Dream / consolidation scheduling with file lock and optional LLM call."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Any, Callable, Protocol

from sentinel_cli.config import AppConfig
from sentinel_cli.llm.types import ChatMessage, ChatRequest, CompletionResult, MessageRole
from sentinel_cli.memory.paths import ensure_within_memory_root, resolve_memory_root
from sentinel_cli.redaction import redact_text


class Completer(Protocol):
    def complete(self, request: ChatRequest) -> CompletionResult: ...


@dataclass(slots=True)
class DreamState:
    last_run_at: str | None
    sessions_since_dream: int


def _state_path(memory_root: Path) -> Path:
    return memory_root / "dream_state.json"


def _lock_path(memory_root: Path) -> Path:
    return memory_root / ".dream.lock"


def load_state(memory_root: Path) -> DreamState:
    path = _state_path(memory_root)
    if not path.exists():
        return DreamState(last_run_at=None, sessions_since_dream=0)
    raw = json.loads(path.read_text(encoding="utf-8"))
    return DreamState(
        last_run_at=raw.get("last_run_at"),
        sessions_since_dream=int(raw.get("sessions_since_dream", 0)),
    )


def save_state(memory_root: Path, state: DreamState) -> None:
    path = _state_path(memory_root)
    payload = {
        "last_run_at": state.last_run_at,
        "sessions_since_dream": state.sessions_since_dream,
    }
    path.write_text(json.dumps(payload, ensure_ascii=True, indent=2), encoding="utf-8")


def try_acquire_lock(lock_path: Path, *, stale_after_sec: int) -> bool:
    """Non-blocking lock file; steal stale locks."""

    if lock_path.exists():
        try:
            age_sec = max(0, int(datetime.now(UTC).timestamp() - lock_path.stat().st_mtime))
        except OSError:
            age_sec = 0
        if age_sec < stale_after_sec:
            return False
        try:
            lock_path.unlink()
        except OSError:
            return False

    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        try:
            os.write(fd, str(os.getpid()).encode("ascii"))
        finally:
            os.close(fd)
        return True
    except FileExistsError:
        return False


def release_lock(lock_path: Path) -> None:
    try:
        lock_path.unlink()
    except OSError:
        pass


def maybe_run_dream(
    config: AppConfig,
    *,
    cwd: str,
    session_id: str,
    completer: Completer | None,
    increment_sessions: bool = True,
) -> dict[str, Any] | None:
    """Run consolidation if thresholds met. Returns status dict or None if skipped."""

    if not config.memory.enabled or not config.dream.enabled:
        return None

    memory_root = resolve_memory_root(config.memory, cwd=cwd)
    memory_root.mkdir(parents=True, exist_ok=True)
    ensure_within_memory_root(memory_root, memory_root)

    state = load_state(memory_root)
    if increment_sessions:
        state.sessions_since_dream += 1

    now = datetime.now(UTC)
    last_run = None
    if state.last_run_at:
        try:
            last_run = datetime.fromisoformat(state.last_run_at)
            if last_run.tzinfo is None:
                last_run = last_run.replace(tzinfo=UTC)
        except ValueError:
            last_run = None

    hours_ok = True
    if last_run is not None:
        hours_ok = now - last_run >= timedelta(hours=config.dream.min_hours_between)

    sessions_ok = state.sessions_since_dream >= config.dream.min_sessions

    save_state(memory_root, state)

    if not (hours_ok and sessions_ok):
        return {"status": "skipped", "reason": "thresholds_not_met"}

    lock_file = _lock_path(memory_root)
    if not try_acquire_lock(lock_file, stale_after_sec=config.dream.lock_stale_sec):
        return {"status": "skipped", "reason": "lock_held"}

    try:
        index_path = ensure_within_memory_root(memory_root, memory_root / "index.md")
        snippet = f"## Consolidation {now.isoformat()}\nSession `{session_id}`\n"
        if completer is not None:
            request = ChatRequest(
                messages=[
                    ChatMessage(
                        role=MessageRole.USER,
                        content=(
                            "Asagidaki bellek ozetini tek paragrafta birlestir; "
                            "kisisel/sir bilgi yazma; Turkce ve kisa tut.\n"
                            f"Oturum: {session_id}"
                        ),
                    )
                ],
                system_prompt="Sentinel bellek birlestirme yardimcisi.",
                tools=[],
            )
            result = completer.complete(request)
            body = redact_text(result.text or "").strip()
            snippet += body + "\n"
        else:
            snippet += "_Consolidation skipped: no completer._\n"

        with index_path.open("a", encoding="utf-8") as handle:
            handle.write(snippet + "\n")

        state = load_state(memory_root)
        state.last_run_at = now.isoformat()
        state.sessions_since_dream = 0
        save_state(memory_root, state)
        return {"status": "ok", "index": str(index_path)}
    finally:
        release_lock(lock_file)
