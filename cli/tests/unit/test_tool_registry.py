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


def test_write_tool_respects_memory_write_jail(tmp_path) -> None:
    config = AppConfig()
    config.tools.auto_approve = True
    config.tools.approval_mode = "auto"
    config.memory.enabled = True
    config.memory.enforce_write_jail = True
    (tmp_path / ".sentinel" / "memory").mkdir(parents=True)
    registry = ToolRegistry(config=config, hook_manager=HookManager(config.hooks))

    bad = registry.execute_tool_call(
        ToolCall(
            id="1",
            name="write_file",
            arguments_json=json.dumps({"path": "evil.txt", "content": "no"}),
        ),
        cwd=str(tmp_path),
        session_id="sess",
        interactive=False,
    )
    assert bad.ok is False
    assert bad.code == "MEMORY_JAIL"

    good = registry.execute_tool_call(
        ToolCall(
            id="2",
            name="write_file",
            arguments_json=json.dumps({"path": ".sentinel/memory/note.txt", "content": "ok"}),
        ),
        cwd=str(tmp_path),
        session_id="sess",
        interactive=False,
    )
    assert good.ok is True
    assert (tmp_path / ".sentinel" / "memory" / "note.txt").read_text(encoding="utf-8") == "ok"


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


def test_registry_exposes_observability_tools() -> None:
    registry = ToolRegistry(config=AppConfig(), hook_manager=HookManager(AppConfig().hooks))

    names = {definition.name for definition in registry.definitions()}

    assert "obs_metric_query" in names
    assert "obs_logs_query" in names
    assert "obs_traces_search" in names
    assert "obs_trace_get" in names


def test_registry_parses_observability_tool_args() -> None:
    registry = ToolRegistry(config=AppConfig(), hook_manager=HookManager(AppConfig().hooks))

    parsed = registry.parse_tool_call(
        ToolCall(
            id="1",
            name="obs_logs_query",
            arguments_json=json.dumps({"service": "gateway", "limit": 5}),
        )
    )

    assert parsed.tool.name == "obs_logs_query"
    assert parsed.arguments.service == "gateway"
    assert parsed.arguments.limit == 5
