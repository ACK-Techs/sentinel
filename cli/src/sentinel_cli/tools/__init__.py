"""Built-in tool registry and optional MCP helpers."""

from sentinel_cli.tools.mcp import MCPClientManager, MCPDiscoveryResult, namespace_tool_name
from sentinel_cli.tools.registry import ParsedToolCall, ToolRegistry

__all__ = [
    "MCPClientManager",
    "MCPDiscoveryResult",
    "ParsedToolCall",
    "ToolRegistry",
    "namespace_tool_name",
]
