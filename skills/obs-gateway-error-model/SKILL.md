---
name: obs-gateway-error-model
description: Observability gateway’de Prometheus/Loki/Tempo arka uç hatalarını tek bir tutarlı error modeline çevirmek, secret-safe (token/URL sızdırmayan) hata yanıtı üretmek veya “client neyi retry etmeli?” belirsizliğini çözmek gerektiğinde kullan. Odak: **error contract** ve mapping’dir.
---

## Purpose
Bu skill’in çıktısı:
- Gateway error sözleşmesi: alanlar (code, message, retryable, backend, trace_id) ve HTTP status eşlemesi
- Upstream→gateway mapping tablosu (4xx/5xx/timeout/cancel/parse)
- Doğrulama: 3 hata sınıfında örnek yanıt + log maskleme kanıtı

## Workflow
- Error kontratını sabitle:
  - Client’ın karar vereceği minimum alanlar: `retryable`, `kind`, `upstream_status`, `request_id`.
  - Kullanıcıya gösterilecek mesaj ile log mesajını ayır (log daha ayrıntılı, yanıt daha güvenli).
- Hata sınıfları:
  - Client hatası (400/401/403/404): retryable=false.
  - Upstream geçici (429/502/503/504, timeout): retryable=true + backoff hint.
  - Upstream kalıcı (4xx ama client değil: ör. bad query): retryable=false.
- Secret-safe kurallar:
  - URL’deki token/query parametrelerini maskele.
  - Header’ları (Authorization) asla response’a taşımama.
- Observability:
  - Her hata yanıtına `trace_id`/`request_id` koy; log’la korele edilsin.
- Doğrulama:
  - Timeout/429/bad query senaryosunda: status + body alanları beklenen mi?

## Common mistakes
- Hata mesajına upstream response body’yi aynen basmak: secret/PII sızar.
- Her şeyi 500 dönmek: client retry karar veremez, debug zorlaşır.

## References
- `skills/obs-gateway-retry-timeout`
- `skills/obs-gateway-auth-token`
