---
name: obs-gateway-retry-timeout
description: Gateway’de backend çağrıları için timeout/retry politikası ve circuit breaker tasarlamak veya “retry yüzünden patlıyor / timeout yüzünden boş sonuç dönüyor” sorunlarını çözmek gerektiğinde kullan. Odak: **idempotency + backpressure + doğru fail-fast**.
---

## Purpose
Bu skill’in çıktısı:
- Endpoint sınıfına göre timeout/retry matrisi (get-by-id vs search)
- Circuit breaker koşulları (error rate, consecutive failures) ve half-open doğrulama
- Doğrulama: backend yavaş/down senaryosunda gateway davranışının deterministik kanıtı

## Workflow
- Çağrıları sınıflandır:
  - Deterministik/ucuz (trace by id) → kısa timeout, sınırlı retry.
  - Pahalı/search (TraceQL, LogQL regex) → daha uzun timeout ama çoğu zaman retry=0 (duplicate load).
- Retry kuralları:
  - Sadece geçici hatalarda (502/503/504, timeout) retry.
  - 4xx’lerde retry yok.
  - Exponential backoff + jitter; toplam süre üst sınırı.
- Circuit breaker:
  - Backend bazlı breaker (Prom/Loki/Tempo ayrı).
  - Open olduğunda hızlı fail + status endpoint’te “degraded” göster.
- Cancellation:
  - Client request iptal ederse upstream çağrıyı da iptal etmeye çalış.
- Doğrulama:
  - Backend’i yavaşlat: timeout tetikleniyor mu, retry sayısı beklenen mi?
  - Backend down: breaker open oluyor mu, gateway yükü stabil mi?

## Common mistakes
- Pahalı search’te retry yapmak: backend’i daha da boğar.
- Timeout’u çok uzun bırakmak: concurrency dolar, gateway kilitlenir.

## References
- `skills/obs-gateway-health-status`
- `skills/obs-gateway-rate-limiting`
