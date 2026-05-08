---
name: agentic-mcp-local-filesystem
description: "MCP filesystem server ile güvenli yerel dosya okuma/yazma; izin verilen dizin kısıtlaması, path traversal koruması ve Sentinel config/log dosyalarına agent erişimi"
---

## Purpose
LLM agent'ların yerel dosya sistemine güvenli ve kısıtlı erişimini sağlamak; path traversal saldırılarına karşı koruma ve izin verilen dizinlerin açık tanımı.

## Workflow

### Filesystem MCP Server Kurulumu
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/sentinel-coming/configs",
        "/var/log/sentinel",
        "/tmp/sentinel-workspace"
      ]
    }
  }
}
```

İzin verilen dizinler positional argument olarak geçilir — bu dizinlerin dışına çıkış otomatik engellenir.

### Path Traversal Koruma (Custom Server)
```python
# secure_fs_server.py
import os
from pathlib import Path
from mcp.server import Server
from mcp.types import TextContent

ALLOWED_ROOTS = [
    Path("/home/user/sentinel-coming/configs").resolve(),
    Path("/var/log/sentinel").resolve(),
]

def is_safe_path(requested: str) -> tuple[bool, Path]:
    """Path traversal koruması"""
    resolved = Path(requested).resolve()
    for root in ALLOWED_ROOTS:
        try:
            resolved.relative_to(root)
            return True, resolved
        except ValueError:
            continue
    return False, resolved

server = Server("sentinel-filesystem")

@server.tool()
async def read_file(path: str) -> list[TextContent]:
    safe, resolved = is_safe_path(path)
    if not safe:
        raise PermissionError(f"Erişim reddedildi: {path}")
    
    if not resolved.exists():
        raise FileNotFoundError(f"Dosya bulunamadı: {path}")
    
    if resolved.stat().st_size > 10 * 1024 * 1024:  # 10MB limit
        raise ValueError("Dosya çok büyük (10MB limit)")
    
    content = resolved.read_text(encoding="utf-8", errors="replace")
    return [TextContent(type="text", text=content)]

@server.tool()
async def write_file(path: str, content: str) -> list[TextContent]:
    safe, resolved = is_safe_path(path)
    if not safe:
        raise PermissionError(f"Yazma reddedildi: {path}")
    
    # Sadece /tmp/sentinel-workspace'e yazma izni
    write_root = Path("/tmp/sentinel-workspace").resolve()
    try:
        resolved.relative_to(write_root)
    except ValueError:
        raise PermissionError(f"Yazma sadece {write_root} içinde mümkün")
    
    resolved.parent.mkdir(parents=True, exist_ok=True)
    resolved.write_text(content, encoding="utf-8")
    return [TextContent(type="text", text=f"Yazıldı: {resolved}")]

@server.tool()
async def list_directory(path: str) -> list[TextContent]:
    safe, resolved = is_safe_path(path)
    if not safe:
        raise PermissionError(f"Dizin erişimi reddedildi: {path}")
    
    if not resolved.is_dir():
        raise NotADirectoryError(f"Dizin değil: {path}")
    
    entries = []
    for entry in sorted(resolved.iterdir()):
        entry_type = "DIR" if entry.is_dir() else "FILE"
        size = entry.stat().st_size if entry.is_file() else 0
        entries.append(f"[{entry_type}] {entry.name} ({size} bytes)")
    
    return [TextContent(type="text", text="\n".join(entries))]
```

### Sentinel Konfigürasyon Dosyası Okuma Örneği
```python
# Agent prompt örneği
SENTINEL_CONFIG_AGENT = """
Sentinel deployment yapılandırmasını analiz et:
1. /home/user/sentinel-coming/configs/prometheus.yml oku
2. scrape_interval ve global timeout değerlerini kontrol et
3. Eksik job label'larını tespit et
4. Önerilen değişiklikleri /tmp/sentinel-workspace/config-review.md olarak kaydet
"""
```

### Güvenli Log Okuma
```python
@server.tool()
async def tail_log(path: str, lines: int = 100) -> list[TextContent]:
    """Son N satırı oku — büyük log dosyaları için güvenli"""
    safe, resolved = is_safe_path(path)
    if not safe:
        raise PermissionError(f"Erişim reddedildi: {path}")
    
    lines = min(lines, 1000)  # maksimum 1000 satır
    
    with open(resolved, "rb") as f:
        # Sondan oku
        f.seek(0, 2)
        file_size = f.tell()
        chunk_size = min(file_size, 64 * 1024)
        f.seek(-chunk_size, 2)
        chunk = f.read().decode("utf-8", errors="replace")
    
    last_lines = chunk.splitlines()[-lines:]
    return [TextContent(type="text", text="\n".join(last_lines))]
```

## Common mistakes
- İzin verilen dizinleri `os.path.join` ile doğrulamak — `Path.resolve()` olmadan semlink atlama riski var
- Yazma iznini okuma izninden ayırt etmemek — agent istemeden config dosyalarını değiştirebilir
- Dosya boyutu kontrolü yapmamak — büyük binary dosya LLM context'ini taşırır
- `..` içeren path'leri sadece string karşılaştırmayla reddetmek — URL-encode edilmiş `%2F..%2F` geçebilir; `Path.resolve()` şarttır

## References
- `skills/agentic-mcp-versioning`
- `skills/sec-tls-mtls-design`
