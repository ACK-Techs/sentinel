---
name: obs-tempo-pipeline-e2e
description: OTEL SDK → OTEL Collector → Tempo → Grafana zincirinin uçtan uca çalıştığını kanıtlamak gerektiğinde kullan. “Trace üretildi mi?”, “collector export ediyor mu?”, “Tempo’da bulunuyor mu?”, “Grafana’da açılıyor mu?” adımlarını canary ile doğrular.
---

## Purpose
Bu skill’in çıktısı:
- Uçtan uca canary senaryosu (tek request) ve her hop için doğrulama sinyali
- Hangi noktada kopuyor? (SDK, collector, tempo ingest, tempo query, grafana datasource) hızlı ayrım
- “Başarılı” kriteri: Tempo’da trace bulunur ve Grafana’da açılır

## Workflow
- 1) SDK doğrulaması:
  - Uygulamada `service.name` net mi?
  - Canary request üret (tek endpoint).
- 2) Collector doğrulaması:
  - Receiver log/metric: canary trace geldi mi?
  - Exporter log/metric: Tempo’ya gönderim hatasız mı?
- 3) Tempo ingest doğrulaması:
  - Tempo/distributor loglarında reject var mı? (protokol, auth, tenant)
  - Storage yazımı sorunlu mu?
- 4) Tempo query doğrulaması:
  - `service.name` + kısa zaman penceresiyle trace ara; bir trace id elde et.
  - Trace get ile trace’i aç (span’lar var mı?).
- 5) Grafana doğrulaması:
  - Tempo datasource bağlantısı sağlıklı mı?
  - Explore’da aynı trace id açılıyor mu?

## Common mistakes
- Sampling yüzünden canary trace’in düşmesi (testte sampling’i geçici yükselt).
- OTLP protocol mismatch (client HTTP, server gRPC).

## References
- `skills/obs-tempo-otel-sdk-integration`
- `skills/obs-tempo-troubleshoot-ingest`
- `skills/obs-tempo-grafana-datasource`
