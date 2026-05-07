---
name: obs-tempo-distributor-config
description: Tempo’ya trace ingest etmek için distributor receiver protokollerini (OTLP, Jaeger, Zipkin) açmak, doğru endpoint/port seçmek veya “trace gönderiyorum ama kabul etmiyor” sorununu çözmek gerektiğinde kullan. Protokol uyumluluğu ve doğrulama adımlarına odaklanır.
---

## Purpose
Bu skill’in çıktısı:
- Hedef protokol için doğru receiver seçimi (OTLP gRPC/HTTP, Jaeger, Zipkin)
- Client tarafı endpoint bilgisi (URL/port/path) ve uyumluluk notu
- Doğrulama: canary trace gönderimi + Tempo’da görme

## Workflow
- Protokol kararını ver:
  - Yeni kurulumlarda OTLP genelde en iyi default’tur.
  - Mevcut ekosistem Jaeger/Zipkin ise uyumluluk receiver’ını seç.
- Endpoint tasarla:
  - gRPC vs HTTP ayrımı (client kütüphanesi ne destekliyor?)
  - Ingress/proxy varsa path/headers bozuluyor mu? (özellikle OTLP/HTTP)
- Güvenlik:
  - Public endpoint açıyorsan auth/TLS ve rate-limit düşün (trace spam kolaydır).
  - Secret’ları örnek komutlarda yazma; placeholder ver.
- Doğrulama:
  - Canary trace gönder (küçük request).
  - Tempo’da trace’i ara (service.name + zaman penceresi).

## Common mistakes
- Client’ın OTLP/HTTP gönderip server’ın sadece OTLP/gRPC dinlemesi (veya tersi).
- Ingress’in gRPC’yi HTTP gibi ele alıp kırması.

## References
- `skills/target-app-fastapi-otel-bootstrap`
- `skills/target-app-observability-lib`
