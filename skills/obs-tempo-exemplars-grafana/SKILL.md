---
name: obs-tempo-exemplars-grafana
description: Grafana’da Prometheus metric exemplar’larından Tempo trace’ine geçişi (link) çalıştırmak gerektiğinde kullan. “Metric’te exemplar var ama trace’e gitmiyor”, “Explore’da trace linki”, “traceID field mapping” gibi exemplar→Tempo korelasyonu odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Grafana’da exemplar tooltip’inden Tempo trace açılacak şekilde gerekli kontrol listesi
- `trace_id` gibi anahtarın metric exemplar’ında nasıl taşındığına dair netlik
- Doğrulama: örnek bir histogram panelinde exemplar görme ve trace açma testi

## Workflow
- Ön koşullar:
  - Grafana’da Prometheus ve Tempo datasource’ları sağlıklı mı?
  - Uygulama trace üretiyor mu (Tempo’da en azından bir trace bulunabiliyor mu)?
- Exemplar’ın varlığını doğrula:
  - Histogram/metric panelinde exemplar noktaları görünüyor mu?
  - Görünmüyorsa önce instrumentation/exemplar üretimi (ayrı skill) kontrol et.
- Trace ID eşlemesini doğrula:
  - Exemplar içinde hangi anahtar var? (örn. `trace_id`)
  - Tempo’nun beklediği formatla uyumlu mu?
- Grafana link:
  - Explore/panel üzerinde exemplar tooltip’inde “View trace” benzeri link çıkıyor mu?
  - Çıkmıyorsa Tempo datasource ayarlarını ve traceId mapping’i kontrol et.
- Doğrulama:
  - Bilinçli bir istek üret; aynı zaman penceresinde exemplar’a tıkla ve doğru trace açılıyor mu bak.

## Common mistakes
- Tempo datasource yok/bozukken exemplar link beklemek.
- Exemplar anahtar adı uyumsuz (trace id var ama Grafana/Tempo okuyamıyor).

## References
- `skills/obs-prometheus-exemplars`
- `skills/obs-tempo-grafana-datasource`
