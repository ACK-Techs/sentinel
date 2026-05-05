from sentinel_cli.config import AppConfig
from sentinel_cli.llm.types import ChatMessage, MessageRole
from sentinel_cli.session import SessionStore, TrajectoryRecorder, redact_text


def test_session_store_roundtrip(tmp_path) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    store = SessionStore(config.session)
    session = store.create(profile="local", provider="openai")
    session.messages.append(ChatMessage(role=MessageRole.USER, content="hello"))
    session.observability_context_snapshot = '{"gateway":{"status":"ok"}}'
    store.save(session)

    loaded = store.load(session.session_id)
    assert loaded.profile == "local"
    assert loaded.messages[0].content == "hello"
    assert loaded.observability_context_snapshot == '{"gateway":{"status":"ok"}}'


def test_session_store_loads_missing_grafana_snapshot_for_legacy_files(tmp_path) -> None:
    config = AppConfig()
    config.session.directory = tmp_path / "sessions"
    config.session.trajectory_directory = tmp_path / "trajectories"
    store = SessionStore(config.session)
    legacy_path = store.path_for("legacy123")
    legacy_path.write_text(
        """
{
  "session_id": "legacy123",
  "profile": "local",
  "provider": "openai",
  "created_at": "2026-04-05T00:00:00+00:00",
  "messages": []
}
""".strip(),
        encoding="utf-8",
    )

    loaded = store.load("legacy123")

    assert loaded.grafana_context_snapshot is None
    assert loaded.observability_context_snapshot is None


def test_trajectory_redacts_tokens(tmp_path) -> None:
    recorder = TrajectoryRecorder(tmp_path, enabled=True)
    recorder.append("sess", {"message": "mail me at a@b.com token sk-secret-12345678"})
    content = (tmp_path / "sess.jsonl").read_text(encoding="utf-8")
    assert "[redacted-email]" in content
    assert "[redacted-token]" in content
    assert "[redacted-token]" in redact_text("sk-secret-12345678")
    assert "[redacted-aws-key-id]" in redact_text("AKIA0123456789ABCDEF")
