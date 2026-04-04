from sentinel_cli.config import ContextWindowSettings
from sentinel_cli.llm.context import ContextWindowPolicy
from sentinel_cli.llm.types import ChatMessage, MessageRole


def test_context_policy_truncates_when_threshold_is_exceeded() -> None:
    policy = ContextWindowPolicy(
        ContextWindowSettings(
            max_input_tokens=10,
            warn_ratio=0.5,
            strategy="truncate",
            preserve_recent_messages=1,
        )
    )

    result = policy.apply(
        [
            ChatMessage(role=MessageRole.USER, content="a" * 30),
            ChatMessage(role=MessageRole.USER, content="b" * 30),
        ]
    )

    assert result.trimmed is True
    assert len(result.messages) == 1
    assert result.warning is not None
