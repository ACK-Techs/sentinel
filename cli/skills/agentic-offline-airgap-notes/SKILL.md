---
name: agentic-offline-airgap-notes
description: Air-gapped ortamda uzak API yokken lokal model, pip mirror ve MCP kısıtları için kontrol listesi hazırlarken kullan.
---

## Amaç

**API yok**: yalnız `SENTINEL_LOCAL_BASE_URL` ve lokal model (`agentic-llm-openai-compatible-local`). **pip/uv**: iç mirror veya wheelhouse; hash doğrulama önerisi. **MCP**: genelde stdio yerel binary ile mümkün; **HTTP MCP** dış ağ gerektiriyorsa **devre dışı** veya proxy istisnası (politika). **Hangi skill’ler zayıflar**: uzak API, web fetch, bazı telemetri exporter’ları.

## Kapsam

### Dahil

- Kurulum öncesi gereken önbellek artefact listesi.
- Model dosyalarının önceden yüklenmesi (Ollama offline mod resmi doküman).

### Hariç

- Ulusal güvenlik sertifikasyon süreçleri.

## Kurallar

- Dışarı sızdırmayı önlemek için telemetry varsayılan kapalı doğrula.
- Harici URL içeren dokümantasyon linkleri “kopyala-USB ile taşı” notu.
- `agentic-mcp-client-config` yalnız onaylı yerel komutlar.

## Kontrol listesi

- [ ] Tüm Python bağımlılıkları iç ağda çözülüyor mu?
- [ ] LLM çıkışı dış API çağırmıyor mu (tool ile)?
- [ ] Güncelleme stratejisi (manuel paket) tanımlı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| pip timeout | index-url | Mirror yapılandır |
| Model yok | ollama list | Offline import |

## İlgili belgeler ve skill'ler

- `../agentic-llm-openai-compatible-local/SKILL.md`
- `../agentic-mcp-client-config/SKILL.md`
- `../agentic-telemetry-optional/SKILL.md`
- `../agentic-feature-flags/SKILL.md`
