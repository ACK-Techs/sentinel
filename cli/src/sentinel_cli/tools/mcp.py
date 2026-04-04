"""Optional MCP stdio discovery and tool execution."""

from __future__ import annotations

import importlib.util
import json
import selectors
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from pydantic import BaseModel, ConfigDict

from sentinel_cli.config import MCPServerConfig, MCPSettings
from sentinel_cli.llm.types import ToolDefinition
from sentinel_cli.tools.base import ToolContext, ToolResult

SUPPORTED_MCP_TRANSPORTS = ("stdio",)
MCP_PROTOCOL_VERSION = "2025-03-26"


def _mcp_extra_available() -> bool:
    return importlib.util.find_spec("mcp") is not None


def namespace_tool_name(server_name: str, tool_name: str, prefix: str | None = None) -> str:
    safe_prefix = prefix or f"mcp_{server_name}"
    return f"{safe_prefix}_{tool_name}"


class MCPToolArguments(BaseModel):
    model_config = ConfigDict(extra="allow")


@dataclass(slots=True)
class MCPToolDescriptor:
    server_name: str
    original_name: str
    namespaced_name: str
    description: str
    input_schema: dict[str, Any]


@dataclass(slots=True)
class MCPDiscoveryResult:
    available: bool
    message: str
    tools: list[MCPToolDescriptor]


class MCPProtocolError(RuntimeError):
    """Raised when an MCP server response is malformed or unavailable."""


class _StdioMCPClient:
    """Very small stdio JSON-RPC client for MCP tools."""

    def __init__(self, server: MCPServerConfig, *, timeout_sec: int) -> None:
        self._server = server
        self._timeout_sec = timeout_sec
        self._process: subprocess.Popen[str] | None = None
        self._request_id = 0

    def __enter__(self) -> "_StdioMCPClient":
        if self._server.transport != "stdio":
            raise MCPProtocolError(f"Desteklenmeyen MCP transport: {self._server.transport}")
        if not self._server.command:
            raise MCPProtocolError(f"MCP sunucu komutu bos: {self._server.name}")
        self._process = subprocess.Popen(
            self._server.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
        )
        self.initialize()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._process is None:
            return
        try:
            if self._process.stdin is not None:
                self._process.stdin.close()
        finally:
            try:
                self._process.terminate()
                self._process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=1)

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _send(self, message: dict[str, Any]) -> None:
        if self._process is None or self._process.stdin is None:
            raise MCPProtocolError("MCP alt sureci hazir degil.")
        self._process.stdin.write(json.dumps(message, ensure_ascii=True, separators=(",", ":")) + "\n")
        self._process.stdin.flush()

    def _read_response(self, expected_id: int) -> dict[str, Any]:
        if self._process is None or self._process.stdout is None or self._process.stderr is None:
            raise MCPProtocolError("MCP alt sureci hazir degil.")
        selector = selectors.DefaultSelector()
        selector.register(self._process.stdout, selectors.EVENT_READ)
        selector.register(self._process.stderr, selectors.EVENT_READ)
        started = time.monotonic()
        stderr_lines: list[str] = []

        while True:
            remaining = self._timeout_sec - (time.monotonic() - started)
            if remaining <= 0:
                tail = stderr_lines[-1] if stderr_lines else "stderr cikti yok"
                raise MCPProtocolError(f"MCP sunucusu zaman asimina ugradi. Son stderr: {tail}")
            for key, _ in selector.select(timeout=remaining):
                if key.fileobj is self._process.stderr:
                    line = self._process.stderr.readline()
                    if line:
                        stderr_lines.append(line.strip())
                    continue
                line = self._process.stdout.readline()
                if not line:
                    continue
                payload = json.loads(line)
                if payload.get("id") != expected_id:
                    continue
                if "error" in payload:
                    message = payload["error"].get("message", "MCP hata yaniti")
                    raise MCPProtocolError(message)
                return payload

    def request(self, method: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        request_id = self._next_id()
        self._send(
            {
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params or {},
            }
        )
        return self._read_response(request_id)

    def notify(self, method: str, params: dict[str, Any] | None = None) -> None:
        self._send({"jsonrpc": "2.0", "method": method, "params": params or {}})

    def initialize(self) -> None:
        self.request(
            "initialize",
            {
                "protocolVersion": MCP_PROTOCOL_VERSION,
                "capabilities": {},
                "clientInfo": {"name": "sentinel-cli", "version": "0.1.0"},
            },
        )
        self.notify("notifications/initialized")

    def list_tools(self) -> list[dict[str, Any]]:
        tools: list[dict[str, Any]] = []
        cursor: str | None = None
        while True:
            response = self.request("tools/list", {"cursor": cursor} if cursor else {})
            result = response.get("result", {})
            tools.extend(result.get("tools", []))
            cursor = result.get("nextCursor")
            if not cursor:
                break
        return tools

    def call_tool(self, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        response = self.request("tools/call", {"name": name, "arguments": arguments})
        return response.get("result", {})


class MCPDynamicTool:
    """Dynamic tool wrapper for a discovered MCP tool."""

    risk_level = "mcp"
    args_model = MCPToolArguments

    def __init__(self, manager: "MCPClientManager", descriptor: MCPToolDescriptor) -> None:
        self._manager = manager
        self._descriptor = descriptor
        self.name = descriptor.namespaced_name
        self.description = descriptor.description

    def definition(self) -> ToolDefinition:
        return ToolDefinition(
            name=self.name,
            description=self.description,
            input_schema=self._descriptor.input_schema,
        )

    def execute(self, arguments: MCPToolArguments, context: ToolContext) -> ToolResult:
        payload = arguments.model_dump(mode="json", exclude_none=True)
        return self._manager.execute_tool(self._descriptor.namespaced_name, payload)


class MCPClientManager:
    """Best-effort MCP discovery and execution for configured stdio servers."""

    def __init__(self, settings: MCPSettings) -> None:
        self._settings = settings
        self._tool_map: dict[str, tuple[MCPServerConfig, MCPToolDescriptor]] = {}

    def _discover_from_server(self, server: MCPServerConfig) -> list[MCPToolDescriptor]:
        if server.transport not in SUPPORTED_MCP_TRANSPORTS:
            raise MCPProtocolError(
                f"MCP transport desteklenmiyor: {server.transport}. Faz 2.C yalnizca stdio destekler."
            )
        with _StdioMCPClient(server, timeout_sec=self._settings.startup_timeout_sec) as client:
            descriptors: list[MCPToolDescriptor] = []
            for tool in client.list_tools():
                original_name = tool["name"]
                namespaced = namespace_tool_name(server.name, original_name, server.tool_prefix)
                descriptors.append(
                    MCPToolDescriptor(
                        server_name=server.name,
                        original_name=original_name,
                        namespaced_name=namespaced,
                        description=tool.get("description") or tool.get("title") or original_name,
                        input_schema=tool.get("inputSchema") or {"type": "object", "additionalProperties": False},
                    )
                )
            return descriptors

    def discover_tools(self) -> MCPDiscoveryResult:
        if not self._settings.enabled or not self._settings.servers:
            return MCPDiscoveryResult(False, "MCP devre disi veya sunucu tanimli degil.", [])
        if not _mcp_extra_available():
            return MCPDiscoveryResult(
                False,
                "MCP extra kurulu degil. `pip install -e \".[mcp]\"` ile stdio MCP etkinlestirilebilir.",
                [],
            )

        discovered: list[MCPToolDescriptor] = []
        self._tool_map.clear()
        errors: list[str] = []
        for server in self._settings.servers:
            if not server.enabled:
                continue
            try:
                descriptors = self._discover_from_server(server)
            except (OSError, subprocess.SubprocessError, MCPProtocolError) as exc:
                errors.append(f"{server.name}: {exc}")
                continue
            for descriptor in descriptors:
                if descriptor.namespaced_name in self._tool_map:
                    continue
                self._tool_map[descriptor.namespaced_name] = (server, descriptor)
                discovered.append(descriptor)
        if errors and not discovered:
            return MCPDiscoveryResult(False, "MCP kesfi basarisiz: " + "; ".join(errors), [])
        if not discovered:
            message = "MCP sunucularinda arac bulunamadi."
            if errors:
                message += " Hatalar: " + "; ".join(errors)
            return MCPDiscoveryResult(True, message, [])
        message = "MCP araclari kesfedildi."
        if errors:
            message += " Bazi sunucular atlandi: " + "; ".join(errors)
        return MCPDiscoveryResult(True, message, discovered)

    def dynamic_tools(self) -> list[MCPDynamicTool]:
        discovery = self.discover_tools()
        if not discovery.available:
            return []
        return [MCPDynamicTool(self, descriptor) for descriptor in discovery.tools]

    def execute_tool(self, namespaced_name: str, arguments: dict[str, Any]) -> ToolResult:
        mapping = self._tool_map.get(namespaced_name)
        if mapping is None:
            discovery = self.discover_tools()
            mapping = self._tool_map.get(namespaced_name)
            if mapping is None:
                return ToolResult(False, "MCP_TOOL_UNKNOWN", discovery.message)

        server, descriptor = mapping
        try:
            with _StdioMCPClient(server, timeout_sec=self._settings.startup_timeout_sec) as client:
                result = client.call_tool(descriptor.original_name, arguments)
        except (OSError, subprocess.SubprocessError, MCPProtocolError) as exc:
            return ToolResult(False, "MCP_CALL_ERROR", f"MCP araci calismadi: {exc}")

        content = result.get("content", [])
        text_parts = [item.get("text", "") for item in content if item.get("type") == "text"]
        message = "\n".join(part for part in text_parts if part).strip()
        if not message and "structuredContent" in result:
            message = json.dumps(result["structuredContent"], ensure_ascii=True)
        if not message:
            message = "(MCP arac sonucu bos)"
        return ToolResult(
            not result.get("isError", False),
            "OK" if not result.get("isError", False) else "MCP_TOOL_ERROR",
            message,
            data={"raw": result, "server": descriptor.server_name, "tool": descriptor.original_name},
        )
