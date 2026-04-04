"""Optional MCP configuration and discovery surface."""

from __future__ import annotations

from dataclasses import dataclass

from sentinel_cli.config import MCPSettings


@dataclass(slots=True)
class MCPDiscoveryResult:
    available: bool
    message: str
    tools: list[dict[str, str]]


class MCPClientManager:
    """Best-effort MCP client bootstrap without hard dependency."""

    def __init__(self, settings: MCPSettings) -> None:
        self._settings = settings

    def discover_tools(self) -> MCPDiscoveryResult:
        if not self._settings.enabled or not self._settings.servers:
            return MCPDiscoveryResult(False, "MCP devre disi.", [])
        try:
            import mcp  # noqa: F401
        except ImportError:
            return MCPDiscoveryResult(
                False,
                "MCP extra kurulu degil. `pip install sentinel-cli[mcp]` ile etkinlestirilebilir.",
                [],
            )
        tools = []
        for server in self._settings.servers:
            prefix = server.tool_prefix or f"mcp_{server.name}"
            tools.append({"server": server.name, "tool_name": f"{prefix}_list_tools"})
        return MCPDiscoveryResult(True, "MCP sunuculari yuklendi.", tools)


def namespace_tool_name(server_name: str, tool_name: str, prefix: str | None = None) -> str:
    safe_prefix = prefix or f"mcp_{server_name}"
    return f"{safe_prefix}_{tool_name}"
