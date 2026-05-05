from __future__ import annotations

import json
from pathlib import Path

from sentinel_cli.agent.turn_end import (
    TurnEndContext,
    _memory_side_effects_allowed,
    run_turn_end_pipeline,
)
from sentinel_cli.config import AppConfig, load_config
from sentinel_cli.llm.types import ChatMessage, MessageRole
from sentinel_cli.memory.dream import maybe_run_dream
from sentinel_cli.memory.extract import append_extract
from sentinel_cli.memory.paths import resolve_memory_root
from sentinel_cli.session import SessionStore, TrajectoryRecorder
from sentinel_cli.tools.bash import BashArgs, BashTool
from sentinel_cli.tools.base import ToolContext


def test_resolve_memory_root_project_policy(tmp_path: Path) -> None:
    config = AppConfig()
    config.memory.policy = "project"
    root = resolve_memory_root(config.memory, cwd=str(tmp_path))
    assert root == tmp_path / ".sentinel" / "memory"


def test_memory_side_effects_bare_mode() -> None:
    config = AppConfig()
    assert _memory_side_effects_allowed(config, interactive=True) is True
    assert _memory_side_effects_allowed(config, interactive=False) is False
    config.memory.allow_non_interactive = True
    assert _memory_side_effects_allowed(config, interactive=False) is True


def test_append_extract_redacts_and_writes_jsonl(tmp_path: Path) -> None:
    config = AppConfig()
    config.memory.enabled = True
    config.memory.extract_on_turn_end = True
    config.memory.policy = "project"

    messages = [
        ChatMessage(role=MessageRole.USER, content="Use token sk-abcdefghijklm in curl"),
        ChatMessage(role=MessageRole.ASSISTANT, content="ok"),
    ]
    path = append_extract(config, cwd=str(tmp_path), session_id="sess1", messages=messages)
    assert path is not None
    line = path.read_text(encoding="utf-8").strip()
    payload = json.loads(line)
    blob = json.dumps(payload["summary"])
    assert "curl" in blob or "curl" in payload["summary"].get("assistant", [])
    assert "sk-" not in blob
    assert "tools" in payload["summary"]


def test_dream_thresholds_skip_without_completer(tmp_path: Path) -> None:
    config = AppConfig()
    config.memory.enabled = True
    config.dream.enabled = True
    config.dream.min_sessions = 1
    config.dream.min_hours_between = 0
    # previous run: allow hours check
    out = maybe_run_dream(
        config,
        cwd=str(tmp_path),
        session_id="s1",
        completer=None,
        increment_sessions=True,
    )
    assert out is not None
    assert out.get("status") in {"ok", "skipped"}


def test_env_overlays_memory_and_dream() -> None:
    config = load_config(
        env={
            "SENTINEL_AUTO_MEMORY": "true",
            "SENTINEL_AUTO_DREAM": "1",
            "SENTINEL_DREAM_MIN_HOURS": "3",
            "SENTINEL_DREAM_MIN_SESSIONS": "2",
            "SENTINEL_MEMORY_ALLOW_NON_INTERACTIVE": "on",
            "SENTINEL_BASH_READ_ONLY": "true",
        }
    )
    assert config.memory.enabled is True
    assert config.dream.enabled is True
    assert config.dream.min_hours_between == 3
    assert config.dream.min_sessions == 2
    assert config.memory.allow_non_interactive is True
    assert config.tools.bash_read_only is True


def test_bash_read_only_blocks_find_exec() -> None:
    tool = BashTool(default_timeout_sec=5, max_output_chars=100, read_only=True)
    res = tool.execute(
        BashArgs(command='find . -name "*.txt" -delete'),
        ToolContext(cwd="/", session_id="s", interactive=False, auto_approve=True),
    )
    assert res.ok is False
    assert res.code == "READ_ONLY"


def test_bash_read_only_blocks_pipe() -> None:
    tool = BashTool(default_timeout_sec=5, max_output_chars=100, read_only=True)
    res = tool.execute(
        BashArgs(command="cat x | wc"),
        ToolContext(cwd="/", session_id="s", interactive=False, auto_approve=True),
    )
    assert res.ok is False
    assert res.code == "READ_ONLY"


def test_turn_end_runs_post_turn_hook(tmp_path: Path) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "traj"
    store = SessionStore(config.session)
    session = store.create(profile="local", provider="openai")
    session.messages.append(ChatMessage(role=MessageRole.USER, content="hi"))

    seen: list[str] = []

    class StubHooks:
        def run(self, phase, payload):
            seen.append(phase)
            from sentinel_cli.hooks import HookResult

            return HookResult()

    trajectory = TrajectoryRecorder(tmp_path / "traj", enabled=False)
    ctx = TurnEndContext(
        session=session,
        cwd=str(tmp_path),
        interactive=True,
        stopped_reason="final_answer",
        profile="local",
        provider=None,
    )
    run_turn_end_pipeline(
        config,
        hook_manager=StubHooks(),  # type: ignore[arg-type]
        session_store=store,
        trajectory=trajectory,
        ctx=ctx,
    )
    assert "post_turn" in seen


def test_turn_end_skips_extract_when_non_interactive_by_default(tmp_path: Path) -> None:
    config = AppConfig()
    config.memory.enabled = True
    config.memory.extract_on_turn_end = True
    config.memory.policy = "project"
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "traj"
    store = SessionStore(config.session)
    session = store.create(profile="local", provider="openai")
    session.messages.append(ChatMessage(role=MessageRole.USER, content="secret api_key=abc"))

    extract_path = tmp_path / ".sentinel" / "memory" / "extract.jsonl"

    class StubHooks:
        def run(self, phase, payload):
            from sentinel_cli.hooks import HookResult

            return HookResult()

    trajectory = TrajectoryRecorder(tmp_path / "traj", enabled=False)
    ctx = TurnEndContext(
        session=session,
        cwd=str(tmp_path),
        interactive=False,
        stopped_reason="final_answer",
        profile="local",
        provider=None,
    )
    run_turn_end_pipeline(
        config,
        hook_manager=StubHooks(),  # type: ignore[arg-type]
        session_store=store,
        trajectory=trajectory,
        ctx=ctx,
    )
    assert not extract_path.exists()


def test_session_state_roundtrip_new_fields(tmp_path: Path) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "traj"
    store = SessionStore(config.session)
    session = store.create(profile="local", provider="openai")
    session.away_summary = "summary line"
    session.compaction_note = "trimmed"
    store.save(session)
    loaded = store.load(session.session_id)
    assert loaded.away_summary == "summary line"
    assert loaded.compaction_note == "trimmed"
