---
name: obs-grafana-heatmap-panel
description: Prometheus histogram metriklerini Grafana heatmap panel ile doğru görselleştirmek (bucket dağılımı, latency band, renk/scale ayarı) gerektiğinde kullan. “Heatmap doğru değil”, “bucket’lar ters”, “p95/p99 çizgisi ile birlikte göster” gibi histogram‑odaklı panel tasarımına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Heatmap için doğru PromQL kalıbı (bucket rate + le boyutunu koru)
- Panel ayarları: bucket axis, color scale, unit (ms/s), log scale kararı
- Doğrulama: heatmap ile p95/p99 çizgisinin aynı hikâyeyi anlatması

## Workflow
- Ön koşul:
  - Histogram metrik ailesi var mı? (`_bucket`, `_sum`, `_count`)
- PromQL’i doğru yaz:
  - Heatmap için bucket’ları rate’e çevir: `sum by (le, ...) (rate(<metric>_bucket[5m]))`
  - `le` boyutunu düşürme; heatmap bucket eksenidir.
- Panel ayarı:
  - Unit: latency ise ms/s doğru seç.
  - Color scale: düşük trafik/gürültü için log scale gerekebilir.
  - Zaman penceresi ve step: çok ince step → gürültü, çok kalın → detay kaybı.
- Yan yana doğrulama:
  - Aynı panelde (veya komşu panelde) p95/p99 çizgisi göster.
  - Heatmap’te band yükseliyorsa p95/p99 da yükselmeli.

## Common mistakes
- `le`’yi aggregate edip kaybetmek: heatmap düz çizgiye dönüşür.
- Raw bucket sayımını kullanmak: rate yerine kümülatif bucket’ı çizmek yanıltır.

## References
- `skills/cos-deploy-grafana`
- `skills/obs-prometheus-histogram-summary`
