---
name: obs-otel-collector-pipeline
description: OpenTelemetry Collector’da metrics/logs/traces için pipeline tasarlamak (receiver→processor→exporter zinciri, fanout, tenant/env ayrımı) veya “sinyal bir yerde kayboluyor” problemini çözmek gerektiğinde kullan. Amaç tek bir çalışır YAML pipeline iskeleti ve doğrulama adımı üretmektir.
---

## Purpose
Bu skill’in çıktısı:
- Sinyal bazlı pipeline iskeleti (metrics/logs/traces ayrı) ve bileşen seçimi gerekçesi
- Fanout/routing kararı (aynı sinyali birden çok backend’e gönderme)
- Doğrulama: Collector metrics/log’larıyla “alıyor → işliyor → export ediyor” kanıtı

## Workflow
- Bağlamı sabitle:
  - Hangi sinyaller var? (metrics/logs/traces)
  - Hedef backends: Prometheus remote-write, Loki, Tempo/OTLP, başka?
- Pipeline’ı sinyal bazlı kur:
  - `receivers`: OTLP gRPC/HTTP gibi girişler.
  - `processors`: minimum set (batch + memory limiter), sonra enrichment/filter.
  - `exporters`: her backend için bir exporter.
  - `service.pipelines`: her sinyal için ayrı liste.
- Fanout/routing:
  - Aynı trace’i hem Tempo’ya hem debug exporter’a göndermek gibi senaryoları açık yaz.
- Güvenlik ve maliyet:
  - PII içeren attribute/log alanlarını filtreleme ihtiyacı var mı?
  - Sampling/attribute drop kararlarını not et (bu skill pipeline iskeleti üretir).
- Doğrulama:
  - Collector’ın kendi telemetry metriklerinden receiver accepted / exporter sent değerlerini kontrol et.

## Common mistakes
- Metrics/logs/traces’i tek pipeline’da karıştırmak: debug zorlaşır.
- Processor ekleyip doğrulamamak: sinyal sessizce düşebilir (drop/filter).

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
