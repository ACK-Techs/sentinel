---
name: agentic-mcp-error-codes
description: "MCP JSON-RPC hata kodu standartları, istemci tarafı hata işleme ve kullanıcıya anlamlı hata mesajı üretimi; hata sınıflandırması ve retry stratejisi"
---

## Purpose
MCP protokolünde JSON-RPC 2.0 hata kodlarını doğru kullanmak, istemcilerin hataları kategorize edip uygun şekilde işleyebilmesini sağlamak.

## Workflow

### Hata Kodu Sınıflandırması
| Kod | Sabit | Açıklama | Retry? |
|-----|-------|----------|--------|
| -32700 | PARSE_ERROR | JSON parse edilemedi | Hayır |
| -32600 | INVALID_REQUEST | JSON-RPC şeması geçersiz | Hayır |
| -32601 | METHOD_NOT_FOUND | Araç/kaynak bulunamadı | Hayır |
| -32602 | INVALID_PARAMS | Parametre doğrulama hatası | Hayır |
| -32603 | INTERNAL_ERROR | Sunucu iç hatası | Evet (backoff) |
| -32000 | SERVER_ERROR | Uygulama seviyesi hata | Bağlama göre |
| -32001 | RATE_LIMITED | İstek hız sınırı | Evet (backoff) |
| -32002 | RESOURCE_NOT_FOUND | MCP resource mevcut değil | Hayır |

### Sunucu Tarafı Hata Üretimi
```python
# mcp_server/errors.py
from dataclasses import dataclass
from typing import Any

@dataclass
class MCPError(Exception):
    code: int
    message: str
    data: Any = None

    def to_jsonrpc(self, request_id) -> dict:
        error = {"code": self.code, "message": self.message}
        if self.data is not None:
            error["data"] = self.data
        return {"jsonrpc": "2.0", "id": request_id, "error": error}

# Özel hata sınıfları
class ToolNotFoundError(MCPError):
    def __init__(self, tool_name: str):
        super().__init__(
            code=-32601,
            message=f"Tool '{tool_name}' not found",
            data={"available_tools": _get_available_tools()}
        )

class ValidationError(MCPError):
    def __init__(self, field: str, reason: str):
        super().__init__(
            code=-32602,
            message=f"Invalid parameter '{field}': {reason}",
            data={"field": field, "reason": reason}
        )
```

### İstemci Tarafı Hata İşleme
```python
import asyncio
from sentinel.mcp_client import MCPClient

async def call_with_retry(client: MCPClient, tool: str, args: dict, max_retries=3):
    RETRYABLE_CODES = {-32603, -32001}
    
    for attempt in range(max_retries):
        try:
            return await client.call_tool(tool, args)
        except MCPError as e:
            if e.code not in RETRYABLE_CODES:
                raise  # retry etme, hemen yükselt
            
            if e.code == -32001:  # rate limited
                retry_after = e.data.get("retry_after", 5) if e.data else 5
                await asyncio.sleep(retry_after)
            else:
                # exponential backoff
                await asyncio.sleep(2 ** attempt)
            
            if attempt == max_retries - 1:
                raise
    
    raise RuntimeError("unreachable")
```

### Structured Error Logging
```python
import structlog

log = structlog.get_logger()

async def dispatch_method(method: str, params: dict, request_id):
    try:
        result = await _call(method, params)
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except MCPError as e:
        log.warning("mcp_error", code=e.code, message=e.message, method=method)
        return e.to_jsonrpc(request_id)
    except Exception as e:
        log.exception("mcp_internal_error", method=method)
        return MCPError(code=-32603, message="Internal error").to_jsonrpc(request_id)
```

## Common mistakes
- `-32000` tek bir "genel sunucu hatası" olarak kullanmak — alt kodlar (`-32001`, `-32002`) ile kategorize et
- Hata `data` alanına stack trace gömmek — production'da güvenlik riski; sadece structured metadata ekle
- İstemcide tüm hataları aynı şekilde işlemek — retry edilemez hataları retry etmek gereksiz yük
- `message` alanını i18n için kullanmaya çalışmak — `data` içine `code_key` ekle, istemci kendi locale'ini uygulasın

## References
- `skills/agentic-mcp-versioning`
- `skills/agentic-mcp-testing`
