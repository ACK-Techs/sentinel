---
name: agentic-mcp-observability-server
description: "Sentinel observability araçlarını (Prometheus, Loki, Tempo) MCP server olarak sunma; LLM agent'ların metrik/log/trace sorgulayabilmesi için tool tanımları ve güvenli erişim"
---

## Purpose
Prometheus, Loki ve Tempo sorgularını MCP araçlarına sararak LLM agent'ların Sentinel gözlemlenebilirlik verisine doğrudan erişmesini sağlamak.

## Workflow

### Server Yapısı
```
sentinel-mcp/
├── server.py           # MCP server bootstrap
├── tools/
│   ├── metrics.py      # Prometheus araçları
│   ├── logs.py         # Loki araçları
│   └── traces.py       # Tempo araçları
└── config.py           # backend URL'leri
```

### Prometheus Tool Tanımları
```python
# tools/metrics.py
from mcp.server import Server
from mcp.types import Tool, TextContent
import httpx

def register_metrics_tools(server: Server, prometheus_url: str):
    
    @server.tool()
    async def query_metric(
        promql: str,
        time: str = "now",
        step: str = "60s"
    ) -> list[TextContent]:
        """Anlık PromQL sorgusu çalıştır"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{prometheus_url}/api/v1/query",
                params={"query": promql, "time": time},
                timeout=10.0
            )
            resp.raise_for_status()
            data = resp.json()
        
        if data["status"] != "success":
            return [TextContent(type="text", text=f"Hata: {data.get('error', 'bilinmiyor')}")]
        
        results = data["data"]["result"]
        if not results:
            return [TextContent(type="text", text="Sonuç bulunamadı")]
        
        lines = [f"{r['metric']}: {r['value'][1]}" for r in results]
        return [TextContent(type="text", text="\n".join(lines))]
    
    @server.tool()
    async def query_metric_range(
        promql: str,
        start: str,
        end: str,
        step: str = "60s"
    ) -> list[TextContent]:
        """Zaman aralığı PromQL sorgusu"""
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{prometheus_url}/api/v1/query_range",
                params={"query": promql, "start": start, "end": end, "step": step},
                timeout=30.0
            )
            resp.raise_for_status()
        return [TextContent(type="text", text=resp.text)]
```

### Loki Tool Tanımları
```python
# tools/logs.py
@server.tool()
async def query_logs(
    logql: str,
    start: str = "now-1h",
    end: str = "now",
    limit: int = 100
) -> list[TextContent]:
    """LogQL ile Loki log sorgula"""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{loki_url}/loki/api/v1/query_range",
            params={
                "query": logql,
                "start": start,
                "end": end,
                "limit": limit
            },
            timeout=15.0
        )
        resp.raise_for_status()
        data = resp.json()
    
    entries = []
    for stream in data.get("data", {}).get("result", []):
        for ts, line in stream.get("values", []):
            entries.append(f"[{ts}] {line}")
    
    return [TextContent(type="text", text="\n".join(entries[-limit:]))]
```

### Server Bootstrap
```python
# server.py
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from sentinel_mcp.config import Settings

async def main():
    settings = Settings()
    server = Server("sentinel-observability")
    
    from sentinel_mcp.tools.metrics import register_metrics_tools
    from sentinel_mcp.tools.logs import register_logs_tools
    from sentinel_mcp.tools.traces import register_traces_tools
    
    register_metrics_tools(server, settings.prometheus_url)
    register_logs_tools(server, settings.loki_url)
    register_traces_tools(server, settings.tempo_url)
    
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### Claude Desktop Konfigürasyonu
```json
{
  "mcpServers": {
    "sentinel": {
      "command": "python",
      "args": ["-m", "sentinel_mcp.server"],
      "env": {
        "PROMETHEUS_URL": "http://localhost:9090",
        "LOKI_URL": "http://localhost:3100",
        "TEMPO_URL": "http://localhost:3200"
      }
    }
  }
}
```

## Common mistakes
- Prometheus yanıtını ham JSON olarak döndürmek — LLM büyük JSON'ı verimli işleyemez; özet metin döndür
- Timeout koymamak — Prometheus range query uzun sürebilir; 30s timeout zorunlu
- Tool başına ayrı HTTP client açmak — `httpx.AsyncClient` context manager ile yeniden kullanılabilir client kur
- LogQL/PromQL doğrulaması yapmamak — geçersiz sorgu ile backend 400 döndürür, MCP INTERNAL_ERROR gibi görünür

## References
- `skills/agentic-mcp-versioning`
- `skills/agentic-mcp-error-codes`
- `skills/obs-tempo-trace-query`
