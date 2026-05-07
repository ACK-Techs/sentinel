---
name: obs-gateway-prometheus-adapter
description: Observability gateway içinde Prometheus adapter katmanı yazmak (query/range API proxy, label normalizasyonu, hata ve timeout yönetimi) veya “PromQL sonuçları gateway’de bozuluyor” sorununu çözmek gerektiğinde kullan. Odak: **Prometheus HTTP API sözleşmesi** ve yanıt normalleştirmesidir.
---

## Purpose
Bu skill’in çıktısı:
- Adapter sözleşmesi: hangi Prometheus endpoint’leri destekleniyor, hangi parametreler forward ediliyor?
- Normalizasyon kuralları: tenant label ekleme/strip, time parametreleri, step limit
- Doğrulama: 2 örnek query ile upstream vs gateway yanıt eşleşmesi kanıtı

## Workflow
- API kapsamını seç:
  - `query`, `query_range`, `labels`, `series` gibi endpoint’ler.
- Parametre hijyeni:
  - `start/end/step` validasyonu; step için üst sınır (çok küçük step → payload patlar).
  - Zaman formatı ve timezone tutarlılığı.
- Multi-tenancy:
  - Tenant’ı header’dan alıp upstream’e nasıl yansıtacaksın? (label rewrite mi, ayrı Prometheus mu)
- Yanıt normalizasyonu:
  - Upstream hata formatını gateway error modeline map et.
  - Büyük yanıtlar için streaming/pagination stratejisi (varsa).
- Doğrulama:
  - Basit `up` query: gateway ve upstream aynı resultType/result verir mi?
  - `query_range` ile step ve datapoint sayısı limitleri çalışıyor mu?

## Common mistakes
- Step limit koymamak: gateway OOM veya upstream’i DoS eder.
- Label rewrite ile kardinaliteyi artırmak: query ve storage maliyeti artar.

## References
- `skills/obs-gateway-error-model`
- `skills/obs-gateway-retry-timeout`
