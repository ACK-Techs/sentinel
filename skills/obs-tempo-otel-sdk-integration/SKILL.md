---
name: obs-tempo-otel-sdk-integration
description: Uygulamada OpenTelemetry SDK ile trace üretmek ve OTLP exporter üzerinden Tempo’ya göndermek için gerekli minimum ayarları yapmak gerektiğinde kullan. “service.name ayarı”, “OTLP endpoint”, “propagation”, “trace yok” gibi uygulama‑tarafı entegrasyon sorularına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Uygulama tarafında minimum “trace contract”: `service.name`, environment, propagators
- OTLP exporter hedefi ve protokol (HTTP vs gRPC) seçimi
- Canary doğrulama: tek istek üret → Tempo’da trace bul

## Workflow
- Resource/kimlik:
  - `service.name` zorunlu ve stabil olmalı (grafana/tempo query bunun üstüne kurulur).
  - `deployment.environment` gibi ortam bilgisini ekle (prod/staging).
- Export:
  - OTLP endpoint’i netleştir (collector mı, direkt tempo mu?).
  - HTTP mi gRPC mi? (kullandığın SDK/exporter neyi destekliyor?)
- Propagation:
  - W3C TraceContext varsayılan; gateway/ingress ile uyumlu mu?
  - Log korelasyonu istiyorsan trace_id’yi log’a da koyma planı yap.
- Sampling:
  - Başlangıçta “çok düşük” sample rate ile debug zorlaşır; canary için yeterli olacak şekilde ayarla.
- Doğrulama:
  - Canary request üret (tek endpoint çağrısı).
  - Tempo’da `service.name` + kısa zaman penceresiyle ara; trace aç ve span’lar var mı bak.

## Common mistakes
- `service.name` boş/yanlış: Tempo’da arama “yokmuş” gibi görünür.
- OTLP protocol mismatch (client HTTP, server gRPC veya tersi).

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
