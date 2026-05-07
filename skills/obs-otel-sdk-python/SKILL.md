---
name: obs-otel-sdk-python
description: Python servisinde OpenTelemetry SDK ile manuel enstrümantasyon kurmak (trace/metric/log provider, exporter, resource, propagator) veya “trace geliyor ama service.name yanlış / metric yok / log korelasyonu yok” gibi SDK-seviyesi problemleri çözmek gerektiğinde kullan.
---

## Purpose
Bu skill’in çıktısı:
- Python için “minimum çalışır” SDK kurulumu iskeleti (resource + tracer/meter/logger)
- Exporter seçimi (OTLP) ve güvenli config (endpoint/headers secret’ı yazmadan)
- Doğrulama: tek bir test span/metric/log ile backend’de görünürlük kanıtı

## Workflow
- Enstrümantasyon kapsamını seç:
  - Sadece traces mi? traces+metrics mi? logs korelasyonu da var mı?
- Resource kontratını sabitle:
  - `service.name`, `service.version`, `deployment.environment` gibi alanları netleştir.
- Provider’ları kur:
  - TracerProvider + span processor (batch).
  - MeterProvider + periodic reader.
  - (Varsa) LoggerProvider + log exporter.
- Exporter ve auth:
  - OTLP gRPC/HTTP endpoint seç; header/token değerlerini ENV/secret üzerinden geçir.
- Propagation:
  - W3C TraceContext varsayılan; gerekiyorsa baggage/extra propagator kararını yaz.
- Doğrulama:
  - Basit bir endpoint’te “test span” üret.
  - Backend’de trace görünür mü; service.name doğru mu; exemplars varsa metric→trace linki çalışıyor mu?

## Common mistakes
- `service.name`’i rastgele/host bazlı yapmak: servis kimliği parçalanır.
- Exporter endpoint’ini yanlış protokolle yazmak: veri sessizce kaybolur veya retry ile kuyruk şişer.

## References
- `skills/obs-otel-semantic-conventions`
- `skills/obs-otel-context-propagation`
- `skills/target-app-fastapi-otel-bootstrap`
