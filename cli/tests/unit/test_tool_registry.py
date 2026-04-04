from __future__ import annotations

import json

from sentinel_cli.config import AppConfig
from sentinel_cli.hooks import HookManager
from sentinel_cli.llm.types import ToolCall
from sentinel_cli.tools.registry import ToolRegistry


def test_unknown_tool_is_rejected() -> None:
    registry = ToolRegistry(config=AppConfig(), hook_manager=HookManager(AppConfig().hooks))
    try:
        registry.parse_tool_call(ToolCall(id="1", name="missing", arguments_json="{}"))
    except ValueError as exc:
        assert "Bilinmeyen tool" in str(exc)
    else:
        raise AssertionError("ValueError bekleniyordu")


def test_invalid_tool_json_is_rejected() -> None:
    registry = ToolRegistry(config=AppConfig(), hook_manager=HookManager(AppConfig().hooks))
    try:
        registry.parse_tool_call(ToolCall(id="1", name="read_file", arguments_json="{"))
    except ValueError as exc:
        assert "JSON" in str(exc)
    else:
        raise AssertionError("ValueError bekleniyordu")


def test_write_tool_respects_auto_approval(tmp_path) -> None:
    config = AppConfig()
    config.tools.auto_approve = True
    config.tools.approval_mode = "auto"
    registry = ToolRegistry(config=config, hook_manager=HookManager(config.hooks))
    target = tmp_path / "note.txt"
    result = registry.execute_tool_call(
        ToolCall(
            id="1",
            name="write_file",
            arguments_json=json.dumps({"path": "note.txt", "content": "hello"}),
        ),
        cwd=str(tmp_path),
        session_id="sess",
        interactive=False,
    )
    assert result.ok is True
    assert target.read_text(encoding="utf-8") == "hello"
