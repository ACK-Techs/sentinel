---
name: agentic-grafana-llm-platform-overview
description: Grafana Labs LLM plugin, Assistant ve HTTP API ayrımını Sentinel CLI bağlamında açıklarken kullan.
---

## Amaç

Grafana ekosisteminde **nerede** yapay zekâ özellikleri sunulduğunu (UI içi LLM, Cloud Assistant, HTTP API) netleştirir; “CLI’yi Grafana LLM’ye bağladım” beklentisi ile teknik gerçeklik arasındaki farkı düşürür.

## Kapsam

### Dahil

- LLM plugin / ML app dokümantasyon yönü (kurulum Grafana tarafında).
- Grafana Assistant’ın Cloud odaklı doğası (self-hosted ile karıştırılmaması).
- Programatik erişim için HTTP API + service account token modeli.

### Hariç

- Grafana Cloud faturalandırma, kurumsal sözleşme.
- Sentinel kod değişikliği (bunun için `agentic-sentinel-grafana-agent-bridge`).

## Kurallar

1. **Grafana içi LLM** ile **dışarıdaki terminal ajanı (Sentinel)** aynı süreç değildir; entegrasyon açıkça tasarlanmalıdır.
2. Self-hosted COS’ta LLM plugin yoksa bu **beklenen** olabilir; eksiklik sanılmasın.
3. Resmi doc linklerini tercih et; sürüm seçiciyi hedef Grafana ile hizala.

## Kontrol listesi

- [ ] Kullanıcı Grafana Cloud mı, self-hosted mı kullanıyor?
- [ ] İhtiyaç “health doğrulama” mı, “metrik sorgusu” mu, “UI asistanı” mı?
- [ ] Token’lar repoya ve loga yazılmıyor mu?

## Hata ve geri dönüş

| Tipik sorun | Ne kontrol et | Sonraki adım |
|-------------|---------------|--------------|
| “Ajan Grafana görmüyor” | REPL’e bağlam/tool girişi var mı | `../agentic-sentinel-grafana-agent-bridge/SKILL.md` |
| Traefik 302 / alt yol | base_url + health | `../agentic-troubleshoot-traefik-ingress/SKILL.md` |
| Login/token | service account | `../agentic-troubleshoot-grafana/SKILL.md` |

## İlgili belgeler ve skill'ler

- `../documantations/GRAFANA_AI_PLATFORM_RESEARCH.md`
- `../documantations/GRAFANA_HTTP_PHASE4.md`
- `../agentic-sentinel-grafana-agent-bridge/SKILL.md`
- `../agentic-troubleshoot-grafana/SKILL.md`
