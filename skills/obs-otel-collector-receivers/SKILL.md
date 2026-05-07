---
name: obs-otel-collector-receivers
description: OpenTelemetry Collector receiver’larını seçmek ve doğru şekilde expose etmek (OTLP gRPC/HTTP, Prometheus scrape, filelog, Jaeger/Zipkin) gerektiğinde kullan. Odak: giriş protokolü, port/TLS/auth ve “agent vs gateway” yerleşimi.
---

## Purpose
Bu skill’in çıktısı:
- Receiver seçimi ve YAML snippet’i (hangi sinyal, hangi port, hangi auth/TLS)
- Yerleşim kararı: node-agent mı central-gateway mi?
- Doğrulama: receiver accepted metrikleriyle “trafik geliyor” kanıtı

## Workflow
- Trafik kaynaklarını yaz:
  - Uygulama OTLP mi gönderiyor? (SDK)
  - Mevcut Prometheus endpoint’leri scrape edilecek mi?
  - Node log dosyaları mı toplanacak? (filelog)
- Receiver seç:
  - OTLP: gRPC/HTTP endpointleri (SDK’larla uyum).
  - Prometheus receiver: scrape target ve relabel ihtiyacı.
  - Filelog: multiline/regex/JSON parse ihtiyacı.
  - Jaeger/Zipkin: legacy trace ingest gerekiyorsa.
- Güvenlik ve ağ:
  - İnternete açık mı? değilse cluster/internal ile sınırla.
  - TLS/mTLS ihtiyacı; token’ları config’e gömme.
- Yerleşim:
  - Agent: node’a yakın (logs/host metrics için).
  - Gateway: merkezi fan-in (OTLP throughput, tenant routing).
- Doğrulama:
  - Collector telemetry’de receiver accepted metriklerine bak.

## Common mistakes
- Gateway’i internete açık OTLP endpoint yapmak: saldırı yüzeyi büyür.
- Receiver açıp pipeline’a bağlamamak: port açık ama sinyal işlenmez.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
