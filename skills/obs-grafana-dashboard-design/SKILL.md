---
name: obs-grafana-dashboard-design
description: Grafana’da yeni bir dashboard tasarlamak veya mevcut dashboard’un okunabilirliğini/operatör verimini artırmak gerektiğinde kullan. Panel seçimi, layout hiyerarşisi, drilldown akışı ve “anti‑pattern” (çok panel, çok değişken, gürültü) konularına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Dashboard iskeleti: “Overview → Drilldown → Debug” hiyerarşisi
- Panel türü seçimi (stat/time-series/table/logs/trace) için kısa karar kuralları
- Anti-pattern listesi ve düzeltme önerisi (panel sayısı, renk/threshold, değişken karmaşası)

## Workflow
- Kullanım senaryosunu sabitle:
  - “Incident sırasında” mı, “günlük sağlık” mı, “kapasite trendi” mi?
- Layout hiyerarşisi kur:
  - Üst satır: 3–6 kritik KPI (stat/gauge) — “kırmızı mı?”
  - Orta: Trend panelleri (time series/heatmap) — “ne zamandır kötü?”
  - Alt: Debug panelleri (table/logs links) — “neden kötü?”
- Panel türü seç:
  - Oran/trend: time series
  - Dağılım/latency: heatmap + p95/p99 çizgisi
  - En kötü N: table + sort
  - Log/trace drilldown: logs panel / trace link (derived field)
- Drilldown akışı:
  - Her panelden bir sonraki seviyeye link: service → instance → logs/traces.
  - “Klikle aç” linkleri için label set’i stabil olmalı.
- Görsel tutarlılık:
  - Renk/threshold standardı: aynı metrik aynı renk.
  - Y ekseni birimleri doğru (ms vs s).

## Anti-patterns
- 50+ panel: kimse incident’ta okumaz; böl veya sadeleştir.
- Her şeyi değişken yapmak: yanlış seçim → boş panel; minimal değişken.
- Ham yüksek kardinalite query: dashboard refresh’te sistemi boğar (recording rule düşün).

## References
- `skills/cos-deploy-grafana`
- `cli/skills/agentic-troubleshoot-grafana`
