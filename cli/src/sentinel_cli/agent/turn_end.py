"""Post-turn pipeline: hooks, memory extract, away summary, magic docs, dream."""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from sentinel_cli.config import AppConfig
from sentinel_cli.hooks import HookManager
from sentinel_cli.memory import append_extract, apply_magic_docs, maybe_run_dream
from sentinel_cli.memory.paths import ensure_within_memory_root, resolve_memory_root
from sentinel_cli.redaction import redact_text
from sentinel_cli.session import SessionState, SessionStore, TrajectoryRecorder

logger = logging.getLogger(__name__)


class ProviderLike(Protocol):
    def complete(self, request: Any) -> Any: ...


@dataclass(slots=True)
class TurnEndContext:
    session: SessionState
    cwd: str
    interactive: bool
    stopped_reason: str
    profile: str
    provider: ProviderLike | None


def _pipeline_allowed(config: AppConfig, *, interactive: bool) -> bool:
    if not config.turn_pipeline.enabled:
        return False
    if interactive:
        return True
    if config.memory.allow_non_interactive:
        return True
    return False


def _build_away_summary(session: SessionState, config: AppConfig) -> str:
    """Deterministic one-line summary from the latest user + assistant content."""

    user_text = ""
    assistant_text = ""
    for message in reversed(session.messages):
        role = getattr(message.role, "value", message.role)
        if role == "user" and not user_text:
            user_text = (message.content or "").replace("\n", " ").strip()
        if role == "assistant" and not assistant_text:
            assistant_text = (message.content or "").replace("\n", " ").strip()
        if user_text and assistant_text:
            break
    combined = f"{user_text} => {assistant_text}".strip(" =>")
    combined = redact_text(combined)
    limit = max(32, config.away.max_chars)
    if len(combined) > limit:
        combined = combined[: limit - 3] + "..."
    return combined


def _append_session_memory_file(
    config: AppConfig,
    *,
    cwd: str,
    session_id: str,
    line: str,
) -> Path | None:
    if not config.memory.enabled or not config.semantic_compaction.persist_session_memory_path:
        return None
    root = resolve_memory_root(config.memory, cwd=cwd)
    root.mkdir(parents=True, exist_ok=True)
    path = ensure_within_memory_root(root, root / config.session.session_memory_filename)
    safe = redact_text(line)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"- {session_id}: {safe}\n")
    return path


def run_turn_end_pipeline(
    config: AppConfig,
    *,
    hook_manager: HookManager,
    session_store: SessionStore,
    trajectory: TrajectoryRecorder,
    ctx: TurnEndContext,
) -> None:
    """Execute turn-end work synchronously (caller may delegate to a thread)."""

    if not _pipeline_allowed(config, interactive=ctx.interactive):
        logger.debug(
            "turn_pipeline_skipped",
            extra={"interactive": ctx.interactive, "reason": "policy"},
        )
        return

    session = ctx.session

    payload = {
        "phase": "post_turn",
        "session_id": session.session_id,
        "cwd": ctx.cwd,
        "stopped_reason": ctx.stopped_reason,
        "profile": ctx.profile,
        "interactive": ctx.interactive,
    }
    hook_manager.run("post_turn", payload)

    if config.memory.enabled and config.memory.extract_on_turn_end:
        pre = hook_manager.run(
            "pre_memory",
            {
                **payload,
                "memory_action": "extract",
            },
        )
        if not pre.blocked:
            append_extract(config, cwd=ctx.cwd, session_id=session.session_id, messages=session.messages)
            hook_manager.run(
                "post_memory",
                {
                    **payload,
                    "memory_action": "extract",
                    "status": "ok",
                },
            )

    if config.away.enabled and ctx.interactive:
        summary = _build_away_summary(session, config)
        session.away_summary = summary
        _append_session_memory_file(
            config,
            cwd=ctx.cwd,
            session_id=session.session_id,
            line=f"away: {summary}",
        )

    if config.magic_docs.enabled:
        magic_summary = session.away_summary or _build_away_summary(session, config)
        apply_magic_docs(config, cwd=ctx.cwd, summary=magic_summary)

    dream_payload: dict[str, Any] | None = None
    if config.dream.enabled:
        dream_payload = maybe_run_dream(
            config,
            cwd=ctx.cwd,
            session_id=session.session_id,
            completer=ctx.provider,
            increment_sessions=True,
        )

    trajectory.append(
        session.session_id,
        {
            "event": "turn_end_pipeline",
            "stopped_reason": ctx.stopped_reason,
            "dream": dream_payload,
        },
    )

    session_store.save(session)


def schedule_turn_end_pipeline(
    config: AppConfig,
    *,
    hook_manager: HookManager,
    session_store: SessionStore,
    trajectory: TrajectoryRecorder,
    ctx: TurnEndContext,
) -> None:
    """Run pipeline in-process or background thread based on config."""

    if not config.turn_pipeline.enabled:
        return

    if config.turn_pipeline.run_in_background:
        thread = threading.Thread(
            target=run_turn_end_pipeline,
            kwargs={
                "config": config,
                "hook_manager": hook_manager,
                "session_store": session_store,
                "trajectory": trajectory,
                "ctx": ctx,
            },
            name="sentinel-turn-end",
            daemon=True,
        )
        thread.start()
        return

    run_turn_end_pipeline(
        config,
        hook_manager=hook_manager,
        session_store=session_store,
        trajectory=trajectory,
        ctx=ctx,
    )
