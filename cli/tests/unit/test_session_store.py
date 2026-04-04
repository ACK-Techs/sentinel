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
    store.save(session)

    loaded = store.load(session.session_id)
    assert loaded.profile == "local"
    assert loaded.messages[0].content == "hello"


def test_trajectory_redacts_tokens(tmp_path) -> None:
    recorder = TrajectoryRecorder(tmp_path, enabled=True)
    recorder.append("sess", {"message": "mail me at a@b.com token sk-secret-12345678"})
    content = (tmp_path / "sess.jsonl").read_text(encoding="utf-8")
    assert "[redacted-email]" in content
    assert "[redacted-token]" in content
    assert "[redacted-token]" in redact_text("sk-secret-12345678")
