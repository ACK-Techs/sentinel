---
name: agentic-mcp-testing
description: "MCP server birim ve entegrasyon testi; mock transport, in-process test client, pytest-asyncio ile tool çağrısı ve hata senaryosu doğrulama"
---

## Purpose
MCP sunucularını ağ bağlantısı gerektirmeden test etmek; araç işleyicilerini izole birim testleri ve tam protokol döngüsünü kapsayan entegrasyon testleriyle doğrulamak.

## Workflow

### Proje Yapısı
```
tests/
├── conftest.py          # shared fixtures
├── unit/
│   ├── test_tools.py    # handler fonksiyonları izole test
│   └── test_validators.py
└── integration/
    └── test_mcp_protocol.py  # tam JSON-RPC döngüsü
```

### Mock Transport Fixture
```python
# tests/conftest.py
import pytest
import asyncio
from mcp import Server
from mcp.server.stdio import stdio_server
from mcp.shared.memory import create_connected_server_and_client_session

@pytest.fixture
async def mcp_session():
    """In-process MCP oturumu — ağ yok, gerçek protokol"""
    from sentinel_mcp.server import create_server
    server = create_server()
    
    async with create_connected_server_and_client_session(server) as (server_session, client_session):
        yield client_session

@pytest.fixture
def anyio_backend():
    return "asyncio"
```

### Tool Handler Birim Testi
```python
# tests/unit/test_tools.py
import pytest
from sentinel_mcp.tools.metrics import fetch_metrics_tool

@pytest.mark.asyncio
async def test_fetch_metrics_returns_prometheus_data(mock_prometheus):
    mock_prometheus.set_response({
        "status": "success",
        "data": {"result": [{"metric": {"job": "api"}, "value": [1700000000, "42"]}]}
    })
    
    result = await fetch_metrics_tool(
        query="up{job='api'}",
        time_range="1h"
    )
    
    assert result["status"] == "success"
    assert len(result["data"]["result"]) == 1
    assert result["data"]["result"][0]["value"][1] == "42"

@pytest.mark.asyncio
async def test_fetch_metrics_invalid_query_raises_validation_error():
    from sentinel_mcp.errors import ValidationError
    
    with pytest.raises(ValidationError) as exc_info:
        await fetch_metrics_tool(query="", time_range="1h")
    
    assert exc_info.value.code == -32602
    assert "query" in exc_info.value.message
```

### Protokol Entegrasyon Testi
```python
# tests/integration/test_mcp_protocol.py
import pytest
from mcp.types import CallToolRequest

@pytest.mark.asyncio
async def test_tool_list_returns_expected_tools(mcp_session):
    tools = await mcp_session.list_tools()
    tool_names = [t.name for t in tools.tools]
    
    assert "fetch_metrics" in tool_names
    assert "query_logs" in tool_names
    assert "get_traces" in tool_names

@pytest.mark.asyncio
async def test_call_tool_full_protocol_round_trip(mcp_session):
    result = await mcp_session.call_tool(
        "fetch_metrics",
        {"query": "up", "time_range": "5m"}
    )
    
    assert result.content is not None
    assert len(result.content) > 0
    assert result.isError is False

@pytest.mark.asyncio
async def test_call_unknown_tool_returns_error(mcp_session):
    result = await mcp_session.call_tool("nonexistent_tool", {})
    assert result.isError is True
```

### CI Konfigürasyonu
```yaml
# pyproject.toml
[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
markers = ["integration: requires running services"]

[tool.coverage.run]
source = ["sentinel_mcp"]
omit = ["tests/*"]
```

## Common mistakes
- Her test için gerçek HTTP bağlantısı açmak — mock transport ile 10x daha hızlı çalışır
- `initialize` handshake'i atlamak — bazı MCP özellikler (logging, progress) negotiation sonrası aktif
- Async fixture'ları `@pytest.fixture` yerine `@pytest.fixture` + `scope="function"` ile tanımlamak — asyncio scope uyuşmazlığı çıkabilir
- Tool handler'ı direkt çağırıp MCP katmanını test etmemek — JSON-RPC serileştirme hatalarını kaçırırsın

## References
- `skills/agentic-mcp-versioning`
- `skills/agentic-mcp-error-codes`
- `skills/test-unit-fastapi`
