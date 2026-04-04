from sentinel_cli.config import AppConfig
from sentinel_cli.tools import MCPClientManager, namespace_tool_name


def test_mcp_namespace_mapping() -> None:
    assert namespace_tool_name("grafana", "query") == "mcp_grafana_query"


def test_mcp_manager_reports_disabled_without_extra() -> None:
    config = AppConfig()
    config.mcp.enabled = True
    config.mcp.servers = []
    result = MCPClientManager(config.mcp).discover_tools()
    assert result.available is False
