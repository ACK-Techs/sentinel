---
name: obs-otel-sdk-auto-instrument
description: Python uygulamasında OpenTelemetry auto-instrumentation ile sıfır/az kod değişikliğiyle izleme açmak; “instrumentation çalışmıyor”, “yanlış exporter”, “span’lar eksik/duplikasyon var” gibi sorunları çözmek gerektiğinde kullan. Manuel SDK kurulumundan farklı olarak **CLI/env tabanlı kurulum** odaklıdır.
---

## Purpose
Bu skill’in çıktısı:
- Auto-instrumentation çalıştırma komutu ve gerekli ENV değişken seti (OTLP endpoint dahil)
- Hangi enstrümantasyon paketleri gerekli (web framework, requests, db) karar matrisi
- Doğrulama: uygulama ayağa kalkınca backend’de beklenen temel span’ların görünmesi

## Workflow
- Uygulama çalıştırma modelini belirle:
  - Gunicorn/Uvicorn, systemd, container entrypoint vs.
- Enstrümantasyon kapsamı seç:
  - Web framework + HTTP client + DB driver (ihtiyaca göre).
  - Double-instrument riskini not et (hem manuel hem auto aynı anda olmasın).
- Konfigürasyon:
  - OTLP endpoint/protocol, service.name, environment.
  - Propagators (TraceContext/Baggage).
- Çalıştır:
  - Uygulama komutunu “instrument” wrapper’ı ile başlat (entrypoint’e entegre et).
- Hata modu teşhisi:
  - Span yok: paket eksik, env yanlış, exporter unreachable.
  - Çok span: duplicate instrumentation.
  - service.name parçalı: env/host bazlı set edilmiş.
- Doğrulama:
  - Basit bir HTTP request gönder; trace grafı oluşuyor mu kontrol et.

## Common mistakes
- Prod’da debug log/verbose exporter ile çalışmak: gürültü ve maliyet.
- Auto-instrumentation’ı “her şeyi çözer” sanmak: domain span’ları yine manuel gerekir.

## References
- `skills/obs-otel-sdk-python`
- `skills/obs-otel-context-propagation`
