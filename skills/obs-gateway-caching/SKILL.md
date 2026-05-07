---
name: obs-gateway-caching
description: Gateway’de Prometheus/Loki sorgularını cache’lemek (query key tasarımı, TTL, tenant izolasyonu, invalidate) veya “aynı dashboard her refresh’te backend’i yakıyor” sorununu çözmek gerektiğinde kullan. Odak: **cache correctness + maliyet**.
---

## Purpose
Bu skill’in çıktısı:
- Cache key sözleşmesi: tenant + endpoint + normalized params (time range dahil)
- TTL stratejisi: instant vs range query; stale-while-revalidate opsiyonu
- Doğrulama: cache hit oranı + aynı sorguda backend çağrısı azalması kanıtı

## Workflow
- Cache’lenebilirliği belirle:
  - Instant query: kısa TTL ile cache’lenebilir.
  - Range query: step ve aralığa göre cache’lenebilir ama key şişebilir.
  - Tail/stream: cache olmaz.
- Key normalizasyonu:
  - Parametreleri canonical sıraya sok; “eşdeğer sorgular” aynı key’e düşsün.
  - Time range’i yuvarlama kararı (örn. 5s/10s bucket) ve veri tazeliği etkisi.
- Tenant izolasyonu:
  - Tenant key’in parçası olmak zorunda; aksi veri sızıntısı.
- TTL ve invalidation:
  - TTL kısa başla; dashboard refresh süresiyle uyumlu ayarla.
  - Backend error’larında cache’e ne koyacaksın? (genelde koyma, veya kısa negative cache)
- Doğrulama:
  - Aynı query arka arkaya: ikinci çağrıda backend’e gitmemeli (hit).
  - Cache bypass/disable mekanizması (debug) çalışıyor mu?

## Common mistakes
- Time parametrelerini normalize etmemek: hit oranı düşük kalır.
- 5xx hatasını uzun süre cache’lemek: outage uzatır.

## References
- `skills/obs-gateway-rate-limiting`
- `skills/obs-gateway-prometheus-adapter`
