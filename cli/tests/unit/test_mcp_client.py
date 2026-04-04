from __future__ import annotations

import json
import sys
from pathlib import Path

from sentinel_cli.config import AppConfig, MCPServerConfig
from sentinel_cli.llm.types import ToolCall
from sentinel_cli.tools import MCPClientManager, ToolRegistry
from sentinel_cli.tools.mcp import namespace_tool_name


SERVER_SCRIPT = """\
import json
import sys

for line in sys.stdin:
    payload = json.loads(line)
    method = payload.get("method")
    if method == "initialize":
        sys.stdout.write(json.dumps({
            "jsonrpc": "2.0",
            "id": payload["id"],
            "result": {
                "protocolVersion": "2025-03-26",
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "demo", "version": "1.0.0"}
            }
        }) + "\\n")
        sys.stdout.flush()
    elif method == "notifications/initialized":
        continue
    elif method == "tools/list":
        sys.stdout.write(json.dumps({
            "jsonrpc": "2.0",
            "id": payload["id"],
            "result": {
                "tools": [{
                    "name": "echo",
                    "description": "Echo input text",
                    "inputSchema": {
                        "type": "object",
                        "properties": {"text": {"type": "string"}},
                        "required": ["text"]
                    }
                }]
            }
        }) + "\\n")
        sys.stdout.flush()
    elif method == "tools/call":
        text = payload["params"]["arguments"]["text"]
        sys.stdout.write(json.dumps({
            "jsonrpc": "2.0",
            "id": payload["id"],
            "result": {
                "content": [{"type": "text", "text": f"echo:{text}"}],
                "isError": False
            }
        }) + "\\n")
        sys.stdout.flush()
"""


def _write_server_script(tmp_path: Path) -> Path:
    script = tmp_path / "fake_mcp_server.py"
    script.write_text(SERVER_SCRIPT, encoding="utf-8")
    return script


def test_mcp_degrades_without_extra(monkeypatch) -> None:
    config = AppConfig()
    config.mcp.enabled = True
    config.mcp.servers = [MCPServerConfig(name="demo", command=["python3", "fake.py"])]
    monkeypatch.setattr("sentinel_cli.tools.mcp._mcp_extra_available", lambda: False)
    result = MCPClientManager(config.mcp).discover_tools()
    assert result.available is False
    assert ".[mcp]" in result.message


def test_mcp_discovery_and_registry_execution(monkeypatch, tmp_path: Path) -> None:
    script = _write_server_script(tmp_path)
    config = AppConfig()
    config.tools.auto_approve = True
    config.tools.approval_mode = "auto"
    config.mcp.enabled = True
    config.mcp.servers = [
        MCPServerConfig(
            name="demo",
            transport="stdio",
            command=[sys.executable, str(script)],
        )
    ]
    monkeypatch.setattr("sentinel_cli.tools.mcp._mcp_extra_available", lambda: True)

    manager = MCPClientManager(config.mcp)
    discovery = manager.discover_tools()
    assert discovery.available is True
    assert discovery.tools[0].namespaced_name == namespace_tool_name("demo", "echo")

    registry = ToolRegistry(config=config)
    definitions = {tool.name for tool in registry.definitions()}
    assert namespace_tool_name("demo", "echo") in definitions

    result = registry.execute_tool_call(
        tool_call=ToolCall(
            id="1",
            name=namespace_tool_name("demo", "echo"),
            arguments_json=json.dumps({"text": "hello"}),
        ),
        cwd=str(tmp_path),
        session_id="sess",
        interactive=False,
    )
    assert result.ok is True
    assert result.message == "echo:hello"
