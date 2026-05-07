---
name: obs-gateway-rate-limiting
description: Gateway’de rate limiting ile Prometheus/Loki/Tempo backends’i korumak (tenant bazlı limit, endpoint bazlı limit, burst kontrolü) veya “bir tenant herkesi yavaşlatıyor” sorununu çözmek gerektiğinde kullan. Odak: **adil paylaşım + maliyet kontrollü limit**.
---

## Purpose
Bu skill’in çıktısı:
- Limit politikası: global + tenant + endpoint sınıfları (search vs get-by-id)
- 429 yanıt semantiği (retry-after, error model uyumu)
- Doğrulama: limit aşımı, burst ve iyi tenant’ın etkilenmemesi senaryoları

## Workflow
- Trafiği sınıflandır:
  - Pahalı: TraceQL search, geniş LogQL regex, PromQL küçük step query_range.
  - Ucuz: trace by id, basit status endpoints.
- Anahtar seç:
  - Tenant (zorunlu) + (opsiyonel) user/client id.
- Limit türleri:
  - RPS limit + concurrency limit (özellikle uzun süren sorgular için).
  - Burst bucket (kısa patlamayı tolere et).
- Yanıt ve observability:
  - 429 → retryable=true; error model alanlarını doldur.
  - Rate limit metrikleri üret (dropped, limited, latency impact).
- Doğrulama:
  - Pahalı endpoint’te limit çalışıyor mu?
  - Ucuz endpoint’ler aynı anda erişilebilir mi?

## Common mistakes
- Tek global limit: noisy neighbor problemi çözülmez.
- Limit koyup client’a retry semantiği vermemek: gereksiz yeniden deneme fırtınası.

## References
- `skills/obs-gateway-error-model`
- `skills/obs-gateway-auth-token`
