---
name: obs-otel-exemplars-bridge
description: Metric→trace köprüsü için exemplars’ı uçtan uca kurmak (SDK exemplar üretimi, Collector/Prometheus/Grafana tarafında görünürlük) veya “Grafana’da exemplar yok, trace linki çıkmıyor” sorununu çözmek gerektiğinde kullan. Odak: **metrik panelinden trace’e tıkla** deneyimidir.
---

## Purpose
Bu skill’in çıktısı:
- Exemplars için gereksinim listesi (histogram/metrics + trace id bağlama koşulları)
- Kurulum kontrol listesi: SDK → Collector → backend → Grafana
- Doğrulama: yüksek latency anında panelde exemplar noktası ve trace linki kanıtı

## Workflow
- Ön koşulları doğrula:
  - Traces üretiliyor mu? metrics üretiliyor mu? aynı service/resource kimliği var mı?
- SDK tarafı:
  - Trace context ile metrik kaydı aynı execution context’te mi?
  - Uygun metrik türü seç (latency histogram gibi).
- Collector/Backend:
  - Trace id’nin metric exemplar alanına taşınması engelleniyor mu? (processor/filter)
  - Prometheus/Grafana tarafında exemplars destekli sorgulama açık mı?
- Grafana UX:
  - Panelde exemplars gösterimi açık mı?
  - Tempo datasource ile trace linki doğru mu?
- Doğrulama:
  - Kontrollü bir “yavaş istek” üret; panelde exemplar noktasından trace aç.

## Common mistakes
- Metric ile trace’in farklı `service.name` altında toplanması: köprü kırılır.
- Processor ile context/attribute drop edip exemplar ilişkilendirmesini bozmak.

## References
- `skills/obs-tempo-exemplars-grafana`
- `skills/obs-grafana-trace-panel`
