---
name: agentic-mcp-resource-endpoints
description: MCP tabanlı araç, kaynak ve taşıma katmanlarını Sentinel ile doğru bağlamak; şema, kimlik doğrulama ve işletim politikalarını netleştirmek gerektiğinde kullan.
---

## MCP bağlamı
`agentic-mcp-resource-endpoints` için odak, Model Context Protocol bileşenlerini Sentinel agent döngüsüne öngörülebilir şekilde bağlamaktır. Burada hata çoğunlukla koddan değil; şema, transport veya auth sözleşmesindeki küçük uyumsuzluklardan çıkar.

## Uygulama iskeleti
- **Server sözleşmesi:** tool/resource/prompt tanımlarını JSON Schema ile açık yaz.
- **Taşıma katmanı:** stdio ve SSE kullanımını ortam koşuluna göre seç; timeout/retry davranışı belirle.
- **Kimlik ve yetki:** minimum yetki, token ömrü ve rotasyon stratejisi uygula.
- **İstemci entegrasyonu:** tool mapping ve isim çakışmalarını başlangıçta doğrula.
- **Test hattı:** handshake, şema ihlali ve auth hata senaryolarını otomasyonla dene.

## Operasyon notları
- Tool isimleri built-in araçlarla çakışmamalı.
- Uzun yaşayan SSE bağlantılarında heartbeat ve reconnect zorunlu.
- Sunucu tarafı hata mesajları kullanıcıya sızan secret içermemeli.

## Skill-spesifik kararlar
- Resource endpoint URI tasariminda stabil path ve acik MIME tipi kullan. Buyuk iceriklerde pagination veya parcali okuma planla.

## Referanslar
- `cli/skills/agentic-mcp-client-config/SKILL.md`
- `cli/skills/agentic-mcp-tool-mapping/SKILL.md`
- `cli/documantations/ARCHITECTURE_AGENTIC_CLI.md`
- `documantations/INTEGRATION_SENTINEL_CLI_FROM_CLI_CLAUDE.md`
