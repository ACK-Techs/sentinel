---
name: agentic-llm-streaming-events
description: Birleşik stream olay türleri (metin parçası, tool parçası, bitiş, hata) ve birleştirme sırasını tanımlarken kullan.
---

## Amaç

Dış API’den gelen parçalar tek **iç olay modeline** map edilir: örn. `text_delta`, `tool_call_delta`, `tool_call_ready`, `done`, `error`, `usage`. **Birleştirme sırası** korunur; **kısmi JSON** argüman biriktirmede sınır taşması ve geçersiz UTF-8 kesimi için uyarı. Çok baytlı karakterlerde **chunk sınırı** sorunları dokümante edilir.

## Kapsam

### Dahil

- SSE vs chunked transfer farkı (transport); iş mantığı aynı olaylar.
- Reasoning / thinking token ayrı kanal (sağlayıcı destekliyorsa proje kararı).

### Hariç

- Ham protokol spesifikasyonunun tamamı.

## Kurallar

- Aynı turda birden fazla tool çağrısı: olay sırası ile deterministik parse.
- `done` gelmeden tool yürütme başlatılmaz (tam argüman hazır olmalı).
- Hata olayında kısmi metin kullanıcıya “yarım yanıt” olarak etiketlenebilir.

## Kontrol listesi

- [ ] Uzun çıktıda tüm delta’lar birleşince içerik birebir mi (regresyon testi)?
- [ ] Kısmi Unicode için decode stratejisi testli mi?
- [ ] `agentic-agent-tool-call-parse` ile olay sözleşmesi uyumlu mu?

## Hata ve geri dönüş

| Tipik sorun | Kontrol | Sonraki adım |
|-------------|---------|--------------|
| Takılı kalan stream | Timeout | Read timeout katmanı |
| Çift done | Sağlayıcı bug | Idempotent tamamlama |

## İlgili belgeler ve skill'ler

- `../documantations/LLM_PROVIDERS.md`
- `../agentic-llm-provider-contract/SKILL.md`
- `../agentic-agent-tool-call-parse/SKILL.md`
- `../agentic-llm-retries-timeouts/SKILL.md`
