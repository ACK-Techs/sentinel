---
name: obs-otel-collector-exporters
description: OpenTelemetry Collector exporter’larını hedef backend’lere göre yapılandırmak (OTLP/Tempo, Loki, Prometheus remote_write, debug/logging) veya “exporter hata veriyor, kuyruk doluyor” sorununu çözmek gerektiğinde kullan. Odak: endpoint/auth, retry/queue ve backpressure.
---

## Purpose
Bu skill’in çıktısı:
- Backend’e göre exporter YAML snippet’i (endpoint + auth/TLS + retry/queue)
- Backpressure stratejisi: kuyruk, retry ve drop risklerinin yazımı
- Doğrulama: exporter sent/failed metrikleri ile “çıktı gidiyor” kanıtı

## Workflow
- Hedef backend’leri listele:
  - Traces: Tempo/OTLP?
  - Logs: Loki?
  - Metrics: Prometheus remote_write?
- Exporter seçimi:
  - Backend’in beklediği protokolü seç (OTLP gRPC/HTTP, remote_write).
  - Debug exporter’ı sadece geçici kullan (prod’da gürültü).
- Auth/TLS:
  - Token/username/password değerlerini config’e gömme; secret store/ENV kullan.
  - mTLS gerekiyorsa sertifika kaynaklarını belirt.
- Retry/queue/backpressure:
  - Geçici hatalarda retry; kalıcı 4xx’lerde hızlı fail.
  - Kuyruk boyutu ve concurrency’yi hedef throughput’a göre ayarla.
  - Hedef down ise “ne olur?” (kuyruk dolar mı drop olur mu) açık yaz.
- Doğrulama:
  - Collector telemetry’de exporter sent/failed değerlerini izle.
  - Backend tarafında veri görünüyor mu? (Grafana’da basit sorgu)

## Common mistakes
- Exporter’ı pipeline’a eklemeyi unutmak: config var ama veri çıkmaz.
- Hedef endpoint’i yanlış (http/https, path, port): sürekli retry ile kuyruk şişer.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
