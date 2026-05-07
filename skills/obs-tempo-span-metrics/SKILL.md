---
name: obs-tempo-span-metrics
description: Trace span’larından metrik (RED: rate/errors/duration) türetmek ve bu metrikleri Prometheus’ta kullanılabilir hale getirmek gerektiğinde kullan. “Span metrics nedir?”, “trace’den error rate çıkar”, “latency histogram üret” gibi span→metric pipeline tasarımı için.
---

## Purpose
Bu skill’in çıktısı:
- Span→metric dönüşümü için net plan (hangi span’lar, hangi label set’i, hangi histogram bucket’lar)
- Kardinalite kontrolü: metrikte taşınacak dimension’lar (service, route group, status class)
- Doğrulama: Prometheus’ta RED metriklerinin geldiğini kanıtlama (örnek PromQL)

## Workflow
- Ön koşul:
  - Trace’lerde `service.name` ve hata bilgisi tutarlı mı? (status / http.status_code)
- Hangi metrikleri türeteceğini seç:
  - Rate: istek sayısı (counter)
  - Errors: 5xx/ERROR oranı (counter + label)
  - Duration: histogram/summary kararı (genelde histogram)
- Dimension (label) bütçesi:
  - Stabil ve az değerli alanları seç (service, env, route_group).
  - Dinamik path, request_id, user_id gibi alanları metrik label yapma.
- Histogram tasarımı:
  - SLO bandını kapsayan bucket seti belirle (çok fazla bucket maliyet).
- Export yolu:
  - Metrikler Prometheus tarafından scrape edilecek mi? (endpoint) Yoksa remote_write benzeri mi?
  - Bu repo bağlamında “Prometheus’a görünür metrik” hedefini net yaz.
- Doğrulama:
  - Canary trace üret → ardından Prometheus’ta metrik artıyor mu kontrol et.
  - Örnek PromQL: rate/error ratio/p95 latency sorguları.

## Common mistakes
- Span attribute’larını sınırsız label’a çevirmek: metrik cardinality patlar.
- Sampling çok agresif: derived metrikler gerçeği temsil etmez (özellikle low traffic).

## References
- `skills/obs-tempo-sampling-strategy`
- `skills/obs-prometheus-histogram-summary`
