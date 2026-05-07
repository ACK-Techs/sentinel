---
name: obs-otel-troubleshoot-pipeline
description: OpenTelemetry Collector pipeline’da telemetry akmıyor (receiver kabul etmiyor, processor drop ediyor, exporter fail/retry) gibi sorunları semptom→teşhis→doğrulama akışıyla çözmek gerektiğinde kullan. Amaç: “veri nerede kayboluyor?” sorusunu kanıtla cevaplamak.
---

## Purpose
Bu skill’in çıktısı:
- Receiver→processor→exporter zinciri için kısa teşhis ağacı ve ölçüm noktaları
- Collector telemetry metrikleriyle doğrulama planı (accepted, dropped, sent, failed)
- Çözüm önerisi: ilgili bileşenin config’ini dar ve güvenli şekilde düzeltme

## Workflow
- Semptomu sınıflandır:
  - A) Hiç veri yok (0 accepted)
  - B) Accepted var ama backend yok (sent/failed problemi)
  - C) Veri var ama eksik (drop/filter/sampling)
  - D) Gecikmeli/“burst” (batch/queue/backpressure)
- A) Receiver katmanı:
  - Port/protocol doğru mu? TLS/auth engelliyor mu?
  - Accepted metrikleri artıyor mu?
- B) Exporter katmanı:
  - Endpoint doğru mu? 401/403/404/5xx?
  - Retry/queue şişiyor mu? failed metrikleri?
- C) Processor katmanı:
  - Filter/transform çok mu agresif?
  - Tail sampling policy eşleşmiyor mu?
- D) Performans:
  - Batch size/timeout; memory limiter tetikliyor mu?
  - Horizontal scaling ihtiyacı var mı?
- Doğrulama:
  - Bir test sinyali üret (tek span/metric/log) ve zincirin her adımında “sayım” ile izini sür.

## References
- `skills/obs-otel-collector-pipeline`
- `skills/obs-otel-collector-processors`
- `skills/obs-otel-collector-exporters`
