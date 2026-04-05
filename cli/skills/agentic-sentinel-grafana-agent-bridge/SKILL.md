---
name: agentic-sentinel-grafana-agent-bridge
description: Sentinel REPL ajanına Grafana bağlamı (doctor özeti enjeksiyonu veya tool) eklerken tasarım ve güvenlik kurallarını uygularken kullan.
---

## Amaç

Faz 4’ün **bağlantı doğrulamasını** REPL’deki LLM’in kullanabileceği **güvenli operasyonel özet** haline getirmeyi standartlaştırır; hallüsinasyonu azaltmak için “canlı panel verisi değildir” ayrımını korur.

## Kapsam

### Dahil

- `check_grafana_connection` → `GrafanaCheckResult.to_dict()` → **oturumda** `grafana_context_snapshot` (JSON string); LLM’e **`system_prompt` birleştirmesi** ile verilmesi (USER mesajı olarak session’a ekleme — compaction ile çakışır).
- YAML/env ile aç/kapa: `agent.grafana_context_in_repl` + `SENTINEL_GRAFANA_CONTEXT_IN_REPL` (`IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md` ile senkron).
- İsteğe bağlı ince tool (yalnızca health/status); Gemini profillerinde tool kapalıysa varsayılan dışı.

### Hariç

- Grafana içinde dashboard otomasyonu, tüm datasource E2E.
- Ham token veya tam Grafana URL’sinin modele düşmesi.

## Adımlar

1. `IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md` kapılarına göre A katmanını (enjeksiyon) uygula.
2. `GrafanaCheckResult.to_dict()` alanlarını kullan; yeni secret alanı ekleme.
3. REPL başlangıcında tek seferlik enjeksiyon; session resume davranışını dokümante et (gerekirse yalnızca yeni oturumda).
4. README’de kullanıcıya: “Özet ≠ canlı metrik; detay için doctor veya datasource skill zinciri.”
5. Test: mock `transport` ile mesaj listesi doğrula.

## Kontrol listesi

- [ ] `ruff` + `pytest` yeşil.
- [ ] `SENTINEL_GRAFANA_*` repoda yok.
- [ ] Açıklama metni Türkçe ve kısa.
- [ ] Cloud+Gemini kullanıcıları için tool katmanı bilinçli kapalı mı?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| Model yine “erişemiyorum” diyor | Enjeksiyon gerçekten ilk mesajda mı | `app.py` REPL akışı |
| 302/http_error | follow_redirects, base_url | `../../src/sentinel_cli/observability/grafana.py` |
| Yanlış beklenti | Grafana LLM plugin | `../agentic-grafana-llm-platform-overview/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../documantations/IMPLEMENTATION_PLAN_INDIVIDUAL_CLOSE.md`
- `../documantations/INDIVIDUAL_CLOSE_SKILL_AND_DOC_INDEX.md`
- `../documantations/GRAFANA_AI_PLATFORM_RESEARCH.md`
- `../agentic-grafana-llm-platform-overview/SKILL.md`
- `../agentic-troubleshoot-grafana/SKILL.md`
