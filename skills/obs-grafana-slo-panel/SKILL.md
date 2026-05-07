---
name: obs-grafana-slo-panel
description: Grafana’da SLO/SLI ve error budget görünümünü tasarlamak (SLO hedefi, budget kalan, burn rate) gerektiğinde kullan. “SLO panel nasıl olmalı?”, “error budget grafiği”, “burn rate göstergesi” gibi SRE odaklı dashboard tasarımına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- SLO panel iskeleti: hedef, mevcut SLI, error budget kalan ve burn rate
- Panel türü seçimi: stat + time series + (opsiyonel) table
- Anti-pattern: sadece “% uptime” göstermek (budget ve burn rate olmadan)

## Workflow
- SLO’yu sabitle:
  - Hedef: ör. 99.9% / 30 gün.
  - SLI tanımı: başarı oranı mı (2xx), latency mi (p95 < X)?
- Error budget’i hesaplayacağın pencereyi seç:
  - Rolling 30 gün vs takvim ayı (ekip standardı).
- Panel seti:
  - Stat: “şu an SLI” ve “budget kalan”.
  - Time series: SLI trend + budget burn (günlük).
  - Burn rate: kısa pencere (1h/6h) ve uzun pencere (3d/30d) birlikte.
- Drilldown:
  - Burn artınca nereye gidilecek? (logs/traces linkleri, en kötü endpoint tablosu)
- Doğrulama:
  - Bir incident penceresinde panel “geriye dönük” doğru davranıyor mu?

## Common mistakes
- SLI penceresi ile SLO penceresini karıştırmak (farklı rollup’lar yanlış yorum üretir).
- Burn rate yerine sadece “son değer” göstermek.

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`
