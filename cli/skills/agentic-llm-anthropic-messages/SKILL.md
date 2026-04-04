---
name: agentic-llm-anthropic-messages
description: Anthropic Messages API ile iç mesaj şeması arasında map ve tool_use/tool_result eşlemesi yaparken kullan.
---

## Amaç

Anthropic tarafında **`system`** ayrı parametre / blok, **`messages`** dizisi; araçlar **`tool_use`** / **`tool_result`** olarak gelir. Uygulama içi ortak şemaya **adapter** ile dönüşüm zorunludur. Beta veya özel header gereksinimleri **resmi Anthropic dokümantasyonunda güncel doğrulanır**; bu skill’de sabit iddia yoksa “dokümanda kontrol et” denir.

## Kapsam

### Dahil

- Çok modlu içerik (metin + tool) birleştirme sırası.
- Streaming deltas → tam tool_use argümanı biriktirme (`agentic-llm-streaming-events`).

### Hariç

- Claude Code ürün API’si (farklı ürün olabilir).

## Kurallar

- `ANTHROPIC_API_KEY` ve `SENTINEL_ANTHROPIC_MODEL` env (`LLM_PROVIDERS.md`).
- Üçüncü parti Anthropic-uyumlu proxy Bearer auth gerekebilir; proje kararı adapter’da.
- Hata gövdelerini kullanıcıya özetle; ham JSON’da secret olabilir.

## Kontrol listesi

- [ ] Mock veya sandbox key ile round-trip tool çağrısı testi var mı?
- [ ] İç şema ile OpenAI yolu aynı ajan döngüsünü besliyor mu?
- [ ] Rate limit 429 mesajı anlamlı mı?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| tool_result eşleşmiyor | call id | Adapter eşlemesini düzelt |
| 400 invalid request | system blok uzunluğu | Context stratejisini gözden geçir |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-llm-provider-contract/SKILL.md`
- `../agentic-agent-tool-call-parse/SKILL.md`
- `https://docs.anthropic.com` (resmi; sürüm notları)
