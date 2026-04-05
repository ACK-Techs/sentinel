from __future__ import annotations

import json
import pytest

from sentinel_cli.agent import AgentLoop
from sentinel_cli.config import AppConfig, ResolvedProfile
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.types import ChatRequest, CompletionResult, ToolCall
from sentinel_cli.session import SessionStore, TrajectoryRecorder


class FakeProvider:
    def __init__(self) -> None:
        self.calls = 0
        self.requests: list[ChatRequest] = []

    def complete(self, request):
        self.calls += 1
        self.requests.append(request)
        if self.calls == 1:
            return CompletionResult(
                text="Dosyayi okuyorum.",
                tool_calls=[ToolCall(id="t1", name="read_file", arguments_json=json.dumps({"path": "info.txt"}))],
                provider_name="fake",
            )
        return CompletionResult(text="Bitti.", provider_name="fake")

    def stream(self, request):
        raise NotImplementedError


class SingleReplyProvider:
    def __init__(self) -> None:
        self.requests: list[ChatRequest] = []

    def complete(self, request):
        self.requests.append(request)
        return CompletionResult(text="Tamam.", provider_name="fake")

    def stream(self, request):
        raise NotImplementedError


def _profile() -> ResolvedProfile:
    return ResolvedProfile(
        name="local",
        provider="openai",
        model="mock",
        base_url="http://127.0.0.1:11434/v1",
        api_key=None,
        api_key_env=None,
        timeout_sec=30,
        supports_tools=True,
    )


def test_agent_loop_executes_tool_and_finishes(tmp_path) -> None:
    (tmp_path / "info.txt").write_text("grafana ok", encoding="utf-8")
    config = AppConfig()
    config.tools.auto_approve = True
    config.tools.approval_mode = "auto"
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    store = SessionStore(config.session)
    trajectory = TrajectoryRecorder(config.session.trajectory_directory, enabled=True)
    loop = AgentLoop(
        config=config,
        resolved_profile=_profile(),
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
    loop = AgentLoop(
        config=config,
        resolved_profile=_profile(),
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


def test_agent_loop_sets_grafana_snapshot_once_and_injects_system_prompt(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    config.agent.grafana_context_in_repl = True
    store = SessionStore(config.session)
    provider = SingleReplyProvider()
    calls: list[dict[str, str]] = []

    class FakeGrafanaResult:
        def to_dict(self) -> dict[str, str]:
            return {"status": "skipped", "message": "mocked"}

    def fake_check(settings, *, env):
        calls.append(env)
        return FakeGrafanaResult()

    monkeypatch.setattr("sentinel_cli.agent.loop.check_grafana_connection", fake_check)

    loop = AgentLoop(
        config=config,
        resolved_profile=_profile(),
        provider=provider,
        session_store=store,
        trajectory=TrajectoryRecorder(config.session.trajectory_directory, enabled=False),
        hook_manager=HookManager(config.hooks),
    )

    result = loop.run(prompt="durum nedir", cwd=str(tmp_path), interactive=False)
    loaded = store.load(result.session_id)

    assert len(calls) == 1
    assert loaded.grafana_context_snapshot == json.dumps(
        {"status": "skipped", "message": "mocked"}, ensure_ascii=True
    )
    assert "Grafana operasyonel ozeti asagidadir" in provider.requests[0].system_prompt
    assert loaded.messages[0].content == "durum nedir"


def test_agent_loop_skips_grafana_snapshot_when_flag_disabled(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    config.agent.grafana_context_in_repl = False
    store = SessionStore(config.session)
    provider = SingleReplyProvider()

    monkeypatch.setattr(
        "sentinel_cli.agent.loop.check_grafana_connection",
        lambda *args, **kwargs: pytest.fail("Grafana check cagrilmamali"),
    )

    loop = AgentLoop(
        config=config,
        resolved_profile=_profile(),
        provider=provider,
        session_store=store,
        trajectory=TrajectoryRecorder(config.session.trajectory_directory, enabled=False),
        hook_manager=HookManager(config.hooks),
    )

    result = loop.run(prompt="selam", cwd=str(tmp_path), interactive=False)
    loaded = store.load(result.session_id)

    assert loaded.grafana_context_snapshot is None
    assert "Grafana operasyonel ozeti asagidadir" not in provider.requests[0].system_prompt


def test_agent_loop_does_not_recheck_when_snapshot_already_exists(
    tmp_path, monkeypatch: pytest.MonkeyPatch
) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    config.agent.grafana_context_in_repl = True
    store = SessionStore(config.session)
    session = store.create(profile="local", provider="openai")
    session.grafana_context_snapshot = json.dumps({"status": "ok"}, ensure_ascii=True)
    store.save(session)
    provider = SingleReplyProvider()

    monkeypatch.setattr(
        "sentinel_cli.agent.loop.check_grafana_connection",
        lambda *args, **kwargs: pytest.fail("Mevcut snapshot varken HTTP cagrisi olmamali"),
    )

    loop = AgentLoop(
        config=config,
        resolved_profile=_profile(),
        provider=provider,
        session_store=store,
        trajectory=TrajectoryRecorder(config.session.trajectory_directory, enabled=False),
        hook_manager=HookManager(config.hooks),
    )

    loop.run(
        prompt="devam et",
        cwd=str(tmp_path),
        interactive=False,
        session_id=session.session_id,
        resume=True,
    )

    assert '{"status": "ok"}' in provider.requests[0].system_prompt
