---
name: agentic-mcp-versioning
description: "MCP protocol versiyon müzakeresi ve geriye dönük uyumluluk yönetimi; istemci-sunucu capability negotiation, BREAKING_CHANGE tespiti ve migration kılavuzu"
---

## Purpose
MCP sunucu ve istemcileri arasında protokol versiyonunu müzakere etmek, uyumsuz değişiklikleri erken tespit etmek ve geriye dönük uyumluluğu korumak.

## Workflow

### 1. Capability Negotiation El Sıkışması
```python
# server/versioning.py
SUPPORTED_PROTOCOL_VERSIONS = ["2024-11-05", "2024-10-07"]

async def handle_initialize(params: dict) -> dict:
    client_version = params.get("protocolVersion")
    
    if client_version in SUPPORTED_PROTOCOL_VERSIONS:
        negotiated = client_version
    else:
        # En yüksek ortak versiyona düş
        negotiated = SUPPORTED_PROTOCOL_VERSIONS[0]
    
    return {
        "protocolVersion": negotiated,
        "capabilities": {
            "tools": {"listChanged": True},
            "resources": {"subscribe": False},
            "logging": {}
        },
        "serverInfo": {
            "name": "sentinel-mcp",
            "version": "1.2.0"
        }
    }
```

### 2. Sunucu Tarafı Versiyon Guard
```python
from functools import wraps
from packaging.version import Version

def require_protocol_version(min_version: str):
    def decorator(fn):
        @wraps(fn)
        async def wrapper(ctx, *args, **kwargs):
            client_ver = ctx.session.protocol_version
            if Version(client_ver) < Version(min_version):
                raise MCPError(
                    code=-32600,
                    message=f"Bu araç protokol {min_version}+ gerektirir, "
                            f"istemci {client_ver} kullanıyor"
                )
            return await fn(ctx, *args, **kwargs)
        return wrapper
    return decorator

@require_protocol_version("2024-11-05")
async def tool_with_streaming(ctx, params):
    ...
```

### 3. İstemci Tarafı Uyumluluk Katmanı
```python
class VersionAwareClient:
    def __init__(self, server_version: str):
        self.server_version = Version(server_version)
    
    def supports_streaming(self) -> bool:
        return self.server_version >= Version("2024-11-05")
    
    def supports_resource_subscribe(self) -> bool:
        return self.server_version >= Version("2024-11-05")
    
    async def call_tool(self, name: str, args: dict):
        if self.supports_streaming():
            return await self._call_with_progress(name, args)
        return await self._call_basic(name, args)
```

### 4. Changelog ile Breaking Change Tespiti
```python
CHANGELOG = {
    "2024-11-05": {
        "breaking": ["resources/subscribe eklendi, eski polling kaldırıldı"],
        "added": ["tool progress notifications", "logging capability"],
        "deprecated": []
    }
}

def check_migration_needed(from_ver: str, to_ver: str) -> list[str]:
    breaking = []
    for ver, changes in CHANGELOG.items():
        if Version(from_ver) < Version(ver) <= Version(to_ver):
            breaking.extend(changes.get("breaking", []))
    return breaking
```

## Common mistakes
- `initialize` yanıtında sunucu versiyonunu göndermemek — istemci hangi feature'ların aktif olduğunu bilemez
- Version string karşılaştırmasını lexicographic yapmak (`"2024-11-05" > "2024-9-01"` hatalı) — `packaging.version.Version` kullan
- Capability müzakeresi olmadan sunucuya yeni araç eklemek — eski istemciler araç listesini parse edemeyebilir
- Protokol versiyonunu session state'e kaydetmemek — her request'te yeniden parse etmek gereksiz yük

## References
- `skills/agentic-mcp-error-codes`
- `skills/agentic-mcp-testing`
