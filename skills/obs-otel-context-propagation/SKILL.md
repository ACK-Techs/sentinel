---
name: obs-otel-context-propagation
description: Servisler arası W3C TraceContext (`traceparent`) ve Baggage header propagation’ını kurmak veya “trace kopuyor”, “aynı request iki ayrı trace oluyor” sorunlarını çözmek gerektiğinde kullan. Odak: header sözleşmesi, gateway/proxy etkisi ve doğrulama akışıdır.
---

## Purpose
Bu skill’in çıktısı:
- Propagation kontratı: hangi propagator’lar aktif, hangi header’lar allow/strip?
- Proxy/gateway checklist’i: ingress, service mesh, API gateway, CORS etkileri
- Doğrulama: uçtan uca tek trace ID ile zincirin korunması kanıtı

## Workflow
- Zinciri haritala:
  - Hangi servisler çağrı yapıyor? hangi protokoller var (HTTP/gRPC)?
  - Arada hangi ara katmanlar var (ingress, gateway, mesh)?
- Propagator seç:
  - Varsayılan: W3C TraceContext.
  - Baggage gerekiyorsa ekle; risklerini not et.
- Header politikası:
  - Ara katmanlarda `traceparent`/`tracestate` header’ları drop ediliyor mu?
  - CORS varsa allowlist’e ekle.
- “Trace kopuyor” teşhisi:
  - Upstream header gelmiyor mu? (client instrument yok)
  - Downstream çıkarıyor mu? (proxy strip)
  - Async job/queue boundary var mı? (context geçişi ayrı tasarım ister)
- Doğrulama:
  - Tek bir request’i tüm servislerde aynı trace ID ile görmeyi hedefle.

## Common mistakes
- Gateway’in güvenlik amaçlı header temizliği yapması ve trace header’ını da silmesi.
- Queue/async sınırında propagation beklemek: explicit context taşıma gerekir.

## References
- `skills/obs-otel-baggage`
- `skills/obs-otel-sdk-python`
