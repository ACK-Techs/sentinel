from __future__ import annotations

import json

from sentinel_cli.agent import AgentLoop
from sentinel_cli.config import AppConfig, ResolvedProfile
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.types import CompletionResult, ToolCall
from sentinel_cli.session import SessionStore, TrajectoryRecorder


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0

    def complete(self, request):
        self.calls += 1
        if self.calls == 1:
            return CompletionResult(
                text="Dosyayi okuyorum.",
                tool_calls=[ToolCall(id="t1", name="read_file", arguments_json=json.dumps({"path": "info.txt"}))],
                provider_name="fake",
            )
        return CompletionResult(text="Bitti.", provider_name="fake")

    def stream(self, request):
        raise NotImplementedError


def test_agent_loop_executes_tool_and_finishes(tmp_path) -> None:
    (tmp_path / "info.txt").write_text("grafana ok", encoding="utf-8")
    config = AppConfig()
    config.tools.auto_approve = True
    config.tools.approval_mode = "auto"
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    store = SessionStore(config.session)
    trajectory = TrajectoryRecorder(config.session.trajectory_directory, enabled=True)
    profile = ResolvedProfile(
        name="local",
        provider="openai",
        model="mock",
        base_url="http://127.0.0.1:11434/v1",
        api_key=None,
        api_key_env=None,
        timeout_sec=30,
        supports_tools=True,
    )
    loop = AgentLoop(
        config=config,
        resolved_profile=profile,
        provider=FakeProvider(),
        session_store=store,
        trajectory=trajectory,
        hook_manager=HookManager(config.hooks),
    )

    result = loop.run(prompt="dosyayi oku", cwd=str(tmp_path), interactive=False)
    assert result.output_text == "Bitti."
    assert result.turns_used == 2


def test_agent_loop_warns_on_profile_mismatch(tmp_path) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    store = SessionStore(config.session)
    session = store.create(profile="cloud", provider="openai")
    profile = ResolvedProfile(
        name="local",
        provider="openai",
        model="mock",
        base_url="http://127.0.0.1:11434/v1",
        api_key=None,
        api_key_env=None,
        timeout_sec=30,
        supports_tools=True,
    )
    loop = AgentLoop(
        config=config,
        resolved_profile=profile,
        provider=FakeProvider(),
        session_store=store,
        trajectory=TrajectoryRecorder(config.session.trajectory_directory, enabled=False),
        hook_manager=HookManager(config.hooks),
    )

    result = loop.run(
        prompt="selam",
        cwd=str(tmp_path),
        interactive=False,
        session_id=session.session_id,
        resume=True,
    )
    assert any("yeni oturum" in warning.lower() for warning in result.warnings)
