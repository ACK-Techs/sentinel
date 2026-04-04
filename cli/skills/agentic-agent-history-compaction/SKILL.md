---
name: agentic-agent-history-compaction
description: Uzun oturumlarda konuşma özetleme veya kesme politikası ve korunacak mesajları seçerken kullan.
---

## Amaç

Eşik aşıldığında: **özet** (ayrı LLM çağrısı veya kural tabanlı kırpma) veya **eski turları at**. **Korunur**: sistem mesajları, ilk kullanıcı hedefi, son N tur (N proje kararı). **Özet kalitesi düşük** ise (çok kısa / anahtar kelime kaçağı) kullanıcıya uyarı ve manuel devam seçeneği. **Maliyet**: özet çağrısı ek token tüketir (`agentic-llm-context-window-strategy`).

## Kapsam

### Dahil

- Tool çıktılarının özetlenmesi veya truncasyon önceliği.
- Oturum dosyası ile uyum (`agentic-session-persistence`).

### Hariç

- Harici vektör bellek / RAG (katalogda yoksa belirt).

## Kurallar

- Özet sonrası tool_call_id eşleşmeleri bozulmamalı (implementasyon dikkati).
- Compaction tetikleyicisi: tahmini token veya `usage` (`MemoryMonitor` benzeri desen).
- Kullanıcı “önemli” mesajı işaretleyebilir (proje kararı).

## Kontrol listesi

- [ ] Özet sonrası ajan görevi sürdürebildi mi (integration test)?
- [ ] İlk kullanıcı isteği kayboldu mu (regresyon)?
- [ ] Maliyet uyarısı dokümante mi?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Özet bağlamı sildi | Koruma kuralları | N artır |
| Sonsuz özet döngüsü | Tek seferde bir compaction | Bayrak kilidi |

## İlgili belgeler ve skill'ler

- `../agentic-llm-context-window-strategy/SKILL.md`
- `../agentic-session-persistence/SKILL.md`
- `../agentic-llm-provider-contract/SKILL.md`
