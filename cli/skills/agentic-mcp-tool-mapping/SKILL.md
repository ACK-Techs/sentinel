---
name: agentic-mcp-tool-mapping
description: MCP tool adlarının iç registry ile çakışmaması için isim önekleri ve çözüm kurallarını tanımlarken kullan.
---

## Amaç

Önerilen kural: **`mcp_<server>_<tool>`** veya benzersiz namespace; çakışmada **MCP mi yerleşik mi** önceliği proje kararı (genelde yerleşik kazanır veya MCP yeniden adlandırılır). Aynı ada sahip iki sunucu: sunucu sırası veya zorunlu alias.

## Kapsam

### Dahil

- Tool listesi birleştirme sırası (model context’e hangi sırayla gider).
- Display name vs internal name ayrımı.

### Hariç

- MCP resource vs tool ayrımının tam spesifikasyonu (SDK’ya bırakılabilir).

## Kurallar

- Çakışma tespitinde başlangıçta uyarı logla.
- Kullanıcıya görünen isimler kısa tutulabilir; iç isim benzersiz kalmalı.
- `agentic-tools-base-contract` şema alanları ile uyum.

## Kontrol listesi

- [ ] İki MCP aynı tool adıyla yüklenince test geçiyor mu?
- [ ] Model yanlış isim çağırınca parse katmanı yakalıyor mu?
- [ ] Dokümante önek tablosu var mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Uzun isim context şişiriyor | Kısaltma haritası | Alias tablosu |
| Yanlış sunucu routing | Server id | Çağrı metadata |

## İlgili belgeler ve skill'ler

- `../agentic-mcp-client-config/SKILL.md`
- `../agentic-tools-base-contract/SKILL.md`
- `../agentic-agent-tool-call-parse/SKILL.md`
