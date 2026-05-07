---
name: obs-prometheus-exemplars
description: Metric’ten trace’e “tek tıkla gitmek” için Prometheus exemplars’ı etkinleştirmek veya Grafana/Tempo’da exemplar üzerinden trace linkini çalışır hale getirmek gerektiğinde kullan. “exemplar görünmüyor”, “traceID label’i”, “histogram + exemplars” gibi spesifik sorunlara odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Exemplars’ın hangi metriklerde/formatlarda çalışacağına dair net şartlar (genelde histogram/counter)
- Trace korelasyonu için gerekli alan: ör. `trace_id` / `traceID` gibi anahtarın hangi tarafta üretileceği
- Grafana’da “exemplar → Tempo trace” linkinin çalışması için kontrol listesi

## Workflow
- Ön koşulları doğrula:
  - Trace backend var mı? (bu repoda tipik: Tempo)
  - Grafana’da Tempo datasource çalışıyor mu? (yoksa önce onu düzelt)
- Exemplars kaynağını belirle:
  - Exemplars genelde **instrumentation** katmanından gelir (uygulama/SDK).
  - Hangi metrik ailesi: histogram bucket’ları en tipik kullanım (latency).
- “Trace ID anahtarı”nı standartlaştır:
  - Exemplars içine hangi alan yazılacak? (örn. `trace_id`)
  - Aynı anahtarın Tempo tarafında aranan alanla uyumlu olduğundan emin ol.
- Prometheus tarafında görünürlük:
  - Exemplars her seride sürekli gelmez; sampling ve trafik etkiler.
  - Panelde p95/p99 çiziyorsan, exemplar’lar çoğunlukla histogram üzerinden anlamlıdır.
- Grafana tarafında link:
  - Panel/Explore’da exemplar tooltip’inde trace linki çıkıyor mu?
  - Çıkmıyorsa: Tempo datasource, traceId field mapping, ve panel query türünü kontrol et.
- Doğrulama:
  - Bilinçli bir test isteği üret (trace oluşsun), aynı zaman penceresinde metric exemplar’ını yakala.
  - Exemplars varsa, linkten açılan trace’in aynı request’e ait olduğunu doğrula.

## Failure modes
- Low traffic: exemplar “yokmuş” gibi görünür (sample denk gelmeyebilir).
- Yanlış anahtar: exemplar var ama trace linklenmez.

## References
- `skills/obs-tempo-grafana-datasource`
- `skills/obs-grafana-prometheus-explore`
